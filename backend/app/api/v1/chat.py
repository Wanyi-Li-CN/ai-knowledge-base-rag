from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import requests
from app.core.config import settings
from app.services.rag.vector_store import get_vector_store

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
        print("=" * 50)
        print("=== chat 函数被调用 ===")
        print(f"问题: {request.question}")
        
        print(f"OPENAI_BASE_URL: {settings.OPENAI_BASE_URL}")
        print(f"OPENAI_API_KEY: {settings.OPENAI_API_KEY[:15]}...")
        print(f"LLM_MODEL: {settings.LLM_MODEL}")
        
        print("正在检索向量数据库...")
        vector_store = get_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": 4})
        docs = retriever.invoke(request.question)
        print(f"检索到 {len(docs)} 个文档片段")
        
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
        print(f"Prompt 长度: {len(prompt)} 字符")
        
        api_url = f"{settings.OPENAI_BASE_URL}/chat/completions"
        print(f"完整请求地址: {api_url}")
        
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": settings.LLM_MODEL,
            "messages": [
                {"role": "system", "content": "你是一个基于私有知识库的问答助手，只根据提供的文档回答问题。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
        }
        
        print("正在发送请求到 DeepSeek API...")
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容前200字符: {response.text[:200]}")
        
        if response.status_code != 200:
            raise Exception(f"DeepSeek API 错误: {response.status_code} - {response.text}")
        
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        print(f"回答: {answer[:100]}...")
        print("=" * 50)
        
        return ChatResponse(
            answer=answer,
            sources=sources
        )
        
    except Exception as e:
        print(f"!!! 异常发生: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        print("=" * 50)
        raise HTTPException(status_code=500, detail=f"问答失败: {str(e)}")