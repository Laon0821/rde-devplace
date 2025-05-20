import argparse
import shutil
from config import VECTORDB_DIRS
from utils.vectordb import build_vectordb, list_documents

TARGETS = ["regulation", "space"]

def delete_vectordb(target: str):
    vectordb_dir = VECTORDB_DIRS[target]
    shutil.rmtree(vectordb_dir, ignore_errors=True)
    print(f"✅ {target} VectorDB 삭제 완료 ({vectordb_dir})")

def build(target: str):
    build_vectordb(target)

def list_docs(target: str):
    docs = list_documents(target)
    print(f"✅ {target} VectorDB 문서 목록:")
    for doc_name, security_level in docs:
        print(f" - {doc_name} (보안등급: {security_level})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VectorDB 관리 스크립트")

    parser.add_argument("action", choices=["build", "delete", "list", "build_all"], help="실행할 작업")
    parser.add_argument("--target", choices=TARGETS, help="대상 (regulation 또는 space)")

    args = parser.parse_args()

    if args.action in ["build", "delete", "list"] and not args.target:
        parser.error("--target 은 필수입니다 (regulation 또는 space)")

    if args.action == "build":
        build(args.target)
    elif args.action == "delete":
        delete_vectordb(args.target)
    elif args.action == "list":
        list_docs(args.target)
    elif args.action == "build_all":
        for target in TARGETS:
            build(target)
