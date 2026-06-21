from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class RawEvent(BaseModel):
    source: str
    text: str
    location: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}


class Incident(BaseModel):
    incident_id: str
    event_type: str
    description: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    urgency: int
    people_affected: Optional[int] = 1
    medical_need: Optional[str] = None
    source: str
    confidence: float
    raw_text: str


class IncidentCluster(BaseModel):
    cluster_id: str
    incidents: List[Incident]
    summary: str
    priority_score: int
    recommended_action: str
    confidence: float
    cluster_color: Optional[str] = "#3b82f6"
    event_category: Optional[str] = "general"