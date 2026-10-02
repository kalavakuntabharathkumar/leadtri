import json
from uuid import uuid4
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from .auth import require_api_key
from .schemas import ContentIn, LeadIn, LeadOut
from .storage import mongo_db, redis_client, cache_key
from .classifier import classify_lead
from .tasks import process_lead

app = FastAPI(title="Async Content and Lead-Triage API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.put("/api/content/{content_id}")
def sync_content(content_id: str, content: ContentIn, _: bool = Depends(require_api_key)):
    if content.content_id != content_id:
        raise HTTPException(400, "Path content_id must match payload")
    document = content.model_dump(mode="json")
    try:
        mongo_db().content.update_one({"content_id": content_id}, {"$set": document}, upsert=True)
        redis_client().set(cache_key(content_id), json.dumps(document), ex=300)
    except Exception as exc:
        raise HTTPException(503, "Content storage unavailable") from exc
    return {"content_id": content_id, "synced": True, "cache_ttl_seconds": 300}

@app.get("/api/content/{content_id}")
def get_content(content_id: str, _: bool = Depends(require_api_key)):
    try:
        cached = redis_client().get(cache_key(content_id))
        if cached:
            return {"source": "cache", "content": json.loads(cached)}
        document = mongo_db().content.find_one({"content_id": content_id}, {"_id": 0})
        if not document:
            raise HTTPException(404, "Content not found")
        redis_client().set(cache_key(content_id), json.dumps(document, default=str), ex=300)
        return {"source": "mongodb", "content": document}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(503, "Content storage unavailable") from exc

@app.post("/api/leads", response_model=LeadOut, status_code=202)
def create_lead(lead: LeadIn, background_tasks: BackgroundTasks, _: bool = Depends(require_api_key)):
    lead_id = str(uuid4())
    record = lead.model_dump()
    record["lead_id"] = lead_id
    category, confidence = classify_lead(lead.message)
    result = {"lead_id": lead_id, "category": category, "confidence": confidence, "status": "queued"}
    try:
        # Store immediately for auditability; Celery handles follow-up processing asynchronously.
        mongo_db().leads.insert_one({**record, **result})
        task = process_lead.delay(record)
        result["task_id"] = task.id
    except Exception:
        # Keep the endpoint useful in local tests even when the worker/broker isn't running.
        background_tasks.add_task(classify_lead, lead.message)
    return result

@app.get("/api/leads/{lead_id}")
def get_lead(lead_id: str, _: bool = Depends(require_api_key)):
    try:
        lead = mongo_db().leads.find_one({"lead_id": lead_id}, {"_id": 0})
        if not lead:
            raise HTTPException(404, "Lead not found")
        return lead
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(503, "Lead storage unavailable") from exc
