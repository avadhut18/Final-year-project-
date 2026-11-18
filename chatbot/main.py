import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from auth import create_token, verify_token
from groq import chat_with_groq

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

# Restrict this list to the actual frontend origin before deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    configured_username = os.getenv("ADMIN_USERNAME")
    configured_password = os.getenv("ADMIN_PASSWORD")

    if configured_username and configured_password and username == configured_username and password == configured_password:
        return {"token": create_token(username)}

    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message")

        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        reply = chat_with_groq(message)
        return JSONResponse(content={"response": reply})
    except HTTPException:
        raise
    except Exception as e:
        print("Error in /chat:", str(e))
        return JSONResponse(
            content={"response": "Error: Could not process your request."},
            status_code=500,
        )


@app.post("/upload")
async def upload_file(
    token: str = Form(...),
    file: UploadFile = File(None),
    url: str = Form(None),
):
    verify_token(token)

    if file:
        # Keep the uploaded name to its final path component.
        safe_name = Path(file.filename or "upload").name
        file_path = os.path.join(UPLOAD_DIR, safe_name)
        with open(file_path, "wb") as destination:
            shutil.copyfileobj(file.file, destination)
        return {"message": "File uploaded", "filename": safe_name}

    if url:
        filename = f"url_{abs(hash(url))}.txt"
        with open(os.path.join(UPLOAD_DIR, filename), "w", encoding="utf-8") as destination:
            destination.write(url)
        return {"message": "URL saved", "filename": filename}

    raise HTTPException(status_code=400, detail="No file or URL provided")


@app.get("/files")
def list_files(token: str = ""):
    verify_token(token)
    return {"files": os.listdir(UPLOAD_DIR)}


@app.post("/delete")
async def delete_file(request: Request):
    form = await request.form()
    token = form.get("token")
    filename = form.get("filename")

    verify_token(token)

    if not filename or Path(filename).name != filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "File deleted"}

    raise HTTPException(status_code=404, detail="File not found")


@app.get("/data/{filename}")
async def get_uploaded_file(filename: str):
    if Path(filename).name != filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)

    raise HTTPException(status_code=404, detail="File not found")
