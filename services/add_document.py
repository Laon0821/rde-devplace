import os
import shutil
import uuid
from config import DATA_DIRS
from utils.vectordb.build_vectordb import build_vectordb

def add_document(pdf_path: str, category: str):
    if category not in DATA_DIRS:
        raise ValueError("❌ category must be either 'regulation' or 'space'")

    # ✅ 확장자 검사
    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("❌ Only .pdf files are allowed.")

    file_name = os.path.basename(pdf_path)
    raw_dir = DATA_DIRS[category]["raw"]
    os.makedirs(raw_dir, exist_ok=True)

    # ✅ 중복 파일명 방지
    dest_path = os.path.join(raw_dir, file_name)
    if os.path.exists(dest_path):
        unique_suffix = uuid.uuid4().hex[:8]
        name, ext = os.path.splitext(file_name)
        new_file_name = f"{name}_{unique_suffix}{ext}"
        dest_path = os.path.join(raw_dir, new_file_name)
        print(f"⚠️ 파일명 중복 → {new_file_name} 으로 저장됩니다.")
    else:
        new_file_name = file_name

    # ✅ 저장
    shutil.copy2(pdf_path, dest_path)
    print(f"📥 PDF 저장 완료: {dest_path}")

    # ✅ VectorDB 재구축
    print(f"🔄 {category} VectorDB 재구축 중...")
    build_vectordb(category)
    print(f"✅ VectorDB 업데이트 완료")

    return {
        "status": "success",
        "saved_as": new_file_name,
        "category": category
    }