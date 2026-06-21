import uuid
from schemas import RawEvent, Incident
from processing.geocoding import geocode_location


def extract_incident(raw_event: RawEvent) -> Incident:
    text = raw_event.text.lower()

    event_type = "general_alert"
    urgency = 3
    medical_need = None

    if "oxygen" in text or "insulin" in text or "dialysis" in text:
        event_type = "medical_emergency"
        urgency = 9
        if "oxygen" in text:
            medical_need = "oxygen"
        elif "insulin" in text:
            medical_need = "insulin"

    elif "trapped" in text or "stuck" in text or "rescue" in text:
        event_type = "rescue_request"
        urgency = 8

    elif "flood" in text or "water rising" in text:
        event_type = "flooding"
        urgency = 7

    elif "power outage" in text or "no power" in text:
        event_type = "power_outage"
        urgency = 5

    elif "shelter" in text:
        event_type = "shelter_update"
        urgency = 4

    latitude = None
    longitude = None
    if raw_event.location:
        coords = geocode_location(raw_event.location)
        if coords:
            latitude, longitude = coords

    return Incident(
        incident_id=str(uuid.uuid4()),
        event_type=event_type,
        description=raw_event.text,
        location=raw_event.location,
        latitude=latitude,
        longitude=longitude,
        urgency=urgency,
        people_affected=1,
        medical_need=medical_need,
        source=raw_event.source,
        confidence=0.85,
        raw_text=raw_event.text
    )