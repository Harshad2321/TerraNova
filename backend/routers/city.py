from fastapi import APIRouter, Response
from backend.schemas.city import CityRequest, CityResponse
from backend.services.planner import generate_city_layout
from backend.services.map_generator import get_city_map_url
from typing import Dict, List
import os
import json
import logging

logger = logging.getLogger("terranova")
router = APIRouter()

@router.post("/plan", response_model=Dict)
async def plan_city(request: dict):
    """
    Plan a city based on width, height, and population
    This endpoint is for frontend grid-based visualization
    """
    width = int(request.get("width", 10))
    height = int(request.get("height", 10)) 
    population = int(request.get("population", 1000))
    name = request.get("name", "NeoCity")
    
    # Generate a simple grid layout
    layout = []
    
    # City planning symbols
    symbols = ["R", "H", "B", "P", "M", "G"]  # Road, Home, Building, Park, Market, Government
    
    # Create a grid based on population density
    density = min(0.8, max(0.2, population / (width * height * 1000)))
    
    import random
    for i in range(height):
        row = []
        for j in range(width):
            # More buildings in center, more parks at edges
            center_distance = ((i - height/2)**2 + (j - width/2)**2)**0.5
            is_center = center_distance < min(width, height)/3
            
            # Create a more structured road network with about 15% roads
            is_road = (i % 3 == 0 or j % 3 == 0) and random.random() < 0.75
            
            if is_road:  # Better structured roads
                row.append("R")
            elif random.random() < density and is_center:  # Buildings in center
                row.append(random.choice(["B", "M", "G"]))
            elif random.random() < 0.7 * density:  # Homes
                row.append("H")
            elif random.random() < 0.3:  # Reduced chance of parks
                row.append("P")
            else:  # Default to houses for remaining spaces
                row.append("H")
        layout.append(row)
    
    # Generate recommendations based on population
    recommendations = [
        f"Build {max(1, population // 50000)} hospitals",
        f"Establish {max(2, population // 20000)} schools",
        f"Create {max(1, population // 100000)} police stations",
        f"Include {max(3, width * height // 25)} parks and green spaces",
        f"Plan for {max(1, population // 40000)} shopping centers"
    ]
    
    try:
        # Generate a visual map using our map generator service
        map_url = get_city_map_url(layout, name)
        logger.info(f"Generated visual map for {name} at {map_url}")
        
        # Map generation successful
        visual_map_available = True
    except Exception as e:
        # If map generation fails, we still return the grid layout
        logger.error(f"Error generating visual map: {str(e)}")
        map_url = None
        visual_map_available = False
    
    return {
        "name": name,
        "population": population,
        "width": width,
        "height": height,
        "layout": layout,
        "recommendations": recommendations,
        "plan": layout,  # For backward compatibility with tests
        "map_url": map_url,
        "visual_map_available": visual_map_available
    }

# Example city details
@router.get("/info")
def get_city_info():
    return {"city": "TerraNova", "population": 500000, "area_km2": 250}
