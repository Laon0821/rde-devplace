from typing import List
from langchain_community.vectorstores import FAISS
from langchain.schema.document import Document
from utils.embedder import embedding_model
from config import VECTORDB_DIRS

def load_vectordb(category: str) -> FAISS:
    if category not in VECTORDB_DIRS:
        raise ValueError("Category must be 'regulation' or 'space'")

    vectordb_path = VECTORDB_DIRS[category]
    return FAISS.load_local(vectordb_path, embedding_model, allow_dangerous_deserialization=True)

def search(category: str, query: str, k: int = 3) -> List[Document]:
    vectordb = load_vectordb(category)
    return vectordb.similarity_search(query, k=k)
