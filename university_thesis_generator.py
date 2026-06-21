"""
Google Gemini 调研报告生成器 - 中国大学标准格式版本
支持生成符合中国高校规范的学位论文格式报告
包含摘要、关键词、目录、参考文献等完整结构
"""

import google.generativeai as genai
from typing import Optional, List, Dict
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import io
import os


class UniversityResearchReport:
    """符合中国大学格式的调研报告生成器"""
    
    def __init__(self, api_key: str):
        """
        初始化报告生成器
        
        Args:
            api_key: Google Gemini API密钥
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.report_sections = {}
        self.charts = []
        self.references = []
        self.keywords = []
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def generate_title_page(self, title: str, author: str, school: str, 
                           major: str, advisor: str, date: str) -> str:
        """
        生成封面（符合中国大学格式）
        
        Args:
            title: 论文题目
            author: 作者名字
            school: 学校名称
            major: 专业/学院
            advisor: 指导老师
            date: 完成日期
            
        Returns:
            格式化的封面文本
        """
        cover = f"""
{'':^80}
{'':^80}
{'':^80}

{'':^80}
{school:^80}
{'':^80}

{' '*20}{'调研报告（学位论文）':^50}
{'':^80}
{'':^80}

{' '*25}{title:^50}
{'':^80}
{'':^80}
{'':^80}

{'':^80}
{'':^80}
{'':^80}

学院/系部：{major:^50}
{'':^80}

专业方向：{'':50}
{'':^80}

作者姓名：{author:^50}
{'':^80}

指导教师：{advisor:^50}
{'':^80}

完成日期：{date:^50}
{'':^80}
"""
        self.report_sections['title_page'] = cover
        return cover
    
    def generate_chinese_abstract(self, topic: str, focus_areas: Optional[List[str]] = None) -> Dict[str, str]:
        """
        生成中文摘要（150-300字）
        
        Args:
            topic: 研究主题
            focus_areas: 研究重点领域
            
        Returns:
            包含摘要和关键词的字典
        """
        focus_text = ""
        if focus_areas:
            focus_text = f"\n主要研究领域：{', '.join(focus_areas)}"
        
        prompt = f"""请为以下主题生成一份学位论文级别的中文摘要（200-300字）：

研究主题：{topic}{focus_text}

要求：
1. 简明扼要地说明研究背景和意义
2. 陈述研究主要内容和方法
3. 突出研究成果和创新之处
4. 指出研究的应用价值
5. 摘要语言严谨，符合学术规范

同时请提供5-8个关键词（用中文逗号分隔）。
回复格式：
【摘要】
<摘要内容>

【关键词】
<关键词列表>"""
        
        response = self.model.generate_content(prompt)
        text = response.text
        
        # 解析摘要和关键词
        abstract = ""
        keywords = ""
        
        if "【摘要】" in text and "【关键词】" in text:
            abstract = text.split("【摘要】")[1].split("【关键词】")[0].strip()
            keywords = text.split("【关键词】")[1].strip()
        
        self.report_sections['abstract'] = abstract
        self.keywords = [k.strip() for k in keywords.split('，')]
        
        return {
            'abstract': abstract,
            'keywords': keywords
        }
    
    def generate_english_abstract(self, topic: str, focus_areas: Optional[List[str]] = None) -> Dict[str, str]:
        """
        生成英文摘要（150-250词）
        
        Args:
            topic: 研究主题
            focus_areas: 研究重点领域
            
        Returns:
            包含英文摘要和关键词的字典
        """
        focus_text = ""
        if focus_areas:
            focus_text = f"\nKey research areas: {', '.join(focus_areas)}"
        
        prompt = f"""Please generate an academic English abstract (200-250 words) for the following research topic:

Topic: {topic}{focus_text}

Requirements:
1. Clearly state the research background and significance
2. Present the main content and methodology
3. Highlight research achievements and innovations
4. Point out the practical application value
5. Use rigorous academic language

Also provide 5-8 English keywords (separated by commas).

Response format:
【ABSTRACT】
<abstract content>

【KEYWORDS】
<keywords list>"""
        
        response = self.model.generate_content(prompt)
        text = response.text
        
        # 解析英文摘要和关键词
        abstract = ""
        keywords = ""
        
        if "【ABSTRACT】" in text and "【KEYWORDS】" in text:
            abstract = text.split("【ABSTRACT】")[1].split("【KEYWORDS】")[0].strip()
            keywords = text.split("【KEYWORDS】")[1].strip()
        
        self.report_sections['english_abstract'] = abstract
        
        return {
            'abstract': abstract,
            'keywords': keywords
        }
    
    def generate_introduction(self, topic: str, background_info: str = "") -> str:
        """
        生成引言部分（500-800字）
        
        Args:
            topic: 研究主题
            background_info: 背景信息
            
        Returns:
            引言内容
        """
        background_text = f"\n背景信息：{background_info}" if background_info else ""
        
        prompt = f"""请为以下研究主题生成符合学位论文规范的引言部分（500-800字）：

