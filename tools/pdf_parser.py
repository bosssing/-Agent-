import pdfplumber
from typing import Optional
import io


class PDFParser:
    @staticmethod
    def parse_pdf(file_path: Optional[str] = None, file_bytes: Optional[bytes] = None) -> str:
        text = ""
        try:
            if file_path:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() or ""
            elif file_bytes:
                with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() or ""
        except Exception as e:
            raise Exception(f"PDF解析失败: {str(e)}")
        return text

    @staticmethod
    def parse_pdf_with_structure(file_path: Optional[str] = None, file_bytes: Optional[bytes] = None) -> dict:
        result = {
            "text": "",
            "pages": [],
            "tables": []
        }
        try:
            if file_path:
                pdf = pdfplumber.open(file_path)
            elif file_bytes:
                pdf = pdfplumber.open(io.BytesIO(file_bytes))
            else:
                return result

            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                result["text"] += page_text
                result["pages"].append({
                    "page_number": page_num + 1,
                    "text": page_text
                })
                
                tables = page.extract_tables()
                if tables:
                    result["tables"].append({
                        "page_number": page_num + 1,
                        "tables": tables
                    })
            
            pdf.close()
        except Exception as e:
            raise Exception(f"PDF结构解析失败: {str(e)}")
        return result
