from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from .vector_store import VectorStore
from utils.config import get_settings


class RAGEngine:
    def __init__(self, vector_store: VectorStore = None, llm=None):
        settings = get_settings()
        self.vector_store = vector_store or VectorStore()
        if llm is None:
            self.llm = ChatOpenAI(
                model=settings.openai_model,
                openai_api_base=settings.openai_api_base,
                openai_api_key=settings.openai_api_key,
                temperature=0
            )
        else:
            self.llm = llm
        self.output_parser = StrOutputParser()

    def query(self, question: str) -> Dict[str, Any]:
        relevant_docs = self.vector_store.similarity_search(question)
        
        context = self._format_documents(relevant_docs)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一位专业的校招顾问。请基于以下上下文信息回答用户的问题。
如果上下文中没有相关信息，请基于你的专业知识回答，但请注明这是基于通用知识的建议。

上下文信息：
{context}"""),
            ("user", "{question}")
        ])
        
        chain = prompt | self.llm | self.output_parser
        
        answer = chain.invoke({
            "context": context,
            "question": question
        })
        
        return {
            "answer": answer,
            "sources": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in relevant_docs
            ]
        }

    def _format_documents(self, documents: List[Document]) -> str:
        formatted = []
        for i, doc in enumerate(documents, 1):
            formatted.append(f"[来源{i}]\n{doc.page_content}\n")
        return "\n".join(formatted)

    def get_knowledge_context(self, question: str) -> str:
        relevant_docs = self.vector_store.similarity_search(question)
        return self._format_documents(relevant_docs)
