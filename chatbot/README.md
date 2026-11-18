# CSMU Chatbot

A college information chatbot for Chhatrapati Shivaji Maharaj University (CSMU). Staff can sign in and upload reference documents; students and visitors can ask questions through a simple web interface. The backend builds context from files in the local `uploads/` directory and uses the Groq API to generate responses.

## Features

- Student-facing chat interface (HTML, CSS and JavaScript)
- Staff login using JWT authentication
- Upload PDF, DOCX and TXT reference files
- Admin dashboard to view and delete uploaded items
- Document text extraction and Groq-powered responses
- FastAPI backend

## Tech stack

- **Backend:** Python, FastAPI, Uvicorn
- **AI API:** Groq Chat Completions
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** PyJWT
- **Document processing:** PyMuPDF and python-docx

## Run locally

1. Install Python 3.10 or later.
2. Open a terminal in this `chatbot/` directory.
3. Create and activate a virtual environment.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env` and set `GROQ_API_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and a long random `JWT_SECRET`.
6. Start the API:

   ```bash
   python run.py
   ```

7. Open `index.html` in a browser. The frontend is configured to call `http://127.0.0.1:8001`.

## Environment variables

| Variable | Purpose |
| --- | --- |
| `GROQ_API_KEY` | Your Groq API key |
| `GROQ_MODEL` | Groq model name |
| `ADMIN_USERNAME` | Staff login username |
| `ADMIN_PASSWORD` | Staff login password |
| `JWT_SECRET` | Long random secret used to sign tokens |
| `JWT_ALGORITHM` | JWT signing algorithm (defaults to HS256) |

## Security and limitations

- Never commit `.env`, API keys, passwords, or JWT secrets.
- Uploaded documents are stored locally in `uploads/`, which Git ignores.
- This is an academic project, not a production-hardened service. Before deployment, restrict CORS origins, use HTTPS, validate uploads and filenames, add rate limiting, and use persistent storage.
- The frontend currently uses a localhost API URL; update it for a deployed backend.
