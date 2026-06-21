import os
import requests
from dotenv import load_dotenv

load_dotenv()

ASI_ONE_API_KEY = os.getenv("ASI_ONE_API_KEY")


def ask_asi_one(user_message: str, location: str, resources: list):
    """
    Replace the URL/model fields with the current ASI:One docs values.
    """

    prompt = f"""
You are Lifeline AI, a crisis resource navigator.

User message:
{user_message}

User location:
{location}

Verified resources:
{resources}

Create a simple Plan A, Plan B, and Plan C.
Be practical. Do not diagnose. Include emergency escalation language when appropriate.
"""

    # PSEUDOCODE API call.
    # Update base_url/model based on ASI:One dashboard/docs.
    response = requests.post(
        "https://api.asi1.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {ASI_ONE_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "asi1-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a safe crisis-navigation assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        },
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]