from docx import Document

def parse_docx(file_path: str) -> str:
    """解析DOCX文件，提取文本内容"""
    try:
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            if para.text:
                text += para.text + "\n"
        return text
    except Exception as e:
        raise Exception(f"DOCX解析失败: {str(e)}")