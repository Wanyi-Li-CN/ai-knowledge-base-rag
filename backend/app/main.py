from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import health, documents, chat

app = FastAPI(
    title="AI多Agent知识库智能问答系统",
    version="1.0.1",
    description="基于LangChain多Agent协同 + PostgreSQL/pgvector"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由 - 三个分组
app.include_router(health.router, prefix="/api/v1", tags=["健康检查"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["文档管理"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["智能问答"])

@app.get("/")
async def root():
    return {
        "message": "AI多Agent知识库智能问答系统",
        "version": "1.0.0",
        "docs": "/docs"
    }