from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import uuid
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# ChromaDB disabled for deployment (too memory-heavy for free tier)
# from app.db import collection, embedding_fn
from app.utils import parse_gpt_json, extract_structured_digest, extract_smartnotes, extract_flashcards, remove_repetitive_endings, remove_hallucinations
from app.models import (
    IngestResponse, IngestResponseData, TranscriptData, DigestData, MemoryMetadata,
    Flashcard, FlashcardsData,
    SearchResponse, SearchResponseData, SearchSource,
    ChatResponse, ChatResponseData,
    SmartNotesResponse, SmartNotesData,
    TranscribeResponse, TranscribeResponseData,
    ErrorResponse
)

client = OpenAI()
app = FastAPI(title="Rizq Memory Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Rizq backend running"}

class SmartNotesRequest(BaseModel):
    text: str

@app.post("/smartnotes")
async def smartnotes(req: SmartNotesRequest):
    import os

    prompt = f"""
    Create Smart Notes for the following text:

    TEXT:
    {req.text}

    OUTPUT IN JSON:
    - summary
    - structured_notes (3-5 bullets)
    - flashcards (list of {{"front": "...", "back": "..."}})
    - quizzes (list of questions)
    - eli12 (explain like I'm 12)
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {"smartnotes": response.choices[0].message.content}

@app.post("/digest")
async def digest(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8", errors="ignore")

    prompt = f"""
    Digest the following document and produce tightly-structured JSON.

    TEXT:
    {content}

    OUTPUT JSON FIELDS:
    - summary (3–5 sentences)
    - highlights (5 bullets)
    - action_items (3–7 bullets)
    - insights (3 bullets)
    - questions (3–5 questions)

    Return ONLY valid JSON.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"digest": response.choices[0].message.content}
class AskRequest(BaseModel):
    question: str
    content: str

