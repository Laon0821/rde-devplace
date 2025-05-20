import os
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.schema.document import Document
from utils.pdf_loader import extract_text_chunks_from_pdf
from utils.embedder import embedding_model  # Embeddings 객체
from config import DATA_DIRS, VECTORDB_DIRS


def build_vectordb(category: str):
    if category not in DATA_DIRS:
        raise ValueError("Invalid category: must be 'regulation' or 'space'.")

    raw_dir = DATA_DIRS[category]["raw"]
    vectordb_dir = VECTORDB_DIRS[category]
    os.makedirs(vectordb_dir, exist_ok=True)

    documents = []

    # PDF 문서 읽기 및 청크화
    if os.path.exists(raw_dir):
        for filename in os.listdir(raw_dir):
            if filename.endswith(".pdf"):
                filepath = os.path.join(raw_dir, filename)
                try:
                    chunks = extract_text_chunks_from_pdf(filepath)
                    for i, chunk in enumerate(chunks):
                        documents.append(
                            Document(
                                page_content=chunk,
                                metadata={
                                    "source": filepath,
                                    "chunk_index": i,
                                    "filename": filename
                                }
                            )
                        )
                except Exception as e:
                    print(f"❌ {filename} 처리 중 오류 발생: {e}")
    else:
        print(f"⚠️ PDF 디렉토리 없음: {raw_dir} (빈 VectorDB 생성 예정)")

    # VectorDB 생성
    if documents:
        print(f"🔍 {len(documents)}개의 청크 임베딩 중...")
        vectordb = FAISS.from_documents(documents, embedding_model)
    else:
        print(f"📭 문서 없음 → 빈 VectorDB 수동 생성")
        dim = 384  # all-MiniLM-L6-v2 기준
        index = faiss.IndexFlatL2(dim)
        docstore = InMemoryDocstore({})
        index_to_docstore_id = {}
        vectordb = FAISS(embedding_model, index, docstore, index_to_docstore_id)

    vectordb.save_local(vectordb_dir)
    print(f"✅ VectorDB 저장 완료: {vectordb_dir}")
