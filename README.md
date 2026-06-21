# 📚 Google Gemini 调研报告生成器 - 完整使用指南

## 📋 项目概述

这是一套基于Google Gemini API的智能调研报告生成系统，支持生成符合**中国大学标准格式**的学位论文。可直接在Google Colab中运行，自动生成Word格式文档。

### 包含文件说明

| 文件名 | 功能描述 |
|--------|--------|
| `research_report_generator.py` | 基础版本 - 生成文本报告 |
| `research_report_with_charts.py` | 增强版本 - 含数据可视化图表 |
| `university_thesis_generator.py` | 学位论文版本 - 符合中国大学格式 |
| `gemini_thesis_to_word.py` | **推荐使用** - 支持Word导出 |
| `README.md` | 本文档 |

---

## 🚀 快速开始

### 方式一：Google Colab中运行（推荐）

#### 第1步：获取Gemini API密钥

1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 登录你的Google账户
3. 点击 "Get API key" → "Create API key in new project"
4. 复制生成的API密钥（保管好，不要泄露！）

#### 第2步���在Colab中运行

复制下面的代码到Google Colab的代码单元格中运行：

```python
# 1. 安装必需库
!pip install python-docx matplotlib numpy google-generativeai

# 2. 从GitHub克隆代码
!git clone https://github.com/Jerryfan2026/STA2026.git
cd STA2026

# 3. 导入模块
from gemini_thesis_to_word import UniversityThesisWordGenerator

# 4. 设置API密钥
API_KEY = "YOUR_GEMINI_API_KEY"  # 替换为你的API密钥

# 5. 创建生成器
generator = UniversityThesisWordGenerator(api_key=API_KEY)

# 6. 生成论文
thesis = generator.generate_complete_thesis(
    title="人工智能在医疗健康领域的应用研究",
    author="张三",
    school="北京大学",
    major="计算机学院 / 人工智能专业",
    advisor="李四教授",
    topic="人工智能在医疗健康中的应用",
    focus_areas=["AI诊断技术", "个性化治疗", "成本优化"],
    research_methods=["文献分析", "数据统计", "案例研究"],
    key_findings=["诊断准确率95%以上", "成本降低30%", "需要伦理规范"]
)

# 7. 保存为Word文档
generator.save_to_word("学位论文.docx")
print("✅ Word文档已生成！")
```

#### 第3步：下载Word文件

在Colab的左侧文件管理器中找到 `学位论文.docx` 文件，点击下载。

---

### 方式二：本地Python环境运行

#### 安装依赖

```bash
pip install python-docx matplotlib numpy google-generativeai
```

#### 编写脚本

```python
from gemini_thesis_to_word import UniversityThesisWordGenerator

API_KEY = "YOUR_GEMINI_API_KEY"

generator = UniversityThesisWordGenerator(api_key=API_KEY)

# 生成论文
thesis = generator.generate_complete_thesis(
    title="你的论文题目",
    author="你的名字",
    school="你的学校",
    major="你的专业",
    advisor="指导老师",
    topic="研究主题",
    focus_areas=["重点领域1", "重点领域2"],
    research_methods=["方法1", "方法2"],
    key_findings=["发现1", "发现2"]
)

# 保存
generator.save_to_word("输出文件名.docx")
```

---

## 📝 详细参数说明

### 必填参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `title` | 论文标题 | "AI在医疗中的应用研究" |
| `author` | 作者名字 | "张三" |
| `school` | 学校名称 | "北京大学" |
| `major` | 专业/学院 | "计算机学院/人工智能" |
| `advisor` | 指导老师 | "李四教授" |
| `topic` | 研究主题 | "人工智能应用前景" |

### 可选参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `focus_areas` | 研究重点领域（列表） | 自动生成 |
| `research_methods` | 研究方法（列表） | ["文献分析", "数据统计"] |
| `key_findings` | 关键发现（列表） | 自动生成 |
| `include_charts` | 是否包含图表 | True |
| `include_references` | 是否包含参考文献 | True |

---

## 📊 生成的报告结构

论文包含以下标准章节：

```
📄 学位论文结构
├── 🎓 封面
│   ├── 学校名称
│   ├── 论文题目
│   ├── 作者信息
│   ├── 指导老师
│   └── 完成日期
├── 📝 中文摘要
│   ├── 摘要正文（200-300字）
│   └── 关键词（5-8个）
├── 📝 英文摘要
│   ├── English Abstract
│   └── Keywords
├── 📋 目录
├── 1️⃣ 引言（Introduction）
│   ├── 研究背景
│   ├── 研究意义
│   ├── 国内外研究现状
│   └── 研究目标
├── 2️⃣ 文献综述（Literature Review）
│   ├── 理论基础
│   ├── 相关研究分析
│   ├── 存在的问题
│   └── 参考文献引用
├── 3️⃣ 研究方法（Methodology）
│   ├── 研究方法介绍
│   ├── 数据来源
│   ├── 数据处理过程
│   └── 科学性说明
├── 4️⃣ 分析讨论（Analysis & Discussion）
│   ├── 多维度分析
│   ├── 数据支撑
│   ├── 观点论证
│   └── 2-3个小节深入展开
├── 5️⃣ 结论与建议（Conclusions & Suggestions）
│   ├── 主要结论
│   ├── 实践意义
│   ├── 研究局限
│   ├── 改进建议
│   └── 未来研究方向
├── 📖 参考文献（References）
│   └── GB/T 7714-2015格式（15-20条）
├── 📊 附录与图表
│   ├── 趋势分析图
│   ├── 地区分布图
│   ├── 构成分析饼图
│   ├── 对比分析图
│   └── 热力分析图
└── 💌 致谢
```

