from fastapi import APIRouter, UploadFile, File
from typing import List
import os

router = APIRouter()

@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    os.makedirs("uploads", exist_ok=True)
    results = []
    for file in files:
        content = await file.read()
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as f:
            f.write(content)
        results.append({
            "filename": file.filename,
            "size": len(content),
            "status": "uploaded"
        })
    return {"message": f"成功上传 {len(results)} 个文件", "files": results}

@router.get("/list")
async def list_documents():
    return {"documents": []}