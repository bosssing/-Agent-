from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from core.base_agent import BaseAgent


class JobMatchingAgent(BaseAgent):
    def get_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """你是一位专业的岗位匹配专家，擅长根据学生的背景和需求，匹配最适合的校招岗位。
请根据提供的信息：
1. 分析岗位与学生的匹配度
2. 列出匹配的关键点
3. 提供投递建议
4. 推荐类似的岗位方向

请结合岗位信息和学生背景进行综合分析。"""),
            ("user", "学生背景：\n{user_profile}\n\n岗位信息：\n{job_info}")
        ])

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_profile = input_data.get("user_profile", "")
        job_info = input_data.get("job_info", "")
        context = input_data.get("context", {})
        
        result = self._invoke_llm({
            "user_profile": user_profile,
            "job_info": job_info
        })
        
        return {
            "agent": "job_matching",
            "result": result,
            "context": {**context, "job_matching": result}
        }
