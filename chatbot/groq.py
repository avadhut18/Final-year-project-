import os
import requests
from dotenv import load_dotenv
from docx import Document
import fitz

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

MAX_CONTEXT_CHARS = 10000


def extract_text_from_docx(path):
    try:
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX {path}: {e}")
        return ""


def extract_text_from_pdf(path):
    try:
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        print(f"Error reading PDF {path}: {e}")
        return ""


def chat_with_groq(messages):
    if not GROQ_API_KEY:
        return "The chatbot is not configured yet. Please set GROQ_API_KEY in your .env file."

    try:
        upload_folder = "uploads"
        context = ""

        if os.path.isdir(upload_folder):
            for file in os.listdir(upload_folder):
                file_path = os.path.join(upload_folder, file)
                if file.endswith(".txt"):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            context += f.read() + "\n\n"
                    except UnicodeDecodeError:
                        print(f"Skipped unreadable .txt file: {file}")
                elif file.endswith(".docx"):
                    context += extract_text_from_docx(file_path) + "\n\n"
                elif file.endswith(".pdf"):
                    context += extract_text_from_pdf(file_path) + "\n\n"
                else:
                    print(f"Skipped unsupported file: {file}")

        context = context[-MAX_CONTEXT_CHARS:]
        system_prompt = {
            "role": "system",
            "content": (
                "You are the official CSMU Chatbot. Only answer using the uploaded content below. "
                "If you do not have an answer from this data, say 'Sorry, I don't have information on that.'\n\n"
                f"CSMU Content:\n{context}"
            )
        }

        final_messages = [system_prompt] + ([{"role": "user", "content": messages}] if isinstance(messages, str) else messages)
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": GROQ_MODEL,
            "messages": final_messages,
            "temperature": 0.7,
            "max_tokens": 512
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print("Error in chat_with_groq:", str(e))
        return "Error: Could not process your request."
