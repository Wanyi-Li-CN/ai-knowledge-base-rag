import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 数据库
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost:5432/knowledge_base")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    # 文件上传
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    
    # 向量检索
    TOP_K: int = 4
    SIMILARITY_THRESHOLD: float = 0.7

# 关键：必须创建 settings 实例
settings = Settings()