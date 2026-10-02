from pydantic import BaseModel, Field, HttpUrl

class ContentIn(BaseModel):
    content_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=2, max_length=240)
    body: str = Field(min_length=1, max_length=100000)
    url: HttpUrl | None = None
    updated_at: str | None = None

class LeadIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=3, max_length=254)
    message: str = Field(min_length=5, max_length=5000)
    source: str = Field(default="website", max_length=80)

class LeadOut(BaseModel):
    lead_id: str
    category: str
    confidence: float
    status: str
