# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rizq is a personal AI memory engine that processes audio files (voice memos, lectures, meetings), transcribes them using OpenAI Whisper, generates structured digests, and stores them in a vector database (ChromaDB) for semantic search and retrieval. Users can upload audio files, ask questions about their past content, and chat with an AI that has access to their memory.

## Architecture

### Backend (Python/FastAPI)
- **Location**: `backend/app/`
- **Framework**: FastAPI with CORS middleware allowing all origins
- **AI Integration**: Uses OpenAI API (GPT-4o-mini for text, Whisper-1 for audio transcription)
- **Vector Database**: ChromaDB with persistent storage in `backend/chroma_db/` directory
- **Embedding Model**: SentenceTransformer (`all-MiniLM-L6-v2`)

### Frontend (React/Vite)
- **Location**: `frontend/src/`
- **Framework**: React 19 with Vite
- **UI**: Simple single-page app for uploading audio files and searching/chatting

### Key Flow
1. User uploads audio file via frontend → `/ingest` endpoint
2. Backend transcribes audio with Whisper
3. Backend generates digest with GPT-4o-mini (summary, highlights, insights, action items, questions)
4. Combined transcript + digest is embedded and stored in ChromaDB with UUID
5. User can search or chat, which queries ChromaDB for relevant context and uses GPT to synthesize answers

## Common Development Commands

### Backend
```bash
# Navigate to backend
cd backend

# Create and activate virtual environment (if not exists)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install missing dependencies that are used but not in requirements.txt
pip install chromadb openai sentence-transformers

# Run the FastAPI server
uvicorn app.main:app --reload --port 8000

# Run without reload
uvicorn app.main:app --port 8000
```

### Frontend
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server (default port 5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Important Implementation Details

### Database Initialization
- ChromaDB client is initialized in `backend/app/db.py` with persistent storage
- Collection name: `"notes"`
- Embedding function is imported and used across the app
- Data persists in `backend/chroma_data/` directory

### API Endpoints Structure
All endpoints are defined in `backend/app/main.py`:
- `POST /ingest` - Full pipeline: transcribe audio → digest → store in ChromaDB
- `POST /transcribe` - Audio transcription only
- `POST /digest` - Text file digestion
- `POST /smartnotes` - Generate smart notes from text
- `POST /ask` - Answer questions based on provided document
- `POST /search` - Semantic search through stored memories
- `POST /chat` - Conversational interface with memory context (top 5 results)

### OpenAI Integration
- The OpenAI client is instantiated multiple times in `main.py` (line 8 and 29)
- Requires `OPENAI_API_KEY` environment variable to be set
- Model used: `gpt-4o-mini` for all text generation tasks
- Whisper model: `whisper-1` for transcription

### Frontend API Communication
- Hardcoded backend URL: `http://127.0.0.1:8000`
- No authentication or error handling implemented
- Responses displayed as raw JSON in `<pre>` tags

## Known Issues & Quirks

1. **Duplicate imports**: `main.py` has duplicate imports (e.g., `from .db import collection` appears twice, OpenAI client instantiated twice)
2. **Missing dependencies**: ChromaDB, OpenAI, and sentence-transformers are used but not in `requirements.txt`
3. **No environment file**: `.env` file needed for `OPENAI_API_KEY` but not documented
4. **Empty routers directory**: `backend/app/routers/` exists but is unused
5. **SQLAlchemy in requirements**: Listed but not used in the codebase
6. **Character replacement**: `/ask` endpoint has unnecessary smart quote replacements (lines 91-92)

## Environment Setup

Create a `.env` file in the `backend/` directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Testing

No test suite currently exists. Manual testing via:
1. Start backend: `cd backend && uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Upload an audio file and verify transcription/storage
4. Search for content to verify retrieval
