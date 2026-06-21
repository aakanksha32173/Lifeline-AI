from schemas import RawEvent
from processing.incident_extractor import extract_incident
from processing.incident_fusion import fuse_incident
from memory.incident_memory import get_all_clusters, save_cluster


def process_raw_event(raw_event: RawEvent):
    incident = extract_incident(raw_event)

    existing_clusters = get_all_clusters()

    cluster = fuse_incident(incident, existing_clusters)

    save_cluster(cluster)

    return {
        "incident": incident,
        "cluster": cluster,
        "recommendation": cluster.recommended_action
    }