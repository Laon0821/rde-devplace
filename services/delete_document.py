import os
import shutil
from config import DATA_DIRS
from utils.vectordb.build_vectordb import build_vectordb
from datetime import datetime

def delete_document(file_name: str, category: str) -> dict:
    if category not in DATA_DIRS:
        raise ValueError("Category must be either 'regulation' or 'space'")

    raw_dir = DATA_DIRS[category]["raw"]
    file_path = os.path.join(raw_dir, file_name)
    deleted = False
    log = []

    if os.path.exists(file_path):
        os.remove(file_path)
        log.append(f"🗑️ 파일 삭제 완료: {file_path}")
        deleted = True
    else:
        log.append(f"⚠️ 파일이 존재하지 않음: {file_path}")

    # 관련 임시/가공/벡터 디렉토리 초기화
    processed_dir = DATA_DIRS[category]["processed"]
    embed_dir = DATA_DIRS[category]["embeddings"]
    vectordb_dir = f"./vectordb/{category}_db"

    for dir_path in [processed_dir, embed_dir, vectordb_dir]:
        shutil.rmtree(dir_path, ignore_errors=True)
        os.makedirs(dir_path, exist_ok=True)
        log.append(f"🧹 디렉토리 초기화 완료: {dir_path}")

    log.append(f"🔄 {category} VectorDB 재구축 시작")
    build_vectordb(category)
    log.append(f"✅ {category} VectorDB 재구축 완료")

    # 로그 남기기
    log_file = f"./logs/delete_{category}.log"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] 삭제 요청 - 파일명: {file_name}\n")
        for entry in log:
            f.write(f"{entry}\n")
        f.write("\n")

    return {
        "deleted": deleted,
        "file": file_name,
        "category": category,
        "log": log
    }