---

## 🎨 Word文档格式特点

生成的Word文档包含：

✅ **专业排版**
- 标准的中文学位论文格式
- 清晰的章节标题层级
- 合理的行距和页边距

✅ **完整的结构**
- 自动生成目录
- 页码编号
- 页眉页脚

✅ **高质量内容**
- 由Gemini AI生成的学术文本
- 符合论文学术规范
- 准确的参考文献引用

✅ **数据可视化**
- 自动插入高质量图表
- 图表编号和标题
- 300dpi高清分辨率

✅ **自定义选项**
- 字体、大小可调
- 颜色方案可定制
- 支持添加页眉页脚

---

## 💡 使用示例

### 示例1：基础使用（最简单）

```python
from gemini_thesis_to_word import UniversityThesisWordGenerator

generator = UniversityThesisWordGenerator(api_key="你的API密钥")

thesis = generator.generate_complete_thesis(
    title="研究主题",
    author="你的名字",
    school="你的学校",
    major="你的专业",
    advisor="指导老师",
    topic="研究主题描述"
)

generator.save_to_word("论文.docx")
```

### 示例2：完整配置

```python
generator = UniversityThesisWordGenerator(api_key="你的API密钥")

thesis = generator.generate_complete_thesis(
    title="人工智能在医疗健康领域的应用研究",
    author="张三",
    school="北京大学",
    major="计算机学院 / 人工智能专业",
    advisor="李四教授",
    topic="AI在医疗诊断中的应用",
    focus_areas=[
        "AI诊断准确性",
        "个性化治疗方案",
        "医疗成本优化",
        "数据隐私保护"
    ],
    research_methods=[
        "文献分析法",
        "案例研究法",
        "数据统计法",
        "对比分析法"
    ],
    key_findings=[
        "诊断准确率达到95%以上",
        "治疗成本可降低30%",
        "个性化方案成为发展趋势",
        "需要完善伦理规范框架"
    ],
    include_charts=True,
    include_references=True
)

generator.save_to_word("学位论文_完整版.docx")
```

### 示例3：自定义Word格式

```python
generator = UniversityThesisWordGenerator(api_key="你的API密钥")

thesis = generator.generate_complete_thesis(...)

# 自定义保存选项
generator.save_to_word(
    filename="论文.docx",
    font_name="宋体",
    font_size=12,
    include_page_numbers=True,
    include_toc=True  # 生成目录
)
```

---

## 🔧 故障排除

### 问题1：API密钥无效

**错误信息：** `APIError: Invalid API key`

**解决方案：**
1. 确认从 https://aistudio.google.com/ 复制的API密钥正确
2. 确保密钥没有过期或被禁用
3. 检查网络连接

### 问题2：Colab中缺少依赖库

**错误信息：** `ModuleNotFoundError: No module named 'docx'`

**解决方案：**
```python
!pip install python-docx
```

### 问题3：文本生成超时

**错误信息：** `Timeout error from API`

**解决方案：**
- 检查网络连接
- 重新运行代码
- 如问题持续，缩减content长度

### 问题4：中文显示乱码

**错误信息：** Word中显示方框或乱码

**解决方案：**
1. 在Word中选中所有文字（Ctrl+A）
2. 将字体改为"宋体"或"微软雅黑"
3. 重新保存文档

---

## 📚 常见问题

### Q: 可以修改生成的内容吗？
**A:** 完全可以！生成Word后可以直接在Word中编辑任何内容。

### Q: 如何添加自己的图表？
**A:** 
1. 生成Word后直接在Word中插入图片
2. 或修改Python代码中的`create_sample_charts()`方法

### Q: 支持其他语言吗？
**A:** 默认为中文。可修改提示词改为其他语言。

### Q: 可以生成PDF吗？
**A:** 可以在Word中另存为PDF，或使用`python-docx`扩展库

### Q: 参考文献格式是什么？
**A:** 采用GB/T 7714-2015标准（中文学位论文标准格式）

### Q: 可以批量生成多篇论文吗？
**A:** 可以，循环调用`generate_complete_thesis()`即可

---

## 📖 相关资源

- [Google Gemini API文档](https://ai.google.dev/)
- [python-docx文档](https://python-docx.readthedocs.io/)
- [GB/T 7714-2015参考文献标准](https://www.gb688.cn/bzgk/gb/newGbInfo?hcno=22DDBEE42A75E8BFD0B3951BA5F0D4C3)
- [中国学位论文格式要求](https://www.cnki.net/)

---

## 🤝 反馈与支持

如有问题或建议，请：
1. 在GitHub上提Issue
2. 发送邮件反馈
3. 查看代码注释获取更多帮助

---

## 📄 许可证

MIT License - 自由使用和修改

---

## ✨ 更新日志

### v1.0 (2026-06-21)
- ✅ 基础报告生成功能
- ✅ 图表可视化支持
- ✅ 中国大学格式支持
- ✅ Word导出功能

### 规划中的功能
- 📋 PDF直接导出
- 🎨 更多图表类型
- 🌍 多语言支持
- 📊 高级数据分析
- 🔐 云端存储支持

---

**最后更新：** 2026年6月21日  
**维护者：** Jerryfan2026  
**GitHub仓库：** https://github.com/Jerryfan2026/STA2026