@app.post("/ask")
async def ask(req: AskRequest):
    safe_question = req.question.replace("“", "\"").replace("”", "\"").replace("’", "'")
    safe_content = req.content.replace("“", "\"").replace("”", "\"").replace("’", "'")

    prompt = f"""
    Use ONLY the document below to answer the question.

    DOCUMENT:
    {req.content}

    QUESTION:
    {req.question}

    Answer concisely and accurately.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"answer": response.choices[0].message.content}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()

    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.m4a", audio_bytes)
    )

    return {"text": transcription.text}

@app.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()

        # Check file size and compress if needed (Whisper has 25MB limit)
        MAX_SIZE = 24 * 1024 * 1024  # 24MB to be safe
        filename = file.filename or "audio.m4a"

        if len(audio_bytes) > MAX_SIZE:
            from pydub import AudioSegment
            import io

            original_size = len(audio_bytes)

            # Load audio
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

            # Compress: reduce to mono, lower bitrate
            audio = audio.set_channels(1)  # Mono
            audio = audio.set_frame_rate(16000)  # Lower sample rate (16kHz is good for speech)

            # Export to compressed format
            compressed_buffer = io.BytesIO()
            audio.export(compressed_buffer, format="mp3", bitrate="32k")  # Very low bitrate for speech
            compressed_buffer.seek(0)
            audio_bytes = compressed_buffer.read()
            filename = "compressed_audio.mp3"

            print(f"Compressed audio from {original_size/(1024*1024):.1f}MB to {len(audio_bytes)/(1024*1024):.1f}MB", flush=True)

        # 1. Transcribe (force English to handle accented speakers)
        # Use prompt to suppress common hallucinations
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=(filename, audio_bytes),
            language="en",  # Force English transcription
            prompt="This is a university lecture recording. Transcribe only the actual spoken lecture content."
        )
        text = transcription.text

        # Clean up hallucinations and repetitions
        text = remove_hallucinations(text)
        text = remove_repetitive_endings(text)

        # 2. Digest - improved prompt for clean JSON
        prompt = f"""
        Create a structured digest of this text. Return ONLY a valid JSON object with no markdown formatting.

        TEXT:
        {text}

        Return JSON with exactly these fields:
        {{
            "summary": "2-3 sentence summary",
            "highlights": ["highlight 1", "highlight 2", "highlight 3", "highlight 4", "highlight 5"],
            "insights": ["insight 1", "insight 2", "insight 3"],
            "action_items": ["action 1", "action 2", "action 3"],
            "questions": ["question 1", "question 2", "question 3"]
        }}
        """

        digest = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        digest_text = digest.choices[0].message.content

        # Parse the digest JSON
        parsed_digest = extract_structured_digest(digest_text)

        # 3. Generate flashcards
        flashcard_prompt = f"""
        Create study flashcards from this text. Return ONLY a valid JSON object with no markdown formatting.

        TEXT:
        {text}

        Generate 8-12 flashcards that help someone study and remember the key concepts.
        Make them concise and test-worthy.

        Return JSON with exactly this format:
        {{
            "flashcards": [
                {{"front": "Question or term", "back": "Answer or definition"}},
                {{"front": "What is...", "back": "The answer is..."}},
                ...
            ]
        }}
        """

        flashcard_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": flashcard_prompt}]
        )

        flashcard_text = flashcard_response.choices[0].message.content
        flashcard_list = extract_flashcards(flashcard_text)

        # Generate unique ID for this memory
        memory_id = str(uuid.uuid4())

        # 4. Store in Chroma with metadata
        # DISABLED FOR DEPLOYMENT: ChromaDB uses too much memory for free tier
        # embeddings = embedding_fn([text])
        # collection.add(
        #     ids=[memory_id],
        #     documents=[text + "\n\n" + digest_text],
        #     embeddings=embeddings,
        #     metadatas=[{
        #         "timestamp": datetime.now().isoformat(),
        #         "filename": file.filename,
        #         "type": "audio_ingest",
        #         "word_count": len(text.split())
        #     }]
        # )

        # 5. Return structured response
        return IngestResponse(
            success=True,
            data=IngestResponseData(
                memory_id=memory_id,
                transcript=TranscriptData(
                    text=text,
                    word_count=len(text.split()),
                    duration=None
                ),
                digest=DigestData(
                    summary=parsed_digest.get("summary", ""),
                    highlights=parsed_digest.get("highlights", []),
                    insights=parsed_digest.get("insights", []),
                    action_items=parsed_digest.get("action_items", []),
                    questions=parsed_digest.get("questions", [])
                ),
                flashcards=FlashcardsData(
                    flashcards=[Flashcard(**card) for card in flashcard_list],
                    count=len(flashcard_list)
                ),
                metadata=MemoryMetadata(
                    created_at=datetime.now().isoformat(),
                    filename=file.filename,
                    type="audio_ingest"
                )
            ),
            message="Audio processed and stored successfully"
        )

    except Exception as e:
        import traceback
        print(f"ERROR IN INGEST: {str(e)}", flush=True)
        print(traceback.format_exc(), flush=True)
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

@app.post("/search", response_model=SearchResponse)
async def search(req: dict):
    # Search disabled in deployment (ChromaDB requires too much memory)
    raise HTTPException(status_code=503, detail="Search feature temporarily disabled in free tier deployment")

    try:
        query = req.get("query", "")

        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Query ChromaDB for relevant documents
        # results = collection.query(
        #     query_texts=[query],
        #     n_results=3
        # )

        matches = results["documents"][0] if results["documents"] else []
        ids = results["ids"][0] if results["ids"] else []
        distances = results.get("distances", [[]])[0] if results.get("distances") else []

        # Ask GPT to synthesize the matches into an answer
        answer_prompt = f"""
        Based on these notes from the memory database, answer the user's question.

        QUESTION: {query}

        NOTES:
        {matches}

        Provide a clear, concise, and helpful answer based on the notes above.
        If the notes don't contain relevant information, say so.
        """

        answer = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": answer_prompt}]
        )

        # Build source list
        sources = []
        for i, match in enumerate(matches):
            sources.append(SearchSource(
                id=ids[i] if i < len(ids) else f"unknown_{i}",
                snippet=match[:300] + "..." if len(match) > 300 else match,
                relevance_score=1.0 - distances[i] if i < len(distances) else None
            ))

        return SearchResponse(
            success=True,
            data=SearchResponseData(
                answer=answer.choices[0].message.content,
                sources=sources,
                query=query
            ),
            message=f"Found {len(matches)} relevant memories"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching memories: {str(e)}")
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(req: ChatRequest):
    user_message = req.message

    # 1) Find relevant memories from Chroma
    results = collection.query(
        query_texts=[user_message],
        n_results=5
    )

    documents = results.get("documents", [[]])
    context = "\n\n---\n\n".join(documents[0]) if documents and documents[0] else ""

    # 2) Build prompt with context
    prompt = f"""
You are Ben's personal AI memory agent.

You have access to his past transcripts, notes, and digests.

CONTEXT (from Ben's memory):
{context}

USER MESSAGE:
{user_message}

Using ONLY the context when relevant, reply with a concise, helpful answer.
If the context doesn't contain anything useful, answer normally but say:
"(No relevant past memory found.)"
"""

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = completion.choices[0].message.content

    return {
        "context_used": context,
        "answer": answer
    }
