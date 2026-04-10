from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from core.base_agent import BaseAgent


class KnowledgeBaseAgent(BaseAgent):
    def get_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """你是一位专业的校招知识库问答专家，擅长回答校招相关的各类问题。
请结合知识库内容，回答用户的问题。如果知识库中没有相关信息，请基于你的专业知识进行回答，但请注明这是基于通用知识的建议。

回答要求：
1. 准确、专业、有针对性
2. 提供实用的建议和解决方案
3. 必要时提供相关资源或链接方向
4. 避免虚假信息和猜测"""),
            ("user", "用户问题：{question}\n\n知识库相关内容：{knowledge_context}")
        ])

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        question = input_data.get("question", "")
        knowledge_context = input_data.get("knowledge_context", "无相关知识库内容")
        context = input_data.get("context", {})
        
        result = self._invoke_llm({
            "question": question,
            "knowledge_context": knowledge_context
        })
        
        return {
            "agent": "knowledge_base",
            "result": result,
            "context": {**context, "knowledge_base": result}
        }
