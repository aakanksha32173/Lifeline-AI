from schemas import IncidentCluster
from asi_client import ask_asi_one


def generate_recommendation(cluster: IncidentCluster) -> str:
    """
    Generate intelligent recommendations using ASI:One API.
    Falls back to rule-based recommendations if API fails.
    """
    event_types = [i.event_type for i in cluster.incidents]
    location = cluster.incidents[0].location or "unknown location"
    
    incident_descriptions = "\n".join([
        f"- {inc.description} (urgency: {inc.urgency}, type: {inc.event_type})"
        for inc in cluster.incidents
    ])
    
    user_message = f"""
Crisis Cluster Analysis:
Location: {location}
Number of related incidents: {len(cluster.incidents)}
Priority Score: {cluster.priority_score}

Incident Details:
{incident_descriptions}

Provide a concise, actionable recommendation for emergency responders.
"""
    
    try:
        recommendation = ask_asi_one(
            user_message=user_message,
            location=location,
            resources=[]
        )
        return recommendation
    except Exception as e:
        print(f"ASI:One API error, using fallback: {e}")
        return generate_fallback_recommendation(cluster)


def generate_fallback_recommendation(cluster: IncidentCluster) -> str:
    """
    Rule-based fallback recommendation when ASI:One API is unavailable.
    """
    event_types = [i.event_type for i in cluster.incidents]
    location = cluster.incidents[0].location or "unknown location"

    has_medical = any(i.medical_need for i in cluster.incidents)
    has_rescue = any(i.event_type == "rescue_request" for i in cluster.incidents)
    has_flood = any(i.event_type == "flooding" for i in cluster.incidents)

    if has_medical and has_rescue:
        return f"Dispatch medical rescue to {location} immediately. Medical need and rescue request detected."

    if has_rescue:
        return f"Prioritize rescue response near {location}. Multiple signs of people needing help."

    if has_medical:
        return f"Send medical support to {location}. Medical resource need detected."

    if has_flood:
        return f"Monitor and warn residents near {location}. Flooding risk is increasing."

    return f"Review incident near {location} and assign appropriate response team."