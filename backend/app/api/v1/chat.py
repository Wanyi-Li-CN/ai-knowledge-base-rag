from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import requests
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from app.core.config import settings

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    knowledge_base_id: Optional[int] = None
    history: Optional[List[dict]] = []

class Source(BaseModel):
    content: str
    source: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = []

def get_vector_store():
    embeddings = OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )
    return PGVector(
        embeddings=embeddings,
        collection_name="knowledge_base",
        connection=settings.DATABASE_URL,
        use_jsonb=True,
    )

def build_prompt(question: str, contexts: List[str]) -> str:
    context_text = "\n\n---\n\n".join(contexts)
    return f"""你是一个基于私有知识库的问答助手，请严格遵循以下规则：

1. 只基于以下提供的文档片段回答问题
2. 如果文档片段中没有相关信息，请直接说"根据当前知识库，我无法回答这个问题"
3. 不要编造任何不在文档中的信息
4. 回答要简洁、准确

文档片段：
{context_text}

问题：{question}

回答："""

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        vector_store = get_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": 4})
        docs = retriever.invoke(request.question)
        
        if not docs:
            return ChatResponse(
                answer="知识库中暂无相关内容，请先上传文档。",
                sources=[]
            )
        
        contexts = [doc.page_content for doc in docs]
        sources = [
            Source(
                content=doc.page_content[:200] + "...",
                source=doc.metadata.get("source", "未知")
            )
            for doc in docs
        ]
        
        prompt = build_prompt(request.question, contexts)
        
        # 用 requests 调用 DeepSeek API
        response = requests.post(
            f"{settings.OPENAI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": settings.LLM_MODEL,
                "messages": [
                    {"role": "system", "content": "你是一个基于私有知识库的问答助手，只根据提供的文档回答问题。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
            },
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"DeepSeek API 错误: {response.status_code} - {response.text}")
        
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        
        return ChatResponse(
            answer=answer,
            sources=sources
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"问答失败: {str(e)}")