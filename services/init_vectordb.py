# services/init_vectordb.py
from utils.vectordb.build_vectordb import build_vectordb

def initialize_vectordb():
    for category in ["regulation", "space"]:
        try:
            print(f"🛠️ {category} VectorDB 초기화 중...")
            build_vectordb(category)  # 내부적으로 빈 경우에도 FAISS Index 생성되도록 설계
            print(f"✅ {category} VectorDB 초기화 완료")
        except Exception as e:
            print(f"❌ {category} 초기화 실패: {e}")

if __name__ == "__main__":
    initialize_vectordb()
