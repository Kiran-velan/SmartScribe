from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.appwrite_client import databases
import os
from uuid import uuid4
from datetime import datetime
import json
from fastapi import Query as FastAPIQuery
from appwrite.query import Query

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SmartScribe backend is up!"}

@app.post("/transcripts")
async def create_transcript(request: Request):
    body = await request.json()
    title = body.get("title")
    original_text = body.get("original_text")
    user_id = body.get("user_id")

    if not (title and original_text and user_id):
        raise HTTPException(status_code=400, detail="Missing fields")

    try:
        response = databases.create_document(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_COLLECTION_ID"),
            document_id=str(uuid4()),
            data={
                "title": title,
                "original_text": original_text,
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat()
            }
        )
        return {"message": "Transcript saved", "id": response["$id"]}
    except Exception as e:
        print("Appwrite Error:", e) 
        return {"error": str(e)}

@app.get("/transcripts")
def get_transcripts(user_id: str = FastAPIQuery(...)):
    try:
        response = databases.list_documents(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_COLLECTION_ID"),
            queries=[Query.equal("user_id", user_id)]
        )
        return {"transcripts": response["documents"]}
    except Exception as e:
        print("Appwrite Fetch Error:", e)
        return {"error": str(e)}

@app.post("/sessions")
async def create_session(request: Request):
    body = await request.json()
    title = body.get("title")
    user_id = body.get("user_id")

    if not (title and user_id):
        raise HTTPException(status_code=400, detail="Missing fields")

    try:
        response = databases.create_document(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_SESSION_COLLECTION_ID"),
            document_id=str(uuid4()),
            data={
                "title": title,
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat()
            }
        )
        return {"message": "Session created", "session": response}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.get("/sessions")
def get_sessions(user_id: str = Query(...)):
    try:
        response = databases.list_documents(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_SESSION_COLLECTION_ID"),
            queries=[Query.equal("user_id", user_id)]
        )
        return {"sessions": response["documents"]}
    except Exception as e:
        return {"error": str(e)}
