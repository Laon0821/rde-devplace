import os
from dotenv import load_dotenv

# 환경 변수 로드 (.env 파일에서)
load_dotenv()

# 데이터 경로 설정
DATA_DIRS = {
    "regulation": {
        "raw": "./data/raw/regulation",
        "processed": "./data/processed/regulation",
        "embeddings": "./data/embeddings/regulation"
    },
    "space": {
        "raw": "./data/raw/space",
        "processed": "./data/processed/space",
        "embeddings": "./data/embeddings/space"
    }
}

# VectorDB 저장 위치
VECTORDB_DIRS = {
    "regulation": "./vectordb/regulation_db",
    "space": "./vectordb/space_db"
}

# 사용할 임베딩 모델
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# OpenAI API Key (예: LLM 호출용)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
