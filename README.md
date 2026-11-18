# CSMU Chatbot — Final-Year Project

A college information chatbot built with a FastAPI backend and an HTML/CSS/JavaScript interface. Staff can sign in, upload reference documents or save website links, and students can ask questions using the available college content. Groq provides the language-model API.

## Repository contents

- `chatbot/` — backend, frontend, authentication, document processing, dependencies and setup guide.

## Quick start

See [`chatbot/README.md`](chatbot/README.md) for configuration and local run instructions. Copy `chatbot/.env.example` to `chatbot/.env` and supply your own API key and credentials. Never commit `.env`.

## Security note

The original archive contained credentials. Those values have been excluded from this repository; use fresh credentials and rotate the previously exposed Groq API key before using the project.