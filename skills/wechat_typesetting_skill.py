"""
wechat_typesetting_skill.py
===========================
公众号编辑与排版 Python Skill
将 Markdown 转换为微信公众号兼容的内联样式 HTML。

参考工具（按 ⭐ 排序）：
  1. doocs/md        ⭐ 13,016  https://github.com/doocs/md
  2. wechat-format   ⭐  4,540  https://github.com/lyricat/wechat-format
  3. NeuraPress       ⭐  1,814  https://github.com/tianyaxiang/neurapress

用法示例
--------
  from skills.wechat_typesetting_skill import WeChatTypesettingSkill

  skill = WeChatTypesettingSkill()
  html = skill.convert("# 标题\\n\\n正文内容")
  print(html)

  # 使用自定义主题色
  skill = WeChatTypesettingSkill(theme_color="#1a73e8")
  html = skill.convert(markdown_text)
"""

import re
import textwrap
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# 主题配置
# ---------------------------------------------------------------------------

@dataclass
class WeChatTheme:
    """排版主题参数。"""

    theme_color: str = "#1E6FBB"            # 主题色（标题、强调色）
    text_color: str = "#333333"             # 正文颜色
    quote_bg: str = "#f5f5f5"               # 引用块背景
    quote_border: str = "#1E6FBB"           # 引用块左边框色
    code_bg: str = "#f0f0f0"               # 行内代码背景
    code_block_bg: str = "#2d2d2d"          # 代码块背景
    code_block_color: str = "#f8f8f2"       # 代码块文字色
    font_family: str = (
        "-apple-system, BlinkMacSystemFont, 'Helvetica Neue', "
        "Arial, 'PingFang SC', 'Hiragino Sans GB', "
        "'Microsoft YaHei', sans-serif"
    )
    line_height: str = "1.75"
    font_size: str = "15px"


# ---------------------------------------------------------------------------
# 核心转换器
# ---------------------------------------------------------------------------

