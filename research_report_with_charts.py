"""
Google Gemini 调研报告生成器（含数据图表）
可在 Google Colab 和 Canvas 中直接运行
支持生成图表、统计数据和可视化分析
"""

import google.generativeai as genai
from typing import Optional, List, Dict
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np
from datetime import datetime
import io
import base64


class ResearchReportWithCharts:
    """带图表的Google Gemini调研报告生成器"""
    
    def __init__(self, api_key: str, language: str = "zh"):
        """
        初始化报告生成器
        
        Args:
            api_key: Google Gemini API密钥
            language: 语言设置 ('zh' 为中文, 'en' 为英文)
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.report_sections = {}
        self.charts = []
        self.language = language
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def generate_summary(self, topic: str) -> str:
        """生成报告摘要"""
        prompt = f"""请为以下主题生成一份简洁的研究报告摘要（150-200字）：
        
主题：{topic}

要求：
- 概括主要研究内容
- 突出关键发现
- 简明扼要，适合作为报告引言"""
        
        response = self.model.generate_content(prompt)
        summary = response.text
        self.report_sections['summary'] = summary
        return summary
    
    def generate_background(self, topic: str) -> str:
        """生成报告背景部分"""
        prompt = f"""请为以下主题生成详细的研究背景部分（300-400字）：

主题：{topic}

要求：
- 介绍主题的历史背景
- 说明为什么这个主题重要
- 阐述当前相关的发展趋势
- 引出研究的必要性"""
        
        response = self.model.generate_content(prompt)
        background = response.text
        self.report_sections['background'] = background
        return background
    
    def generate_analysis(self, topic: str, focus_areas: Optional[list] = None) -> str:
        """生成报告分析部分"""
        focus_text = ""
        if focus_areas:
            focus_text = f"\n重点分析领域：{', '.join(focus_areas)}"
        
        prompt = f"""请为以下主题生成深入的分析部分（400-500字）：

主题：{topic}{focus_text}

要求：
- 多角度分析该主题
- 列举主要观点和证据
- 讨论优势、劣势、机遇和挑战
- 提供数据支持（如无实际数据，可用合理假设）
- 组织结构清晰，便于理解"""
        
        response = self.model.generate_content(prompt)
        analysis = response.text
        self.report_sections['analysis'] = analysis
        return analysis
    
    def generate_conclusion(self, topic: str, key_findings: Optional[list] = None) -> str:
        """生成报告结论部分"""
        findings_text = ""
        if key_findings:
            findings_text = f"\n已识别的关键发现：\n" + "\n".join([f"- {finding}" for finding in key_findings])
        
        prompt = f"""请为以下主题生成有力的结论部分（250-300字）：

主题：{topic}{findings_text}

