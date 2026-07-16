from app.core.config import settings
from app.services.rag.aliyun_embeddings import AliyunEmbeddings


def get_embeddings():
    """根据配置创建 Embedding 实例"""
    
    provider = settings.EMBEDDING_PROVIDER
    
    if provider == "aliyun":
        return AliyunEmbeddings(
            api_key=settings.EMBEDDING_API_KEY,
            model=settings.EMBEDDING_MODEL,
            base_url=settings.EMBEDDING_BASE_URL,
        )
    
    elif provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.EMBEDDING_API_KEY,
            base_url=settings.EMBEDDING_BASE_URL,
        )
    
    elif provider == "local":
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(
                model_name="BAAI/bge-large-zh-v1.5",
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )
        except ImportError:
            raise ImportError("请安装 sentence-transformers: pip install sentence-transformers")
    
    else:
        # 默认使用 OpenAI
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
        )