import os
import shutil
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.init_vectordb import initialize_vectordb
from services.add_document import add_document
from services.delete_document import delete_document
from services.multi_agent_chat import chat_with_agent

router = APIRouter()

@router.post("/init")
def init_vectordb():
    initialize_vectordb()
    return {"message": "✅ 모든 VectorDB 초기화 완료"}

@router.post("/add")
async def add_pdf(file: UploadFile = File(...), category: str = Form(...)):
    if category not in ["regulation", "space"]:
        raise HTTPException(status_code=400, detail="category는 regulation 또는 space 여야 합니다.")

    # 임시 경로 저장
    temp_path = f"./temp/{file.filename}"
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)

    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 핵심 처리
    try:
        add_document(temp_path, category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(temp_path)

    return {"message": f"✅ {file.filename} 처리 완료", "category": category}

class DeleteRequest(BaseModel):
    filename: str
    category: str

@router.delete("/delete")
def delete_pdf(request: DeleteRequest):
    if request.category not in ["regulation", "space"]:
        raise HTTPException(status_code=400, detail="category는 regulation 또는 space 여야 합니다.")

    try:
        result = delete_document(request.filename, request.category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "✅ 삭제 요청 처리 완료",
        "deleted": result["deleted"],
        "file": result["file"],
        "category": result["category"],
        "log": result["log"]
    }

@router.post("/chat")
def chat(message_text: str = Form(...)):
    result = chat_with_agent(message_text)
    return result
