const API_BASE = 'http://localhost:8001/api/v1';

export async function chat(question: string) {
  const res = await fetch(`${API_BASE}/chat`, {  // ← 改成 /chat
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, knowledge_base_id: null, history: [] }),
  });
  return res.json();
}

export async function uploadFiles(files: FileList) {
  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append('files', files[i]);
  }
  const res = await fetch(`${API_BASE}/documents/upload`, {
    method: 'POST',
    body: formData,
  });
  return res.json();
}