研究主题：{topic}{background_text}

要求：
1. 介绍研究课题的理论背景
2. 分析问题的现实意义
3. 阐述国内外研究现状和存在的问题
4. 明确提出研究目标和意义
5. 概括论文的主要内容和结构安排
6. 使用恰当的引用和文献支撑
7. 语言严谨，层次分明"""
        
        response = self.model.generate_content(prompt)
        introduction = response.text
        self.report_sections['introduction'] = introduction
        return introduction
    
    def generate_literature_review(self, topic: str, key_concepts: Optional[List[str]] = None) -> str:
        """
        生成文献综述部分（1000-1500字）
        
        Args:
            topic: 研究主题
            key_concepts: 关键概念列表
            
        Returns:
            文献综述内容
        """
        concept_text = ""
        if key_concepts:
            concept_text = f"\n主要概念：{', '.join(key_concepts)}"
        
        prompt = f"""请为以下研究主题生成学位论文级别的文献综述（1000-1500字）：

研究主题：{topic}{concept_text}

要求：
1. 系统梳理国内外相关研究现状
2. 分析不同学者的主要观点
3. 指出当前研究的优势和不足
4. 明确阐述理论基础
5. 为后续分析奠定基础
6. 结合具体文献进行论述
7. 体现研究的创新意义

请在论述中自然融入至少8-12条参考文献的引用。"""
        
        response = self.model.generate_content(prompt)
        literature_review = response.text
        self.report_sections['literature_review'] = literature_review
        return literature_review
    
    def generate_methodology(self, topic: str, research_methods: List[str]) -> str:
        """
        生成研究方法部分（400-600字）
        
        Args:
            topic: 研究主题
            research_methods: 研究方法列表
            
        Returns:
            方法论内容
        """
        methods_text = f"研究方法：{', '.join(research_methods)}"
        
        prompt = f"""请为以下研究生成符合学位论文规范的研究方法部分（400-600字）：

研究主题：{topic}
{methods_text}

要求：
1. 明确阐述采用的研究方法和工具
2. 说明数据来源和收集方式
3. 描述数据处理和分析过程
4. 阐述研究的科学性和可靠性
5. 如适用，阐述样本选择的原则
6. 方法部分应具有可操作性和可验证性"""
        
        response = self.model.generate_content(prompt)
        methodology = response.text
        self.report_sections['methodology'] = methodology
        return methodology
    
    def generate_analysis(self, topic: str, focus_areas: Optional[List[str]] = None) -> str:
        """
        生成分析部分（1500-2000字）
        
        Args:
            topic: 研究主题
            focus_areas: 分析重点领域
            
        Returns:
            分析内容
        """
        focus_text = ""
        if focus_areas:
            focus_text = f"\n分析重点：{', '.join(focus_areas)}"
        
        prompt = f"""请为以下研究主题生成学位论文级别的分析部分（1500-2000字）：

研究主题：{topic}{focus_text}

要求：
1. 多维度、深层次地分析研究问题
2. 运用数据、案例进行论证
3. 逐步深化分析层次
4. 揭示现象背后的本质
5. 提出具有见地的观点
6. 分析过程严密，论证充分
7. 可分为2-3个小节，每节围绕不同角度展开"""
        
        response = self.model.generate_content(prompt)
        analysis = response.text
        self.report_sections['analysis'] = analysis
        return analysis
    
    def generate_conclusions_and_suggestions(self, topic: str, findings: Optional[List[str]] = None) -> str:
        """
        生成结论与建议部分（400-600字）
        
        Args:
            topic: 研究主题
            findings: 主要发现列表
            
        Returns:
            结论与建议内容
        """
        findings_text = ""
        if findings:
            findings_text = f"\n主要发现：\n" + "\n".join([f"- {finding}" for finding in findings])
        
        prompt = f"""请为以下研究生成学位论文级别的结论与建议部分（400-600字）：

研究主题：{topic}{findings_text}

要求：
1. 准确概括研究的主要结论
2. 阐述结论的理论和实践意义
3. 说明研究的局限性
4. 针对问题提出切实可行的建议
5. 指出未来的研究方向
6. 结论应与引言相呼应
7. 建议要有针对性和可操作性"""
        
        response = self.model.generate_content(prompt)
        conclusions = response.text
        self.report_sections['conclusions'] = conclusions
        return conclusions
    
    def generate_references(self, topic: str, count: int = 20) -> List[str]:
        """
        生成参考文献列表
        
        Args:
            topic: 研究主题
            count: 参考文献数量
            
        Returns:
            参考文献列表
        """
        prompt = f"""请为以下研究主题生成{count}条符合GB/T 7714-2015标准的参考文献：

