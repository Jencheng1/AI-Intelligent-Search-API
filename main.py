from fastapi import FastAPI, HTTPException, Depends
from elasticsearch import Elasticsearch
from datetime import datetime
import uuid
from typing import List
import os
from dotenv import load_dotenv

from models import NoteInput, NoteResponse, SearchQuery, SearchResponse, HealthCheck
from classifier import NoteClassifier

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Notes Search & Classification API",
    description="API for storing, searching, and classifying notes using FastAPI and Elasticsearch",
    version="1.0.0"
)

# Initialize Elasticsearch client
es = Elasticsearch(
    os.getenv("ELASTICSEARCH_URL", "http://localhost:9200"),
    basic_auth=(os.getenv("ELASTICSEARCH_USER", "admin"), 
                os.getenv("ELASTICSEARCH_PASSWORD", "admin"))
)

# Initialize classifier
classifier = NoteClassifier()

# Create index if it doesn't exist
INDEX_NAME = "notes"
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(
        index=INDEX_NAME,
        mappings={
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "category": {"type": "keyword"},
                "created_at": {"type": "date"},
                "updated_at": {"type": "date"}
            }
        }
    )

@app.post("/notes", response_model=NoteResponse)
async def add_note(note: NoteInput):
    """Add a new note and classify it."""
    try:
        # Classify the note
        category = classifier.classify(note.content)
        
        # Create note document
        note_doc = {
            "id": str(uuid.uuid4()),
            "title": note.title,
            "content": note.content,
            "category": category,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Store in Elasticsearch
        es.index(index=INDEX_NAME, id=note_doc["id"], document=note_doc)
        
        return note_doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search", response_model=SearchResponse)
async def search_notes(
    keyword: str,
    category: str = None,
    page: int = 1,
    size: int = 10
):
    """Search notes by keyword and optionally filter by category."""
    try:
        # Build search query
        query = {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": keyword,
                            "fields": ["title^2", "content"]
                        }
                    }
                ]
            }
        }
        
        # Add category filter if specified
        if category:
            query["bool"]["filter"] = [{"term": {"category": category}}]
        
        # Execute search
        result = es.search(
            index=INDEX_NAME,
            query=query,
            from_=(page - 1) * size,
            size=size
        )
        
        # Format response
        hits = result["hits"]["hits"]
        notes = [hit["_source"] for hit in hits]
        
        return {
            "total": result["hits"]["total"]["value"],
            "page": page,
            "size": size,
            "results": notes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Check the health of the API and its dependencies."""
    try:
        # Check Elasticsearch
        es_status = "healthy" if es.ping() else "unhealthy"
        
        # Check classifier
        classifier_status = "healthy"
        try:
            classifier.classify("test")
        except Exception:
            classifier_status = "unhealthy"
        
        return {
            "status": "healthy" if es_status == "healthy" and classifier_status == "healthy" else "unhealthy",
            "elasticsearch_status": es_status,
            "classifier_status": classifier_status
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "elasticsearch_status": "error",
            "classifier_status": "error"
        }

@app.get("/categories")
async def get_categories():
    """Get list of available categories."""
    return {"categories": classifier.categories} 