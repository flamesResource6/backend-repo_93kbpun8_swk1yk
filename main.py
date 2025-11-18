import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, get_documents, create_document
from schemas import Gift

app = FastAPI(title="Gift Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GiftCreate(BaseModel):
    gift: str
    background: str
    pattern: str
    number: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    tags: Optional[List[str]] = None


@app.get("/")
def read_root():
    return {"message": "Gift Search Backend Running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


@app.get("/api/gifts")
def search_gifts(
    gift: Optional[str] = Query(None, description="Gift type"),
    background: Optional[str] = Query(None, description="Background"),
    pattern: Optional[str] = Query(None, description="Pattern"),
    number: Optional[str] = Query(None, description="Number"),
    q: Optional[str] = Query(None, description="Free text search in title/description/tags"),
    limit: int = Query(24, ge=1, le=100)
):
    """Search gifts by filters. All parameters are optional."""
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    filter_dict = {}
    if gift:
        filter_dict["gift"] = gift
    if background:
        filter_dict["background"] = background
    if pattern:
        filter_dict["pattern"] = pattern
    if number:
        filter_dict["number"] = number

    if q:
        # Case-insensitive regex search on title/description/tags
        regex = {"$regex": q, "$options": "i"}
        filter_dict["$or"] = [
            {"title": regex},
            {"description": regex},
            {"tags": regex},
        ]

    docs = get_documents("gift", filter_dict, limit)

    # Convert ObjectId to string
    def normalize(doc):
        doc["id"] = str(doc.get("_id"))
        doc.pop("_id", None)
        return doc

    return [normalize(d) for d in docs]


@app.post("/api/gifts")
def create_gift(payload: GiftCreate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    data = payload.model_dump()
    inserted_id = create_document("gift", data)
    return {"id": inserted_id}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
