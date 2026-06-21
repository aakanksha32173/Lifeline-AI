from schemas import Incident


def calculate_priority(incidents: list[Incident]) -> int:
    score = 0

    for incident in incidents:
        score += incident.urgency * 8

        text = incident.raw_text.lower()

        if incident.medical_need:
            score += 25

        if "elderly" in text or "grandmother" in text or "grandfather" in text:
            score += 20

        if "child" in text or "baby" in text:
            score += 20

        if "trapped" in text or "stuck" in text:
            score += 20

        if "water rising" in text or "flood" in text:
            score += 15

    if len(incidents) > 1:
        score += min(len(incidents) * 5, 20)

    return min(score, 100)