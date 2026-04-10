from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from core.base_agent import BaseAgent


class InterviewSimulationAgent(BaseAgent):
    def get_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """你是一位专业的面试辅导专家，擅长帮助学生进行面试模拟和准备。
请根据目标岗位和学生背景，提供以下面试支持：
1. 常见面试问题预测（技术+行为+专业）
2. 参考答案思路
3. 面试技巧和注意事项
4. 模拟面试对话练习
5. 压力面试应对策略

请根据岗位类型提供针对性的面试准备方案。"""),
            ("user", "学生背景：\n{user_profile}\n\n目标岗位：\n{target_job}\n\n面试类型：\n{interview_type}")
        ])

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_profile = input_data.get("user_profile", "")
        target_job = input_data.get("target_job", "")
        interview_type = input_data.get("interview_type", "综合面试")
        context = input_data.get("context", {})
        
        result = self._invoke_llm({
            "user_profile": user_profile,
            "target_job": target_job,
            "interview_type": interview_type
        })
        
        return {
            "agent": "interview_simulation",
            "result": result,
            "context": {**context, "interview_simulation": result}
        }