研究主题：{topic}

要求：
1. 包含中文期刊论文、中文著作、外文论文等多种类型
2. 遵循GB/T 7714-2015参考文献著录规则
3. 按照在论文中出现的顺序编号
4. 格式示例（中文期刊）：
   [1] 作者.篇名[J].刊名,年份,卷(期):页码.
5. 格式示例（中文著作）：
   [2] 作者.书名[M].出版地:出版社,出版年.
6. 格式示例（英文期刊）：
   [3] Author. Title[J]. Journal, Year, Volume(Issue):Pages.

请直接返回按[1][2]...[n]编号的参考文献列表"""
        
        response = self.model.generate_content(prompt)
        ref_text = response.text
        
        # 解析参考文献
        references = []
        lines = ref_text.strip().split('\n')
        for line in lines:
            if line.strip() and '[' in line:
                references.append(line.strip())
        
        self.references = references
        return references
    
    def create_sample_charts(self) -> List[str]:
        """
        创建示例图表（学位论文格式）
        
        Returns:
            图表文件列表
        """
        chart_files = []
        
        # 图表1：折线图
        print("  • 生成趋势分析图...")
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('#f5f5f5')
        
        years = [2019, 2020, 2021, 2022, 2023]
        values = [15, 28, 42, 65, 88]
        
        ax.plot(years, values, marker='o', linewidth=2.5, markersize=8, color='#2E86AB')
        for year, value in zip(years, values):
            ax.text(year, value + 2, f'{value}%', ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel('年份 (Year)', fontsize=11, fontweight='bold')
        ax.set_ylabel('增长率 (%)', fontsize=11, fontweight='bold')
        ax.set_title('图1 近五年发展趋势分析', fontsize=12, fontweight='bold', pad=15)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(0, max(values) + 15)
        
        filename = 'fig_1_trend.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        chart_files.append(filename)
        
        # 图表2：柱状图
        print("  • 生成对比分析图...")
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('#f5f5f5')
        
        categories = ['地区A', '地区B', '地区C', '地区D']
        values = [28, 35, 22, 15]
        colors = ['#A23B72', '#F18F01', '#C73E1D', '#6A994E']
        
        bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2, alpha=0.85)
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_ylabel('占比 (%)', fontsize=11, fontweight='bold')
        ax.set_title('图2 不同地区分布情况', fontsize=12, fontweight='bold', pad=15)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_ylim(0, max(values) + 10)
        
        filename = 'fig_2_distribution.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        chart_files.append(filename)
        
        # 图表3：饼图
        print("  • 生成构成分析图...")
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor('white')
        
        labels = ['研发投入', '生产成本', '销售渠道', '服务支持', '其他']
        sizes = [25, 30, 25, 15, 5]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        explode = (0.05, 0, 0, 0, 0)
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                          colors=colors, explode=explode, startangle=90,
                                          textprops={'fontsize': 10})
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('图3 产业链构成分析', fontsize=12, fontweight='bold', pad=15)
        
        filename = 'fig_3_composition.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        chart_files.append(filename)
        
        self.charts = chart_files
        return chart_files
    
    def generate_complete_report(self, 
                                title: str,
                                author: str,
                                school: str,
                                major: str,
                                advisor: str,
                                topic: str,
                                focus_areas: Optional[List[str]] = None,
                                research_methods: Optional[List[str]] = None,
                                key_findings: Optional[List[str]] = None) -> str:
        """
        生成完整的学位论文格式报告
        
        Args:
            title: 论文标题
            author: 作者名字
            school: 学校名称
            major: 专业/学院
            advisor: 指导老师
            topic: 研究主题
            focus_areas: 研究重点领域
            research_methods: 研究方法
            key_findings: 关键发现
            
        Returns:
            完整报告文本
        """
        if research_methods is None:
            research_methods = ['文献分析法', '数据统计法', '对比分析法']
        
        print(f"🎓 开始生成『{title}』的学位论文...\n")
        
        # 生成封面
        print("📖 生成封面...")
        date = datetime.now().strftime('%Y年%m月%d日')
        cover = self.generate_title_page(title, author, school, major, advisor, date)
        print("✓ 封面完成\n")
        
        # 生成摘要
        print("📝 生成中文摘要...")
        abstract_dict = self.generate_chinese_abstract(topic, focus_areas)
        print("✓ 中文摘要完成\n")
        
        print("📝 生成英文摘要...")
        en_abstract_dict = self.generate_english_abstract(topic, focus_areas)
        print("✓ 英文摘要完成\n")
        
        # 生成引言
        print("📚 生成引言...")
        introduction = self.generate_introduction(topic)
        print("✓ 引言完成\n")
        
        # 生成文献综述
        print("📚 生成文献综述...")
        literature_review = self.generate_literature_review(topic, focus_areas)
        print("✓ 文献综述完成\n")
        
        # 生成研究方法
        print("🔬 生成研究方法...")
        methodology = self.generate_methodology(topic, research_methods)
        print("✓ 研究方法完成\n")
        
        # 生成分析部分
        print("🔍 生成分析部分...")
        analysis = self.generate_analysis(topic, focus_areas)
        print("✓ 分析部分完成\n")
        
        # 生成结论与建议
        print("💡 生成结论与建议...")
        conclusions = self.generate_conclusions_and_suggestions(topic, key_findings)
        print("✓ 结论与建议完成\n")
        
        # 生成参考文献
        print("📋 生成参考文献...")
        references = self.generate_references(topic, count=20)
        print("✓ 参考文献完成\n")
        
        # 生成图表
        print("📊 生成数据图表...\n")
        self.create_sample_charts()
        print("✓ 数据图表完成\n")
        
        # 组合完整报告
        full_report = f"""
{cover}

