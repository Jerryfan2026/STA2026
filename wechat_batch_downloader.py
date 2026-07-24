"""
微信公众号文章批量下载工具

说明：
- 仅用于下载你已合法获取访问权限的公众号文章页面
- 需要提供文章 URL 列表（.txt 或 .csv）
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from html import unescape
from pathlib import Path
from typing import List, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


DEFAULT_USER_AGENT = (
    # 可按需定期更新版本号，避免被识别为过旧客户端
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
)
RETRY_BACKOFF_MULTIPLIER = 2
MAX_RETRY_DELAY_SECONDS = 5
# Windows/Unix 文件名非法字符 + 常见控制字符
FILENAME_INVALID_CHARS_PATTERN = r"[\\/:*?\"<>|\n\r\t]+"


def non_negative_float(value: str) -> float:
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("该参数必须为非负数")
    return number


def positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("该参数必须大于0")
    return number


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="微信公众号文章批量下载")
    parser.add_argument("-i", "--input", required=True, help="URL列表文件路径（txt/csv）")
    parser.add_argument("-o", "--output-dir", default="wechat_articles", help="输出目录")
    parser.add_argument("--delay", type=non_negative_float, default=1.5, help="每次请求间隔（秒）")
    parser.add_argument("--timeout", type=positive_int, default=25, help="请求超时（秒）")
    parser.add_argument("--retries", type=positive_int, default=3, help="失败重试次数")
    parser.add_argument("--cookie", default="", help="可选：请求 Cookie")
    parser.add_argument(
        "--referer",
        default="https://mp.weixin.qq.com/",
        help="可选：Referer 头，默认微信域名",
    )
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="可选：User-Agent")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已存在文件")
    return parser.parse_args()


def load_urls(file_path: Path) -> List[str]:
    if not file_path.exists():
        raise FileNotFoundError(f"输入文件不存在: {file_path}")

    urls: List[str] = []
    suffix = file_path.suffix.lower()

    if suffix == ".csv":
        with file_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                value = row[0].strip()
                if value and value.startswith("http"):
                    urls.append(value)
    else:
        with file_path.open("r", encoding="utf-8-sig") as f:
            for line in f:
                value = line.strip()
                if value and not value.startswith("#") and value.startswith("http"):
                    urls.append(value)

    return urls


def sanitize_filename(name: str, max_len: int = 150) -> str:
    safe = re.sub(FILENAME_INVALID_CHARS_PATTERN, "_", name).strip()
    safe = "".join(ch for ch in safe if ch.isprintable())
    safe = re.sub(r"\s+", " ", safe)
    if not safe:
        safe = "untitled"
    return safe[:max_len]


def extract_title(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if not match:
        return "untitled"
    title = unescape(match.group(1)).strip()
    title = re.sub(r"\s*[-|_]\s*微信公众平台\s*$", "", title)
    return title or "untitled"


def fetch_html(
    url: str,
    timeout: int,
    retries: int,
    user_agent: str,
    referer: str,
    cookie: str,
) -> Tuple[bool, str]:
    headers = {
        "User-Agent": user_agent,
        "Referer": referer,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    if cookie:
        headers["Cookie"] = cookie

    last_error = ""
    for attempt in range(1, retries + 1):
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                charset = resp.headers.get_content_charset() or "utf-8"
                text = raw.decode(charset, errors="replace")
                return True, text
        except HTTPError as e:
            last_error = f"HTTP {e.code}"
        except URLError as e:
            last_error = f"URL Error: {e.reason}"
        except Exception as e:
            last_error = str(e)

        if attempt < retries:
            time.sleep(min(RETRY_BACKOFF_MULTIPLIER * attempt, MAX_RETRY_DELAY_SECONDS))

    return False, last_error


def save_article(
    html: str,
    url: str,
    index: int,
    output_dir: Path,
    overwrite: bool,
) -> Path:
    title = sanitize_filename(extract_title(html))
    file_name = f"{index:04d}_{title}.html"
    file_path = output_dir / file_name
    meta_path = output_dir / f"{index:04d}_{title}.json"
    meta = {
        "url": url,
        "title": title,
        "host": urlparse(url).netloc,
        # Unix epoch seconds
        "saved_at": int(time.time()),
    }
    if file_path.exists() and not overwrite:
        if not meta_path.exists():
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        return file_path

    file_path.write_text(html, encoding="utf-8")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return file_path


def main() -> int:
    """命令行入口。

    返回码：
    - 0: 全部成功
    - 1: 部分成功，部分失败
    - 2: 全部失败
    """
    args = parse_args()
    input_file = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    urls = load_urls(input_file)
    if not urls:
        print("未找到可用URL，请检查输入文件。")
        return 1

    success_count = 0
    fail_count = 0
    manifest_rows = []

    print(f"共读取 {len(urls)} 条URL，开始下载...")
    for i, url in enumerate(urls, start=1):
        ok, content_or_error = fetch_html(
            url=url,
            timeout=args.timeout,
            retries=args.retries,
            user_agent=args.user_agent,
            referer=args.referer,
            cookie=args.cookie,
        )
        if ok:
            file_path = save_article(
                html=content_or_error,
                url=url,
                index=i,
                output_dir=output_dir,
                overwrite=args.overwrite,
            )
            success_count += 1
            manifest_rows.append({"index": i, "url": url, "status": "success", "file": str(file_path.name)})
            print(f"[{i}/{len(urls)}] ✅ {file_path.name}")
        else:
            fail_count += 1
            manifest_rows.append({"index": i, "url": url, "status": "failed", "error": content_or_error})
            print(f"[{i}/{len(urls)}] ❌ {url} -> {content_or_error}")

        if i < len(urls):
            time.sleep(args.delay)

    manifest_path = output_dir / "download_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "total": len(urls),
                "success": success_count,
                "failed": fail_count,
                "items": manifest_rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\n下载完成")
    print(f"- 总数: {len(urls)}")
    print(f"- 成功: {success_count}")
    print(f"- 失败: {fail_count}")
    print(f"- 清单: {manifest_path}")
    if fail_count == 0:
        return 0
    if success_count > 0:
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