class WeChatTypesettingSkill:
    """
    将 Markdown 文本转换为微信公众号兼容的内联样式 HTML。

    微信公众号编辑器不支持外部 CSS，所有样式必须内联。
    本 Skill 模仿 doocs/md 与 wechat-format 的核心排版逻辑。
    """

    # 参考工具注册表（按 ⭐ 降序）
    TOOLS_REGISTRY = [
        {
            "rank": 1,
            "stars": 13016,
            "name": "doocs/md",
            "url": "https://github.com/doocs/md",
            "description": "WeChat Markdown Editor | 多主题、AI助手、多图床",
            "updated": "2026-07",
        },
        {
            "rank": 2,
            "stars": 4540,
            "name": "lyricat/wechat-format",
            "url": "https://github.com/lyricat/wechat-format",
            "description": "转换 Markdown 到微信特制 HTML，轻量极简",
            "updated": "2026-07",
        },
        {
            "rank": 3,
            "stars": 1814,
            "name": "tianyaxiang/neurapress",
            "url": "https://github.com/tianyaxiang/neurapress",
            "description": "现代化编辑器，集成 DeepSeek AI，响应式设计",
            "updated": "2026-06",
        },
        {
            "rank": 4,
            "stars": 206,
            "name": "xueyc1f/turbopush-website",
            "url": "https://github.com/xueyc1f/turbopush-website",
            "description": "多平台一键发布、定时发布、数据分析",
            "updated": "2026-07",
        },
        {
            "rank": 5,
            "stars": 150,
            "name": "mengjian-github/lark-to-markdown",
            "url": "https://github.com/mengjian-github/lark-to-markdown",
            "description": "飞书文档 → 微信公众号编辑器，完美转换图片/表格",
            "updated": "2026-05",
        },
        {
            "rank": 6,
            "stars": 136,
            "name": "MuGuiLin/wxEditor",
            "url": "https://github.com/MuGuiLin/wxEditor",
            "description": "全功能富文本公众号编辑器，基于 UEditor 二次开发",
            "updated": "2025",
        },
        {
            "rank": 7,
            "stars": 75,
            "name": "sleepy-zone/woocs",
            "url": "https://github.com/sleepy-zone/woocs",
            "description": "基于 doocs/md 的 Electron 桌面客户端",
            "updated": "2026-06",
        },
        {
            "rank": 8,
            "stars": 7,
            "name": "italks/md-wechat",
            "url": "https://github.com/italks/md-wechat",
            "description": "CLI 批量排版 + OpenClaw Skill 接入，支持 Mermaid/公式",
            "updated": "2026-06",
        },
    ]

    def __init__(self, theme: Optional[WeChatTheme] = None, theme_color: Optional[str] = None):
        """
        Parameters
        ----------
        theme:       完整主题对象（优先使用）。
        theme_color: 快捷设置主题色（会覆盖 theme.theme_color）。
        """
        self.theme = theme or WeChatTheme()
        if theme_color:
            self.theme.theme_color = theme_color
            self.theme.quote_border = theme_color

    # ------------------------------------------------------------------
    # 公开接口
    # ------------------------------------------------------------------

    def convert(self, markdown: str) -> str:
        """
        将 Markdown 文本转换为微信公众号兼容的 HTML 字符串。

        Parameters
        ----------
        markdown: 标准 Markdown 文本。

        Returns
        -------
        str: 带内联样式的 HTML，可直接粘贴进微信公众号后台。
        """
        text = textwrap.dedent(markdown).strip()
        text = self._convert_headings(text)
        text = self._convert_code_blocks(text)
        text = self._convert_blockquotes(text)
        text = self._convert_horizontal_rules(text)
        text = self._convert_unordered_lists(text)
        text = self._convert_ordered_lists(text)
        text = self._convert_bold(text)
        text = self._convert_italic(text)
        text = self._convert_inline_code(text)
        text = self._convert_links(text)
        text = self._convert_images(text)
        text = self._convert_paragraphs(text)
        return self._wrap_section(text)

    def list_tools(self) -> str:
        """返回工具清单的 Markdown 格式字符串（按 ⭐ 降序）。"""
        lines = [
            "## 公众号编辑与排版工具（按 ⭐ 排序）\n",
            f"{'排名':<4} {'⭐ Stars':<10} {'工具名称':<35} 描述",
            "-" * 90,
        ]
        for tool in self.TOOLS_REGISTRY:
            lines.append(
                f"{tool['rank']:<4} {tool['stars']:<10,} {tool['name']:<35} {tool['description']}"
            )
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # 内部转换方法
    # ------------------------------------------------------------------

    def _s(self, **kwargs) -> str:
        """将 CSS 键值对合并为内联 style 字符串。"""
        return "; ".join(f"{k.replace('_', '-')}: {v}" for k, v in kwargs.items())

    def _wrap_section(self, html: str) -> str:
        style = self._s(
            font_family=self.theme.font_family,
            font_size=self.theme.font_size,
            line_height=self.theme.line_height,
            color=self.theme.text_color,
            word_break="break-word",
            max_width="677px",
            margin="0 auto",
            padding="20px 16px",
        )
        return f'<section style="{style}">\n{html}\n</section>'

    def _convert_headings(self, text: str) -> str:
        t = self.theme

        def h1(m):
            style = self._s(
                font_size="22px",
                font_weight="bold",
                color=t.theme_color,
                border_bottom=f"2px solid {t.theme_color}",
                padding_bottom="8px",
                margin="24px 0 16px",
                line_height="1.4",
            )
            return f'<h1 style="{style}">{m.group(1).strip()}</h1>'

        def h2(m):
            style = self._s(
                font_size="19px",
                font_weight="bold",
                color=t.theme_color,
                border_left=f"4px solid {t.theme_color}",
                padding_left="10px",
                margin="20px 0 12px",
                line_height="1.4",
            )
            return f'<h2 style="{style}">{m.group(1).strip()}</h2>'

        def h3(m):
            style = self._s(
                font_size="17px",
                font_weight="bold",
                color=t.theme_color,
                margin="16px 0 10px",
                line_height="1.4",
            )
            return f'<h3 style="{style}">{m.group(1).strip()}</h3>'

        def h4(m):
            style = self._s(
                font_size="16px",
                font_weight="bold",
                color=t.text_color,
                margin="14px 0 8px",
            )
            return f'<h4 style="{style}">{m.group(1).strip()}</h4>'

        text = re.sub(r"^#{1}\s+(.+)$", h1, text, flags=re.MULTILINE)
        text = re.sub(r"^#{2}\s+(.+)$", h2, text, flags=re.MULTILINE)
        text = re.sub(r"^#{3}\s+(.+)$", h3, text, flags=re.MULTILINE)
        text = re.sub(r"^#{4,}\s+(.+)$", h4, text, flags=re.MULTILINE)
        return text

    def _convert_code_blocks(self, text: str) -> str:
        t = self.theme

        def replace(m):
            lang = m.group(1) or ""
            code = m.group(2).strip()
            outer_style = self._s(
                background=t.code_block_bg,
                color=t.code_block_color,
                border_radius="6px",
                padding="16px",
                margin="16px 0",
                overflow_x="auto",
                font_size="13px",
                font_family="'Courier New', Consolas, monospace",
                line_height="1.6",
            )
            label = f'<span style="color:#999; font-size:11px;">{lang}</span>\n' if lang else ""
            safe = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            return f'<pre style="{outer_style}">{label}<code>{safe}</code></pre>'

        return re.sub(r"```(\w*)\n([\s\S]*?)```", replace, text)

    def _convert_blockquotes(self, text: str) -> str:
        t = self.theme

        def replace(m):
            content = re.sub(r"^>\s?", "", m.group(0), flags=re.MULTILINE).strip()
            style = self._s(
                border_left=f"4px solid {t.quote_border}",
                background=t.quote_bg,
                padding="12px 16px",
                margin="16px 0",
                color="#666",
                font_size="14px",
                border_radius="0 4px 4px 0",
            )
            return f'<blockquote style="{style}">{content}</blockquote>'

        return re.sub(r"(^>.*\n?)+", replace, text, flags=re.MULTILINE)

    def _convert_horizontal_rules(self, text: str) -> str:
        t = self.theme
        style = self._s(
            border="none",
            border_top=f"1px solid {t.quote_bg}",
            margin="24px 0",
        )
        return re.sub(r"^(-{3,}|\*{3,}|_{3,})$", f'<hr style="{style}">', text, flags=re.MULTILINE)

    def _convert_unordered_lists(self, text: str) -> str:
        t = self.theme

        def replace_block(m):
            items_raw = m.group(0).strip().split("\n")
            items_html = []
            for item in items_raw:
                content = re.sub(r"^[-*+]\s+", "", item.strip())
                li_style = self._s(margin="6px 0", line_height=t.line_height)
                items_html.append(f'<li style="{li_style}">{content}</li>')
            ul_style = self._s(
                padding_left="20px",
                margin="12px 0",
                color=t.text_color,
            )
            return f'<ul style="{ul_style}">\n' + "\n".join(items_html) + "\n</ul>"

        return re.sub(r"(^[-*+] .+\n?)+", replace_block, text, flags=re.MULTILINE)

    def _convert_ordered_lists(self, text: str) -> str:
        t = self.theme

        def replace_block(m):
            items_raw = m.group(0).strip().split("\n")
            items_html = []
            for item in items_raw:
                content = re.sub(r"^\d+\.\s+", "", item.strip())
                li_style = self._s(margin="6px 0", line_height=t.line_height)
                items_html.append(f'<li style="{li_style}">{content}</li>')
            ol_style = self._s(
                padding_left="20px",
                margin="12px 0",
                color=t.text_color,
            )
            return f'<ol style="{ol_style}">\n' + "\n".join(items_html) + "\n</ol>"

        return re.sub(r"(^\d+\. .+\n?)+", replace_block, text, flags=re.MULTILINE)

    def _convert_bold(self, text: str) -> str:
        t = self.theme
        style = self._s(font_weight="bold", color=t.theme_color)
        return re.sub(
            r"\*\*(.+?)\*\*|__(.+?)__",
            lambda m: f'<strong style="{style}">{m.group(1) or m.group(2)}</strong>',
            text,
        )

    def _convert_italic(self, text: str) -> str:
        return re.sub(
            r"\*(.+?)\*|_(.+?)_",
            lambda m: f'<em style="font-style: italic;">{m.group(1) or m.group(2)}</em>',
            text,
        )

    def _convert_inline_code(self, text: str) -> str:
        t = self.theme
        style = self._s(
            background=t.code_bg,
            color="#c7254e",
            padding="2px 5px",
            border_radius="3px",
            font_family="'Courier New', Consolas, monospace",
            font_size="0.9em",
        )
        return re.sub(
            r"`([^`]+)`",
            lambda m: f'<code style="{style}">{m.group(1)}</code>',
            text,
        )

    def _convert_links(self, text: str) -> str:
        t = self.theme
        style = self._s(color=t.theme_color, text_decoration="none", border_bottom=f"1px solid {t.theme_color}")
        return re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            lambda m: f'<a href="{m.group(2)}" style="{style}">{m.group(1)}</a>',
            text,
        )

    def _convert_images(self, text: str) -> str:
        img_style = self._s(max_width="100%", height="auto", display="block", margin="16px auto", border_radius="4px")
        return re.sub(
            r"!\[([^\]]*)\]\(([^)]+)\)",
            lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}" style="{img_style}">',
            text,
        )

    def _convert_paragraphs(self, text: str) -> str:
        t = self.theme
        p_style = self._s(
            margin="12px 0",
            line_height=t.line_height,
            color=t.text_color,
            font_size=t.font_size,
            text_align="justify",
        )
        lines = text.split("\n")
        result = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            if line.startswith("<"):
                result.append(line)
            else:
                result.append(f'<p style="{p_style}">{line}</p>')
            i += 1
        return "\n".join(result)


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="公众号编辑与排版 Skill — 将 Markdown 转换为微信兼容 HTML"
    )
    parser.add_argument("input", nargs="?", help="Markdown 文件路径（默认读取 stdin）")
    parser.add_argument("-o", "--output", help="输出 HTML 文件路径（默认输出到 stdout）")
    parser.add_argument("--color", default="#1E6FBB", help="主题色（十六进制，默认 #1E6FBB）")
    parser.add_argument("--list-tools", action="store_true", help="列出所有推荐工具（按 ⭐ 排序）")
    args = parser.parse_args()

    skill = WeChatTypesettingSkill(theme_color=args.color)

    if args.list_tools:
        print(skill.list_tools())
        sys.exit(0)

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            md = f.read()
    else:
        md = sys.stdin.read()

    html_output = skill.convert(md)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"✅ 已输出到 {args.output}")
    else:
        print(html_output)
