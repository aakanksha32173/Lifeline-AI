import os
from typing import Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

geocoder = Nominatim(user_agent="lifeline-ai-crisis-management")


def geocode_location(location: str) -> Optional[Tuple[float, float]]:
    """
    Convert a location string to latitude and longitude coordinates.
    Returns (latitude, longitude) or None if geocoding fails.
    """
    if not location or location.strip() == "":
        return None
    
    try:
        time.sleep(0.1)
        location_data = geocoder.geocode(location, timeout=10)
        
        if location_data:
            return (location_data.latitude, location_data.longitude)
        
        return None
    
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error for '{location}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected geocoding error: {e}")
        return None


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points in kilometers using Haversine formula.
    """
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371.0
    
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance
