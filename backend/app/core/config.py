import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 数据库
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost:5432/knowledge_base")
    
    # 大模型配置（DeepSeek）
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "deepseek-chat")
    
    # Embedding 配置（独立于大模型）
    EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "aliyun")
    EMBEDDING_API_KEY: str = os.getenv("EMBEDDING_API_KEY", "")
    EMBEDDING_BASE_URL: str = os.getenv("EMBEDDING_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-v3")
    
    # 文件上传
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE: int = 50 * 1024 * 1024
    
    # 向量检索
    TOP_K: int = 4
    SIMILARITY_THRESHOLD: float = 0.7

settings = Settings()