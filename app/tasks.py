from celery import Celery
from .config import REDIS_URL

celery_app = Celery("lead_triage", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(task_serializer="json", accept_content=["json"], result_serializer="json")

@celery_app.task(name="lead_triage.process_lead")
def process_lead(lead: dict) -> dict:
    from .classifier import classify_lead
    category, confidence = classify_lead(lead.get("message", ""))
    lead["category"] = category
    lead["confidence"] = confidence
    lead["status"] = "triaged"
    return lead

# Celery worker isolates lead triage from request latency.