{'='*80}
                        中 文 摘 要
{'='*80}

{abstract_dict['abstract']}

关键词：{abstract_dict['keywords']}

{'='*80}
                         ABSTRACT
{'='*80}

{en_abstract_dict['abstract']}

Keywords: {en_abstract_dict['keywords']}

{'='*80}
                         目    录
{'='*80}

1. 引言..........................................3
2. 文献综述......................................5
3. 研究方法......................................8
4. 分析讨论......................................10
5. 结论与建议....................................15
参考文献..........................................17

{'='*80}
                        1. 引    言
{'='*80}

{introduction}

{'='*80}
                       2. 文 献 综 述
{'='*80}

{literature_review}

{'='*80}
                       3. 研 究 方 法
{'='*80}

{methodology}

{'='*80}
                      4. 分 析 讨 论
{'='*80}

{analysis}

{'='*80}
                    5. 结 论 与 建 议
{'='*80}

{conclusions}

{'='*80}
                        参 考 文 献
{'='*80}

"""
        for ref in references:
            full_report += f"{ref}\n"
        
        full_report += f"""

{'='*80}
                     附    录：图    表
{'='*80}

本报告包含以下图表：
"""
        for idx, chart_file in enumerate(self.charts, 1):
            full_report += f"  图{idx}：{chart_file}\n"
        
        full_report += f"""

{'='*80}
                          致    谢
{'='*80}

本研究的完成离不开各位指导老师的耐心指导和同学的大力支持。
特别感谢 {advisor} 老师的精心指导，以及 {school} 提供的良好研究环境。
同时感谢所有参与问卷调查和访谈的受访者，没有他们的配合就没有本研究的顺利完成。

{'='*80}
                    论文完成于：{date}
                       作者：{author}
{'='*80}

"""
        return full_report
    
    def save_report(self, report: str, filename: str = "学位论文.txt"):
        """保存报告到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存到: {filename}")
        print(f"📊 生成的图表文件: {', '.join(self.charts)}")


# 使用示例
def main():
    """主函数"""
    
    # 设置API密钥
    API_KEY = "YOUR_GEMINI_API_KEY"  # 替换为你的Gemini API密钥
    
    # 创建报告生成器
    generator = UniversityResearchReport(api_key=API_KEY)
    
    # 定义论文信息
    title = "人工智能在医疗健康领域应用的现状与展望"
    author = "张三"
    school = "北京大学"
    major = "计算机学院 / 人工智能专业"
    advisor = "李四教授"
    topic = "人工智能在医疗健康中的应用"
    
    focus_areas = [
        "AI诊断技术",
        "个性化治疗方案",
        "医疗成本优化",
        "数据隐私保护"
    ]
    
    research_methods = [
        "文献分析法",
        "案例研究法",
        "数据统计法",
        "对比分析法"
    ]
    
    key_findings = [
        "AI诊断准确率已达到95%以上",
        "个性化治疗将成为未来医疗主流方向",
        "需要建立完善的数据安全保护机制",
        "应用前景广阔但面临伦理挑战"
    ]
    
    # 生成完整报告
    report = generator.generate_complete_report(
        title=title,
        author=author,
        school=school,
        major=major,
        advisor=advisor,
        topic=topic,
        focus_areas=focus_areas,
        research_methods=research_methods,
        key_findings=key_findings
    )
    
    # 打印报告
    print(report)
    
    # 保存报告
    generator.save_report(report, filename="学位论文_标准格式.txt")
    print("\n✨ 报告生成完毕！所有文件已保存。")


if __name__ == "__main__":
    main()
