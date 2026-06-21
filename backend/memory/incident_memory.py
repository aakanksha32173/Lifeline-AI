import json
from memory.redis_client import redis_client
from schemas import IncidentCluster


CLUSTERS_KEY = "lifeline:incident_clusters"


def save_cluster(cluster: IncidentCluster):
    redis_client.hset(
        CLUSTERS_KEY,
        cluster.cluster_id,
        cluster.model_dump_json()
    )


def get_all_clusters() -> list[IncidentCluster]:
    data = redis_client.hgetall(CLUSTERS_KEY)
    clusters = []

    for value in data.values():
        clusters.append(IncidentCluster(**json.loads(value)))

    return clusters


def clear_memory():
    redis_client.delete(CLUSTERS_KEY)