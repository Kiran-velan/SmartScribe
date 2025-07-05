from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.appwrite_client import databases
import os
from uuid import uuid4
from datetime import datetime
import json
from fastapi import Query as FastAPIQuery
from appwrite.query import Query
from fastapi import Request
from fastapi import File, Form, UploadFile
from app.summarizer import transcribe_file, transcribe_youtube


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
async def create_transcript(
    request: Request,
    file: UploadFile = File(None),
    title: str = Form(None),
    user_id: str = Form(None),
    session_id: str = Form(None),
):
    try:
        # File Upload
        if file:
            file_bytes = await file.read()
            if not title:
                title = file.filename
            original_text = transcribe_file(file_bytes, file.filename)

        # JSON Fallback (for YouTube and raw JSON)
        else:
            body = await request.json()
            title = title or body.get("title")
            user_id = user_id or body.get("user_id")
            session_id = session_id or body.get("session_id")
            youtube_url = body.get("youtube_url")
            original_text = body.get("original_text")

            if youtube_url:
                if not title:
                    title = youtube_url
                original_text = transcribe_youtube(youtube_url)

        # Final validation
        if not (title and original_text and user_id):
            raise HTTPException(status_code=400, detail="Missing required fields")

        data = {
            "title": title,
            "original_text": original_text,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
        }
        if session_id:
            data["session_id"] = session_id

        response = databases.create_document(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_COLLECTION_ID"),
            document_id=str(uuid4()),
            data=data
        )

        return {"message": "Transcript saved", "id": response["$id"]}
    except Exception as e:
        print("Transcript Error:", e)
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

@app.post("/messages")
async def create_message(request: Request):
    body = await request.json()
    print("Message payload:", body)
    session_id = body.get("session_id")
    sender = body.get("sender")
    text = body.get("text")

    if not (session_id and sender and text):
        raise HTTPException(status_code=400, detail="Missing fields")

    try:
        response = databases.create_document(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_MESSAGES_COLLECTION_ID"),
            document_id=str(uuid4()),
            data={
                "session_id": session_id,
                "sender": sender,
                "text": text,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        return {"message": "Message stored", "message_doc": response}
    except Exception as e:
        print("Error creating message:", e)
        return {"error": str(e)}

@app.get("/messages")
def get_messages(session_id: str = Query(...)):
    try:
        res = databases.list_documents(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_MESSAGES_COLLECTION_ID"),
            queries=[Query.equal("session_id", session_id)],
        )
        return {"messages": res["documents"]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    try:
        session = databases.get_document(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_SESSION_COLLECTION_ID"),
            document_id=session_id
        )
        return {"session": session}
    except Exception as e:
        return {"error": str(e)}

@app.patch("/sessions/{session_id}")
async def update_session(session_id: str, request: Request):
    body = await request.json()
    new_title = body.get("title")

    if not new_title:
        raise HTTPException(status_code=400, detail="Missing title")

    try:
        updated = databases.update_document(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_SESSION_COLLECTION_ID"),
            document_id=session_id,
            data={"title": new_title}
        )
        return {"message": "Session updated", "session": updated}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transcripts/by-session")
def get_transcripts_by_session(session_id: str = Query(...)):
    try:
        response = databases.list_documents(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_COLLECTION_ID"),
            queries=[Query.equal("session_id", session_id)]
        )
        return {"transcripts": response["documents"]}
    except Exception as e:
        print("Transcript Fetch Error:", e)
        return {"error": str(e)}
