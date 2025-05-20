import fitz
from PIL import Image
from io import BytesIO
from typing import List

def extract_text_chunks_from_pdf(pdf_path: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    doc = fitz.open(pdf_path)
    chunks = []

    for page in doc:
        text = page.get_text()
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        for para in paragraphs:
            # 너무 긴 문단은 슬라이딩 윈도우로 나누기
            if len(para) <= chunk_size:
                chunks.append(para)
            else:
                start = 0
                while start < len(para):
                    end = start + chunk_size
                    chunk = para[start:end]
                    chunks.append(chunk)
                    start += chunk_size - overlap

    return chunks

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

def extract_images_from_pdf(pdf_path: str) -> List[Image.Image]:
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image = Image.open(BytesIO(base_image["image"]))
            images.append(image)
    return images
