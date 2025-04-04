from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class NoteInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)

class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    category: str
    created_at: datetime
    updated_at: datetime

class SearchQuery(BaseModel):
    keyword: str = Field(..., min_length=1)
    category: Optional[str] = None
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)

class SearchResponse(BaseModel):
    total: int
    page: int
    size: int
    results: List[NoteResponse]

class HealthCheck(BaseModel):
    status: str
    elasticsearch_status: str
    classifier_status: str 