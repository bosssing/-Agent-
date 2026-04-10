from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from core.base_agent import BaseAgent


class ResumeOptimizationAgent(BaseAgent):
    def get_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """你是一位专业的简历优化专家，擅长帮助学生优化简历，提高校招成功率。
请根据提供的简历内容和目标岗位，进行以下优化：
1. 简历结构优化建议
2. 内容亮点提炼
3. 关键词优化（匹配岗位JD）
4. 经历描述STAR法则优化
5. 整体改进建议

请提供具体的修改建议和优化后的简历版本。"""),
            ("user", "原始简历：\n{resume_content}\n\n目标岗位：\n{target_job}")
        ])

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        resume_content = input_data.get("resume_content", "")
        target_job = input_data.get("target_job", "")
        context = input_data.get("context", {})
        
        result = self._invoke_llm({
            "resume_content": resume_content,
            "target_job": target_job
        })
        
        return {
            "agent": "resume_optimization",
            "result": result,
            "context": {**context, "resume_optimization": result}
        }
