from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import RawEvent
from agents.asi_coordinator import process_raw_event
from memory.incident_memory import get_all_clusters, clear_memory

app = FastAPI(title="Lifeline AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Lifeline AI backend running"}


@app.post("/events/process")
def process_event(event: RawEvent):
    return process_raw_event(event)


@app.get("/clusters")
def clusters():
    return get_all_clusters()


@app.get("/priority-queue")
def priority_queue():
    clusters = get_all_clusters()
    clusters.sort(key=lambda c: c.priority_score, reverse=True)
    return clusters


@app.delete("/memory")
def reset_memory():
    clear_memory()
    return {"message": "Memory cleared"}