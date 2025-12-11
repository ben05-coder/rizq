from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


# Response Models

class TranscriptData(BaseModel):
    """Transcript information"""
    text: str
    word_count: int
    duration: Optional[float] = None


class DigestData(BaseModel):
    """Structured digest information"""
    summary: str
    highlights: List[str]
    insights: List[str]
    action_items: List[str]
    questions: List[str]


class MemoryMetadata(BaseModel):
    """Memory metadata"""
    created_at: str
    filename: Optional[str] = None
    type: str = "audio_ingest"


class IngestResponseData(BaseModel):
    """Data returned from ingest endpoint"""
    memory_id: str
    transcript: TranscriptData
    digest: DigestData
    metadata: MemoryMetadata


class IngestResponse(BaseModel):
    """Response from /ingest endpoint"""
    success: bool
    data: IngestResponseData
    message: Optional[str] = None


class SearchSource(BaseModel):
    """Individual search result source"""
    id: str
    snippet: str
    relevance_score: Optional[float] = None


class SearchResponseData(BaseModel):
    """Data returned from search endpoint"""
    answer: str
    sources: List[SearchSource]
    query: str


class SearchResponse(BaseModel):
    """Response from /search endpoint"""
    success: bool
    data: SearchResponseData
    message: Optional[str] = None


class ChatResponseData(BaseModel):
    """Data returned from chat endpoint"""
    answer: str
    context_used: str
    sources_count: int


class ChatResponse(BaseModel):
    """Response from /chat endpoint"""
    success: bool
    data: ChatResponseData
    message: Optional[str] = None


class SmartNotesData(BaseModel):
    """Smart notes structure"""
    summary: str
    structured_notes: List[str]
    flashcards: List[Dict[str, str]]
    quizzes: List[str]
    eli12: str


class SmartNotesResponse(BaseModel):
    """Response from /smartnotes endpoint"""
    success: bool
    data: SmartNotesData
    message: Optional[str] = None


class TranscribeResponseData(BaseModel):
    """Data returned from transcribe endpoint"""
    text: str
    word_count: int


class TranscribeResponse(BaseModel):
    """Response from /transcribe endpoint"""
    success: bool
    data: TranscribeResponseData
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response format"""
    success: bool = False
    error: str
    details: Optional[str] = None


# Request Models (already exist as BaseModel in main.py, but documenting here)

class SmartNotesRequest(BaseModel):
    """Request for smartnotes endpoint"""
    text: str


class AskRequest(BaseModel):
    """Request for ask endpoint"""
    question: str
    content: str


class ChatRequest(BaseModel):
    """Request for chat endpoint"""
    message: str
