from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from typing import List
import os
from app.services.parser import parse_pdf, parse_txt, parse_docx
from app.services.parser.chunker import chunk_text
from app.services.rag.vector_store import add_document_to_vector_store

router = APIRouter()

def process_document(file_path: str, filename: str):
    """后台处理文档：解析 -> 切片 -> 向量入库"""
    try:
        print(f"=== 开始处理文档: {filename} ===")
        
        # 1. 解析文档
        ext = filename.split('.')[-1].lower()
        if ext == 'pdf':
            text = parse_pdf(file_path)
        elif ext == 'txt':
            text = parse_txt(file_path)
        elif ext == 'docx':
            text = parse_docx(file_path)
        else:
            print(f"不支持的文件类型: {ext}")
            return
        
        print(f"文档解析完成，文本长度: {len(text)} 字符")
        
        # 2. 切片
        chunks = chunk_text(text)
        print(f"切片完成: {len(chunks)} 个片段")
        
        if not chunks:
            print("切片结果为空，跳过入库")
            return
        
        # 3. 向量入库
        metadatas = [{"source": filename, "chunk_id": i} for i in range(len(chunks))]
        count = add_document_to_vector_store(chunks, metadatas)
        print(f"向量入库完成: {count} 个向量")
        
    except Exception as e:
        print(f"文档处理失败: {str(e)}")

@router.post("/upload")
async def upload_documents(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    os.makedirs("uploads", exist_ok=True)
    results = []
    for file in files:
        content = await file.read()
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 后台处理：解析 -> 切片 -> 入库
        background_tasks.add_task(process_document, file_path, file.filename)
        
        results.append({
            "filename": file.filename,
            "size": len(content),
            "status": "processing"
        })
    return {"message": f"成功上传 {len(results)} 个文件，正在后台处理", "files": results}

@router.get("/list")
async def list_documents():
    return {"documents": []}