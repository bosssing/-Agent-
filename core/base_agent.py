from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.config import get_settings


class BaseAgent(ABC):
    def __init__(self, llm: Optional[ChatOpenAI] = None):
        settings = get_settings()
        self.llm = llm or ChatOpenAI(
            model=settings.openai_model,
            base_url=settings.openai_api_base,
            api_key=settings.openai_api_key,
            temperature=0.7
        )
        self.output_parser = StrOutputParser()

    @abstractmethod
    def get_prompt_template(self) -> ChatPromptTemplate:
        pass

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def _invoke_llm(self, prompt_kwargs: Dict[str, Any]) -> str:
        prompt = self.get_prompt_template()
        chain = prompt | self.llm | self.output_parser
        return chain.invoke(prompt_kwargs)
