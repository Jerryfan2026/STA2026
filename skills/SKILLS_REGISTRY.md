# 🗂️ 公众号编辑与排版 Skill 清单

> 按 GitHub ⭐ 数量降序排列，最后更新：2026-07-14

---

## 📋 工具清单

| 排名 | ⭐ Stars | 工具名称 | 仓库地址 | 核心能力 | 语言/平台 | 最后更新 |
|------|---------|---------|---------|---------|---------|---------|
| 1 | 13,016 | **doocs/md** | [doocs/md](https://github.com/doocs/md) | Markdown → 微信 HTML；多主题；AI 助手；多图床；内容管理 | TypeScript / Vue3 | 2026-07 |
| 2 | 4,540 | **wechat-format** | [lyricat/wechat-format](https://github.com/lyricat/wechat-format) | Markdown 转微信特制 HTML；支持代码高亮、LaTeX 公式 | JavaScript | 2026-07 |
| 3 | 1,814 | **NeuraPress** | [tianyaxiang/neurapress](https://github.com/tianyaxiang/neurapress) | 现代化 Markdown 编辑器；DeepSeek 集成；响应式/移动端 | Vue | 2026-06 |
| 4 | 206 | **TurboPush** | [xueyc1f/turbopush-website](https://github.com/xueyc1f/turbopush-website) | 多平台一键发布；定时发布；数据分析 | TypeScript | 2026-07 |
| 5 | 150 | **lark-to-markdown** | [mengjian-github/lark-to-markdown](https://github.com/mengjian-github/lark-to-markdown) | 飞书文档 → 微信公众号编辑器；图片/表格/代码块完美转换 | TypeScript | 2026-05 |
| 6 | 136 | **wxEditor** | [MuGuiLin/wxEditor](https://github.com/MuGuiLin/wxEditor) | 全功能富文本公众号编辑器（基于百度 UEditor 二次开发） | JavaScript | 2025 |
| 7 | 75 | **Woocs** | [sleepy-zone/woocs](https://github.com/sleepy-zone/woocs) | 基于 doocs/md 的桌面客户端（Electron） | Vue / Electron | 2026-06 |
| 8 | 7 | **md-wechat** | [italks/md-wechat](https://github.com/italks/md-wechat) | 命令行批量排版；OpenClaw Skill；Mermaid/数学公式 | HTML / Python | 2026-06 |

---

## 🔍 各工具详细说明

### 1. doocs/md ⭐ 13,016（**首选**）
- **在线体验**：<https://doocs.github.io/md/>
- **亮点**：
  - 完整支持 GFM Markdown 语法
  - 内置 AI 助手（支持多种 LLM）
  - 多图床（GitHub / 腾讯云 / 阿里云 / Gitee）
  - 自定义 CSS 主题
  - 数学公式（KaTeX）、Mermaid 流程图、代码高亮
  - 一键复制到公众号编辑器
- **适合**：技术文章、图文并茂的深度内容

### 2. lyricat/wechat-format ⭐ 4,540
- **在线体验**：<https://lab.lyric.im/wxformat/>
- **亮点**：
  - 轻量极简，转换速度快
  - 支持自定义颜色主题
  - 代码高亮、引用块美化
  - 导出微信专属 HTML（可直接粘贴进后台）
- **适合**：快速排版、技术博客迁移

### 3. tianyaxiang/neurapress ⭐ 1,814
- **在线体验**：<https://neurapress.vercel.app/>
- **亮点**：
  - 集成 DeepSeek/OpenAI AI 写作辅助
  - 移动端响应式设计
  - 多种预设排版主题
  - 实时双栏预览
- **适合**：需要 AI 辅助写作的内容创作者

### 4. xueyc1f/turbopush-website ⭐ 206
- **亮点**：
  - 一键同步发布到微信公众号 + 其他平台
  - 定时发布排程
  - 多账号管理
  - 内容数据分析
- **适合**：多平台运营、矩阵号管理

### 5. mengjian-github/lark-to-markdown ⭐ 150
- **亮点**：
  - 飞书/Notion 文档一键迁移到公众号
  - 图片自动上传到图床
  - 完美还原表格、代码块格式
- **适合**：使用飞书/Notion 协作写作的团队

### 6. MuGuiLin/wxEditor ⭐ 136
- **亮点**：
  - 所见即所得富文本编辑器
  - 素材库管理
  - 前后端完整方案
- **适合**：需要私有化部署的团队

### 7. sleepy-zone/woocs ⭐ 75
- **亮点**：
  - 基于 doocs/md 的 Electron 桌面应用
  - 离线可用
  - 本地文件管理
- **适合**：偏好桌面工具的用户

### 8. italks/md-wechat ⭐ 7
- **亮点**：
  - 命令行批量转换（CI/CD 友好）
  - 支持 OpenClaw Skill 接入
  - 样式配置提取与复用
- **适合**：开发者自动化排版流水线

---

## 🚀 推荐使用场景

| 场景 | 推荐工具 |
|------|---------|
| 日常图文排版 | doocs/md |
| 快速转换 Markdown | wechat-format |
| AI 辅助写作 | NeuraPress |
| 多平台发布 | TurboPush |
| 飞书迁移 | lark-to-markdown |
| 团队私有化部署 | wxEditor |
| 离线桌面使用 | Woocs |
| 自动化 CI/CD 排版 | md-wechat |

---

## 📌 本地 Python Skill

仓库内置了一个 Python 技能封装，见 [`wechat_typesetting_skill.py`](./wechat_typesetting_skill.py)。

该 Skill 提供：
- Markdown → 微信兼容 HTML 转换（无需外部服务）
- 内联样式注入（公众号不支持外部 CSS）
- 标题 / 代码块 / 引用块 / 列表 / 粗斜体 样式美化
- 自定义主题色
