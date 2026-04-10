from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from core.base_agent import BaseAgent


class DemandAnalysisAgent(BaseAgent):
    def get_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """你是一位专业的校招需求分析专家，擅长帮助学生分析自己的求职需求和职业规划。
请根据学生提供的信息，分析其：
1. 个人背景（学历、专业、成绩、技能等）
2. 求职意向（目标行业、岗位、城市、薪资期望等）
3. 核心竞争力和短板
4. 职业发展建议

请用结构化的方式输出分析结果。"""),
            ("user", "{user_input}")
        ])

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_input = input_data.get("user_input", "")
        context = input_data.get("context", {})
        
        result = self._invoke_llm({
            "user_input": user_input
        })
        
        return {
            "agent": "demand_analysis",
            "result": result,
            "context": {**context, "demand_analysis": result}
        }
