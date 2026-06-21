"""
Google Gemini 调研报告生成器
可在 Google Colab 和 Canvas 中直接运行
"""

import google.generativeai as genai
from typing import Optional
import json


class ResearchReportGenerator:
    """基于Google Gemini的调研报告生成器"""
    
    def __init__(self, api_key: str):
        """
        初始化报告生成器
        
        Args:
            api_key: Google Gemini API密钥
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.report_sections = {}
    
    def generate_summary(self, topic: str) -> str:
        """
        生成报告摘要
        
        Args:
            topic: 调研主题
            
        Returns:
            摘要内容
        """
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
        """
        生成报告背景部分
        
        Args:
            topic: 调研主题
            
        Returns:
            背景内容
        """
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
        """
        生成报告分析部分
        
        Args:
            topic: 调研主题
            focus_areas: 重点分析领域列表（可选）
            
        Returns:
            分析内容
        """
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
        """
        生成报告结论部分
        
        Args:
            topic: 调研主题
            key_findings: 关键发现列表（可选）
            
        Returns:
            结论内容
        """
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
    
    def generate_complete_report(self, topic: str, focus_areas: Optional[list] = None, 
                                key_findings: Optional[list] = None) -> str:
        """
        生成完整的调研报告
        
        Args:
            topic: 调研主题
            focus_areas: 重点分析领域（可选）
            key_findings: 关键发现（可选）
            
        Returns:
            完整报告文本
        """
        print(f"开始生成『{topic}』的调研报告...\n")
        
        # 生成各部分
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
        
        # 组合完整报告
        report = f"""
{'='*60}
调研报告：{topic}
{'='*60}

【摘要】
{summary}

{'-'*60}

【背景】
{background}

{'-'*60}

【分析】
{analysis}

{'-'*60}

【结论】
{conclusion}

{'='*60}
"""
        return report
    
    def save_report(self, report: str, filename: str = "research_report.txt"):
        """
        保存报告到文件
        
        Args:
            report: 报告内容
            filename: 保存文件名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ 报告已保存到: {filename}")


def main():
    """主函数 - 使用示例"""
    
    # 1. 设置API密钥 (在Colab中，可以使用userdata.get('GEMINI_API_KEY'))
    API_KEY = "YOUR_GEMINI_API_KEY"  # 替换为你的Gemini API密钥
    
    # 2. 创建报告生成器
    generator = ResearchReportGenerator(api_key=API_KEY)
    
    # 3. 定义研究主题和参数
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
    
    # 4. 生成完整报告
    report = generator.generate_complete_report(
        topic=topic,
        focus_areas=focus_areas,
        key_findings=key_findings
    )
    
    # 5. 打印报告
    print(report)
    
    # 6. 保存报告
    generator.save_report(report, filename="research_report.txt")


if __name__ == "__main__":
    main()
