from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "sk-74087c072d48405bad3cdbb5ae910fd1")
        self.openai_api_base: str = os.getenv("OPENAI_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "deepseek-v3")
        
        self.milvus_host: str = os.getenv("MILVUS_HOST", "localhost")
        self.milvus_port: int = int(os.getenv("MILVUS_PORT", "19530"))
        
        self.boss_zhipin_api_key: str = os.getenv("BOSS_ZHIPIN_API_KEY", "")
        
        self.langchain_tracing_v2: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
        self.langchain_api_key: str = os.getenv("LANGCHAIN_API_KEY", "")
        self.langchain_project: str = os.getenv("LANGCHAIN_PROJECT", "campus-recruitment-assistant")
        
        self.secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
        self.algorithm: str = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
