from typing import List
from langchain_core.embeddings import Embeddings
import requests


class AliyunEmbeddings(Embeddings):
    """阿里云百炼 Embedding 适配器"""
    
    def __init__(self, api_key: str, model: str = "text-embedding-v3", base_url: str = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """批量向量化"""
        response = requests.post(
            f"{self.base_url}/embeddings",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "input": texts
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return [item["embedding"] for item in data["data"]]
    
    def embed_query(self, text: str) -> List[float]:
        """单个文本向量化"""
        return self.embed_documents([text])[0]