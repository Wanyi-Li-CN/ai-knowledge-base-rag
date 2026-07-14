from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    knowledge_base_id: Optional[int] = None
    history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict] = []

@router.post("/chat")
async def chat(request: ChatRequest):
    # 临时返回，不依赖任何配置
    return ChatResponse(
        answer=f"你问的是：{request.question}。欢迎使用AI知识库问答系统！（测试版本）",
        sources=[]
    )