要求：
- 总结主要研究发现
- 阐述研究的实际意义
- 提出建议或未来展望
- 突出创新之处或重要发现
- 结构清晰，有力有据"""
        
        response = self.model.generate_content(prompt)
        conclusion = response.text
        self.report_sections['conclusion'] = conclusion
        return conclusion
    
    def create_trend_chart(self, title: str, years: List[int], values: List[float], 
                          ylabel: str = "增长率 (%)", filename: str = None) -> str:
        """
        创建趋势折线图
        
        Args:
            title: 图表标题
            years: 年份列表
            values: 数值列表
            ylabel: Y轴标签
            filename: 保存文件名
            
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#ffffff')
        
        # 绘制折线图
        line = ax.plot(years, values, marker='o', linewidth=3, markersize=10, 
                       color=self.colors[0], label='增长趋势')
        
        # 添加数值标签
        for year, value in zip(years, values):
            ax.text(year, value + 2, f'{value}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # 设置样式
        ax.set_xlabel('年份', fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(0, max(values) + 10)
        
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            self.charts.append(filename)
            return filename
        else:
            return fig
    
    def create_bar_chart(self, title: str, categories: List[str], values: List[float],
                        xlabel: str = "", ylabel: str = "数值", filename: str = None) -> str:
        """
        创建条形图
        
        Args:
            title: 图表标题
            categories: 类别列表
            values: 数值列表
            xlabel: X轴标签
            ylabel: Y轴标签
            filename: 保存文件名
            
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#ffffff')
        
        # 绘制柱状图
        bars = ax.bar(categories, values, color=self.colors[:len(categories)], 
                      edgecolor='black', linewidth=1.5, alpha=0.85)
        
        # 添加数值标签
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # 设置样式
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            self.charts.append(filename)
            return filename
        else:
            return fig
    
    def create_pie_chart(self, title: str, labels: List[str], sizes: List[float],
                        filename: str = None) -> str:
        """
        创建饼图
        
        Args:
            title: 图表标题
            labels: 标签列表
            sizes: 大小列表
            filename: 保存文件名
            
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor('#f8f9fa')
        
        # 绘制饼图
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                          colors=self.colors, startangle=90,
                                          textprops={'fontsize': 11, 'weight': 'bold'})
        
        # 美化自动百分比文本
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            self.charts.append(filename)
            return filename
        else:
            return fig
    
    def create_comparison_chart(self, title: str, categories: List[str], 
                               data_dict: Dict[str, List[float]], filename: str = None) -> str:
        """
        创建对比图（多组数据）
        
        Args:
            title: 图表标题
            categories: 类别列表
            data_dict: {数据组名: [数值列表]}
            filename: 保存文件名
            
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#ffffff')
        
        x = np.arange(len(categories))
        width = 0.25
        
        # 绘制多组柱状图
        for idx, (label, values) in enumerate(data_dict.items()):
            offset = (idx - len(data_dict)/2 + 0.5) * width
            bars = ax.bar(x + offset, values, width, label=label, 
                         color=self.colors[idx % len(self.colors)],
                         edgecolor='black', linewidth=1, alpha=0.85)
            
            # 添加数值标签
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.0f}', ha='center', va='bottom', fontsize=9)
        
        # 设置样式
        ax.set_xlabel('类别', fontsize=12, fontweight='bold')
        ax.set_ylabel('数值', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            self.charts.append(filename)
            return filename
        else:
            return fig
    
    def create_heatmap(self, title: str, data: np.ndarray, x_labels: List[str],
                      y_labels: List[str], filename: str = None) -> str:
        """
        创建热力图
        
        Args:
            title: 图表标题
            data: 数据矩阵
            x_labels: X轴标签
            y_labels: Y轴标签
            filename: 保存文件名
            
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor('#f8f9fa')
        
        im = ax.imshow(data, cmap='RdYlGn', aspect='auto')
        
        # 设置标签
        ax.set_xticks(np.arange(len(x_labels)))
        ax.set_yticks(np.arange(len(y_labels)))
        ax.set_xticklabels(x_labels)
        ax.set_yticklabels(y_labels)
        
        # 添加数值标签
        for i in range(len(y_labels)):
            for j in range(len(x_labels)):
                text = ax.text(j, i, f'{data[i, j]:.0f}',
                             ha="center", va="center", color="black", fontweight='bold')
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        fig.colorbar(im, ax=ax, label='数值范围')
        
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            self.charts.append(filename)
            return filename
        else:
            return fig
    
    def generate_complete_report(self, topic: str, focus_areas: Optional[list] = None,
                                key_findings: Optional[list] = None, include_charts: bool = True) -> str:
        """
        生成完整的调研报告（含图表）
        
        Args:
            topic: 调研主题
            focus_areas: 重点分析领域
            key_findings: 关键发现
            include_charts: 是否包含图表
            
        Returns:
            完整报告文本
        """
        print(f"🚀 开始生成『{topic}』的调研报告...\n")
        
        # 生成各部分内容
        print("📝 正在生成摘要...")
        summary = self.generate_summary(topic)
        print("✓ 摘要完成\n")
        
        print("📚 正在生成背景...")
        background = self.generate_background(topic)
        print("✓ 背景完成\n")
        
        print("🔍 正在生成分析...")
        analysis = self.generate_analysis(topic, focus_areas)
        print("✓ 分析完成\n")
        
        print("💡 正在生成结论...")
        conclusion = self.generate_conclusion(topic, key_findings)
        print("✓ 结论完成\n")
        
        # 生成示例图表
        if include_charts:
            print("📊 正在生成数据图表...\n")
            self._generate_sample_charts(topic)
            print("✓ 图表生成完成\n")
        
        # 组合完整报告
        report = f"""
{'='*70}
                          调 研 报 告
{'='*70}
主题：{topic}
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}

【摘要 ABSTRACT】
{'-'*70}
{summary}

{'-'*70}

【背景 BACKGROUND】
{'-'*70}
{background}

{'-'*70}

【分析 ANALYSIS】
{'-'*70}
{analysis}

{'-'*70}

【结论 CONCLUSION】
{'-'*70}
{conclusion}

{'='*70}

【附录：图表列表】
"""
        if self.charts:
            for idx, chart_file in enumerate(self.charts, 1):
                report += f"\n图表 {idx}: {chart_file}"
        
        report += f"\n\n{'='*70}\n报告生成完毕\n{'='*70}\n"
        
        return report
    
    def _generate_sample_charts(self, topic: str):
        """生成示例图表"""
        
        # 示例1：趋势图
        print("  • 生成增长趋势图...")
        self.create_trend_chart(
            title=f"{topic} - 近5年增长趋势",
            years=[2019, 2020, 2021, 2022, 2023],
            values=[15, 28, 42, 65, 88],
            ylabel="市场规模增长率 (%)",
            filename="chart_1_trend.png"
        )
        plt.close()
        
        # 示例2：柱状图
        print("  • 生成地区对比图...")
        self.create_bar_chart(
            title=f"{topic} - 主要地区分布情况",
            categories=['北美', '欧洲', '亚洲', '其他地区'],
            values=[28, 22, 35, 15],
            ylabel="市场份额占比 (%)",
            filename="chart_2_region.png"
        )
        plt.close()
        
        # 示例3：饼图
        print("  • 生成构成分析图...")
        self.create_pie_chart(
            title=f"{topic} - 产业链构成分析",
            labels=['研发', '生产', '销售', '服务', '其他'],
            sizes=[25, 30, 25, 15, 5],
            filename="chart_3_composition.png"
        )
        plt.close()
        
        # 示例4：对比图
        print("  • 生成多维度对比图...")
        self.create_comparison_chart(
            title=f"{topic} - 国内外对比分析",
            categories=['技术水平', '市场规模', '投资额', '增长速度', '竞争力'],
            data_dict={
                '国内': [72, 65, 58, 85, 68],
                '国际': [88, 92, 78, 75, 90]
            },
            filename="chart_4_comparison.png"
        )
        plt.close()
        
        # 示例5：热力图
        print("  • 生成热力分析图...")
        heatmap_data = np.array([
            [8, 7, 6, 5, 4],
            [7, 9, 8, 6, 5],
            [6, 8, 9, 7, 6],
            [5, 6, 7, 8, 7],
            [4, 5, 6, 7, 9]
        ])
        self.create_heatmap(
            title=f"{topic} - 区域发展热力分布",
            data=heatmap_data,
            x_labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'],
            y_labels=['地区A', '地区B', '地区C', '地区D', '地区E'],
            filename="chart_5_heatmap.png"
        )
        plt.close()
    
    def save_report(self, report: str, filename: str = "research_report.txt"):
        """保存报告到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ 报告已保存到: {filename}")


# 使用示例
def main():
    """主函数"""
    
    # 设置API密钥
    API_KEY = "YOUR_GEMINI_API_KEY"  # 替换为你的API密钥
    
    # 创建报告生成器
    generator = ResearchReportWithCharts(api_key=API_KEY)
    
    # 定义研究主题
    topic = "人工智能在医疗健康中的应用前景"
    focus_areas = [
        "诊断准确性提升",
        "个性化治疗方案",
        "医疗成本优化",
        "数据隐私与安全"
    ]
    key_findings = [
        "AI可以提升诊断准确率至95%以上",
        "个性化治疗将成为未来医疗主流",
        "需要建立完善的数据保护机制"
    ]
    
    # 生成完整报告（包含图表）
    report = generator.generate_complete_report(
        topic=topic,
        focus_areas=focus_areas,
        key_findings=key_findings,
        include_charts=True
    )
    
    # 打印报告
    print(report)
    
    # 保存报告
    generator.save_report(report, filename="research_report_with_charts.txt")
    print("\n✨ 所有图表已保存为PNG文件，可在报告中引用！")


if __name__ == "__main__":
    main()
