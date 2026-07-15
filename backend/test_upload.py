import requests
import sys

print("1. 开始执行...", flush=True)

url = "http://localhost:8001/api/v1/documents/upload"
file_path = "test.txt"

print("2. 检查文件是否存在...", flush=True)
try:
    with open(file_path, "rb") as f:
        content = f.read()
    print(f"3. 文件大小: {len(content)} 字节", flush=True)
except FileNotFoundError:
    print("错误: test.txt 文件不存在！", flush=True)
    sys.exit(1)

print("4. 构建请求...", flush=True)
files = {"files": (file_path, open(file_path, "rb"), "text/plain")}

print("5. 发送POST请求...", flush=True)
try:
    response = requests.post(url, files=files, timeout=5)
    print("6. 收到响应", flush=True)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print("请求失败:", e)
except Exception as e:
    print("其他错误:", e)

print("7. 执行完毕", flush=True)