import uuid
from schemas import Incident, IncidentCluster
from processing.priority_scorer import calculate_priority
from processing.recommendation_engine import generate_recommendation
from processing.semantic_clustering import should_cluster_together


def get_cluster_color(event_type: str) -> str:
    """
    Assign color based on event category for visual clustering.
    """
    color_map = {
        "medical_emergency": "#ef4444",
        "rescue_request": "#f97316",
        "flooding": "#3b82f6",
        "power_outage": "#eab308",
        "shelter_update": "#22c55e",
        "general_alert": "#6366f1"
    }
    return color_map.get(event_type, "#6366f1")


def get_event_category(event_type: str) -> str:
    """
    Get broader category for event type.
    """
    category_map = {
        "medical_emergency": "medical",
        "rescue_request": "rescue",
        "flooding": "environmental",
        "power_outage": "infrastructure",
        "shelter_update": "shelter",
        "general_alert": "general"
    }
    return category_map.get(event_type, "general")


def fuse_incident(new_incident: Incident, existing_clusters: list[IncidentCluster]) -> IncidentCluster:
    """
    Fuse incident into existing cluster using semantic similarity and geographic proximity,
    or create new cluster if no match found.
    """
    new_coords = None
    if new_incident.latitude and new_incident.longitude:
        new_coords = (new_incident.latitude, new_incident.longitude)
    
    for cluster in existing_clusters:
        for old_incident in cluster.incidents:
            old_coords = None
            if old_incident.latitude and old_incident.longitude:
                old_coords = (old_incident.latitude, old_incident.longitude)
            
            if should_cluster_together(
                new_incident.raw_text,
                old_incident.raw_text,
                new_incident.location,
                old_incident.location,
                new_coords,
                old_coords,
                semantic_threshold=0.70,
                distance_threshold_km=5.0
            ):
                cluster.incidents.append(new_incident)
                cluster.priority_score = calculate_priority(cluster.incidents)
                cluster.summary = summarize_cluster(cluster.incidents)
                cluster.recommended_action = generate_recommendation(cluster)
                return cluster

    new_cluster = IncidentCluster(
        cluster_id=str(uuid.uuid4()),
        incidents=[new_incident],
        summary=summarize_cluster([new_incident]),
        priority_score=calculate_priority([new_incident]),
        recommended_action="",
        confidence=new_incident.confidence,
        cluster_color=get_cluster_color(new_incident.event_type),
        event_category=get_event_category(new_incident.event_type)
    )

    new_cluster.recommended_action = generate_recommendation(new_cluster)
    return new_cluster


def summarize_cluster(incidents: list[Incident]) -> str:
    location = incidents[0].location or "Unknown location"
    types = list(set([i.event_type for i in incidents]))
    return f"{len(incidents)} related reports near {location}: {', '.join(types)}"