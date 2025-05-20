import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

# SentenceTransformer 직접 로드
model = SentenceTransformer(EMBEDDING_MODEL)

# LangChain Embeddings 객체로도 준비 (이걸 FAISS에 넘길 것임)
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def embed_text(text: str) -> np.ndarray:
    """
    텍스트를 numpy array로 변환 (기존 코드 유지 - 단독 사용시)
    """
    return model.encode(text)

def image_to_embedding(image: Image.Image) -> np.ndarray:
    """
    이미지를 numpy array로 변환
    """
    image = image.resize((64, 64)).convert("RGB")
    arr = np.array(image).flatten() / 255.0
    return arr[:384] if arr.size >= 384 else np.pad(arr, (0, 384 - arr.size))
