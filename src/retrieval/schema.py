from pydantic import BaseModel
from typing import Optional

class RetrievedDoc(BaseModel):
    id: str
    doc_id: str
    text: str
    score: Optional[float] = None
    title: Optional[str] = None
    section: Optional[str] = None
    source: Optional[str] = None
    order: Optional[int] = None
    rerank_score: Optional[float] = None



