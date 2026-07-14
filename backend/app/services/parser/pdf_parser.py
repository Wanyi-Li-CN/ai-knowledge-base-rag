from pypdf import PdfReader

def parse_pdf(file_path: str) -> str:
    """解析PDF文件，提取文本内容"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        raise Exception(f"PDF解析失败: {str(e)}")