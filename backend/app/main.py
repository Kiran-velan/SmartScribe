from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.appwrite_client import databases, storage
import os
from uuid import uuid4
from datetime import datetime
import json
from fastapi import Query as FastAPIQuery
from appwrite.query import Query
from fastapi import File, Form, UploadFile
from app.summarizer import transcribe_file, transcribe_youtube
# Importing RAG components
from app.rag.chunker import chunk_transcript
from app.rag.embedder import get_embeddings
from app.rag.vector_store import TranscriptVectorStore
from app.rag.responder import answer_question
from appwrite.input_file import InputFile
import base64, pickle
from io import BytesIO
from pydantic import BaseModel


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

# Pydantic based style
class TalkRequest(BaseModel):
    session_id: str
    prompt: str

# RAG endpoint to answer questions based on session transcripts
@app.post("/talk")
async def talk(data: TalkRequest):
    try:
        session_id = data.session_id

        # 1. Fetch all transcripts for this session
        transcript_response = databases.list_documents(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_COLLECTION_ID"),
            queries=[Query.equal("session_id", session_id)]
        )
        transcripts = transcript_response["documents"]

        if not transcripts:
            raise HTTPException(status_code=404, detail="No transcripts found for this session.")

        num_transcripts = len(transcripts)

        # 2. Check if vector store is cached
        embedding_response = databases.list_documents(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_EMBEDDING_COLLECTION_ID"),
            queries=[Query.equal("session_id", session_id)]
        )

        cached = embedding_response["documents"][0] if embedding_response["documents"] else None

        if cached and cached["number_of_transcripts"] == num_transcripts:
            # ✅ Load vector store from Appwrite Storage
            vector_file = storage.get_file_download(
                bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
                file_id=cached["vector_file_id"]
            )
            vector_store = pickle.loads(vector_file)

        else:
            # 🛠 Rebuild vector store
            vector_store = TranscriptVectorStore(dim=384)
            for doc in transcripts:
                chunks = chunk_transcript(doc["original_text"])
                embeddings = get_embeddings(chunks)
                vector_store.add_embeddings(embeddings, chunks)

            # 🔐 Pickle and upload to Appwrite Storage
            pickle_bytes = pickle.dumps(vector_store)
            file_id = str(uuid4())

            storage_res = storage.create_file(
                bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
                file_id=file_id,
                file=InputFile.from_bytes(pickle_bytes, filename="vector_store.pkl")
            )

            # 🔁 Update or insert vector store record
            if cached:
                databases.update_document(
                    database_id=os.getenv("APPWRITE_DATABASE_ID"),
                    collection_id=os.getenv("APPWRITE_EMBEDDING_COLLECTION_ID"),
                    document_id=cached["$id"],
                    data={
                        "vector_file_id": file_id,
                        "number_of_transcripts": num_transcripts
                    }
                )
            else:
                databases.create_document(
                    database_id=os.getenv("APPWRITE_DATABASE_ID"),
                    collection_id=os.getenv("APPWRITE_EMBEDDING_COLLECTION_ID"),
                    document_id=str(uuid4()),
                    data={
                        "session_id": session_id,
                        "vector_file_id": file_id,
                        "number_of_transcripts": num_transcripts
                    }
                )

        # 3. Generate answer using RAG
        answer = answer_question(data.prompt, vector_store)

        # 4. Store assistant response in messages collection
        databases.create_document(
            database_id=os.getenv("APPWRITE_DATABASE_ID"),
            collection_id=os.getenv("APPWRITE_MESSAGES_COLLECTION_ID"),
            document_id=str(uuid4()),
            data={
                "session_id": session_id,
                "sender": "assistant",
                "text": answer,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

        return {"response": answer}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
