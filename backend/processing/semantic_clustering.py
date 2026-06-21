import os
from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
from dotenv import load_dotenv

load_dotenv()

ASI_ONE_API_KEY = os.getenv("ASI_ONE_API_KEY")


def get_embedding(text: str) -> List[float]:
    """
    Get embedding vector for text using ASI:One API.
    Falls back to simple text comparison if API fails.
    """
    try:
        response = requests.post(
            "https://api.asi1.ai/v1/embeddings",
            headers={
                "Authorization": f"Bearer {ASI_ONE_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "asi1-embedding",
                "input": text
            },
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]["embedding"]
        else:
            print("No embedding data in response, using fallback")
            return _get_fallback_embedding(text)
            
    except Exception as e:
        print(f"Error getting ASI:One embedding: {e}, using fallback")
        return _get_fallback_embedding(text)


def _get_fallback_embedding(text: str) -> List[float]:
    """
    Simple fallback embedding based on text features.
    Used when ASI:One API is unavailable.
    """
    import hashlib
    
    text_lower = text.lower()
    embedding = [0.0] * 384
    
    keywords = {
        "medical": [1, 50, 100],
        "emergency": [2, 51, 101],
        "rescue": [3, 52, 102],
        "flood": [4, 53, 103],
        "water": [5, 54, 104],
        "fire": [6, 55, 105],
        "trapped": [7, 56, 106],
        "help": [8, 57, 107],
        "urgent": [9, 58, 108],
        "oxygen": [10, 59, 109],
        "insulin": [11, 60, 110],
        "shelter": [12, 61, 111],
        "power": [13, 62, 112],
        "outage": [14, 63, 113],
    }
    
    for keyword, indices in keywords.items():
        if keyword in text_lower:
            for idx in indices:
                embedding[idx] = 1.0
    
    hash_val = int(hashlib.md5(text_lower.encode()).hexdigest(), 16)
    for i in range(20):
        embedding[200 + i] = ((hash_val >> i) & 1) * 0.5
    
    return embedding


def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts using embeddings.
    Returns a score between 0 and 1, where 1 is most similar.
    """
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    
    emb1_array = np.array(emb1).reshape(1, -1)
    emb2_array = np.array(emb2).reshape(1, -1)
    
    similarity = cosine_similarity(emb1_array, emb2_array)[0][0]
    
    return float(similarity)


def should_cluster_together(
    incident1_text: str,
    incident2_text: str,
    incident1_location: str = None,
    incident2_location: str = None,
    incident1_coords: tuple = None,
    incident2_coords: tuple = None,
    semantic_threshold: float = 0.75,
    distance_threshold_km: float = 5.0
) -> bool:
    """
    Determine if two incidents should be clustered together based on:
    1. Semantic similarity of descriptions
    2. Geographic proximity
    """
    from processing.geocoding import calculate_distance
    
    semantic_score = calculate_semantic_similarity(incident1_text, incident2_text)
    
    if semantic_score < semantic_threshold:
        return False
    
    if incident1_coords and incident2_coords:
        distance = calculate_distance(
            incident1_coords[0], incident1_coords[1],
            incident2_coords[0], incident2_coords[1]
        )
        
        if distance > distance_threshold_km:
            return False
    
    elif incident1_location and incident2_location:
        if incident1_location.lower() != incident2_location.lower():
            return False
    
    return True
