from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from app.core.config import settings

def get_vector_store():
    """获取 pgvector 向量存储实例"""
    embeddings = OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )
    
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="knowledge_base",
        connection=settings.DATABASE_URL,
        use_jsonb=True,
    )
    return vector_store

def add_document_to_vector_store(texts: list, metadatas: list = None):
    """将文本块添加到向量库"""
    vector_store = get_vector_store()
    vector_store.add_texts(texts, metadatas=metadatas)
    return len(texts)