from backend.schemas.city import DetailedCityRequest, DetailedCityResponse
from typing import Dict
import os

def generate_city_layout(data: DetailedCityRequest) -> DetailedCityResponse:
    """
    Generate city planning recommendations and feasibility analysis
    
    Args:
        data: DetailedCityRequest containing city parameters
        
    Returns:
        DetailedCityResponse with recommendations and analysis
    """
    # Ensure the city name is valid for a filename
    city_name = ''.join(c if c.isalnum() else '_' for c in data.city_name)
    
    # Base recommendations based on population and area
    recs = {
        "hospitals": max(1, data.population // 50000),
        "schools": max(2, data.population // 20000),
        "residential_zones": max(5, int(data.area) // 10),
        "office_buildings": max(2, int(data.area) // 25),
        "shopping_malls": max(1, data.population // 80000),
        "factories": 0,
        "police_stations": max(1, data.population // 100000),
        "fire_stations": max(1, data.population // 120000),
        "railway_stations": 0,
        "parks": max(1, int(data.area) // 20),
        "solar_plants": 1 if data.surroundings.lower() in ["coastal", "plain"] else 0,
        "wind_turbines": 1 if data.surroundings.lower() == "coastal" else 0,
    }

    # Adjustments based on soil type
    soil_type = data.soil_type.lower()
    if soil_type == "clay":
        recs["factories"] += 1
        recs["parks"] += 1
    elif soil_type == "rocky":
        recs["railway_stations"] += 1
        recs["solar_plants"] += 1
    elif soil_type == "sandy":
        recs["parks"] -= 1 if recs["parks"] > 1 else 0
        recs["residential_zones"] -= 1 if recs["residential_zones"] > 2 else 0
    elif soil_type == "loamy":
        recs["parks"] += 2
        recs["residential_zones"] += 1
    
    # Adjustments based on surroundings
    surroundings = data.surroundings.lower()
    if surroundings == "hilly":
        recs["parks"] += 1
        recs["residential_zones"] -= 1 if recs["residential_zones"] > 2 else 0
    elif surroundings == "forest":
        recs["parks"] += 2
        recs["factories"] -= 1 if recs["factories"] > 0 else 0

    # Feasibility rules
    feasible = data.population > 10000 and data.area > 10
    
    # Check for special cases that might make it infeasible
    if data.population > 500000 and data.area < 50:
        feasible = False  # Too dense
    if soil_type == "rocky" and data.population > 200000:
        feasible = False  # Rocky terrain can't support very large populations
        
    # Summary string
    summary = (
        f"City {data.city_name} is planned with a population of {data.population:,} "
        f"and area {data.area} sq km. The soil is {data.soil_type}, "
        f"surrounded by {data.surroundings} terrain. "
        f"Recommended {recs['hospitals']} hospitals, "
        f"{recs['schools']} schools, {recs['parks']} parks, and {recs['office_buildings']} office buildings."
    )
    
    if not feasible:
        if data.population > 500000 and data.area < 50:
            summary += " The city plan may not be feasible due to excessive population density."
        elif soil_type == "rocky" and data.population > 200000:
            summary += " The rocky terrain may not support such a large population."
        else:
            summary += " The city plan may not be feasible due to inadequate area or population."

    # Use placeholder map image
    # In a real app, we would generate a custom map here
    map_url = "/maps/NeoCity_map.png"
    
    return DetailedCityResponse(
        city_name=data.city_name,
        population=data.population,
        area=data.area,
        soil_type=data.soil_type,
        surroundings=data.surroundings,
        feasible=feasible,
        summary=summary,
        recommendations=recs,
        map_url=map_url,
    )
