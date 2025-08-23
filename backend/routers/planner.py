from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

# ---------- INPUT MODEL ----------
class CityPlanRequest(BaseModel):
    city_name: str
    population: int
    area: float  # in sq km
    soil_type: str
    surroundings: str  # e.g., coastal, hilly, plain


# ---------- OUTPUT MODEL ----------
class CityPlanResponse(BaseModel):
    city_name: str
    population: int
    area: float
    soil_type: str
    surroundings: str
    feasible: bool
    summary: str
    recommendations: Dict[str, int]
    map_url: str


# ---------- HELPER FUNCTION ----------
def generate_plan(data: CityPlanRequest) -> CityPlanResponse:
    """Generate recommendations based on user input"""

    # Base recommendations
    recs = {
        "hospitals": max(1, data.population // 50000),
        "schools": max(2, data.population // 20000),
        "residential": max(5, data.area // 10),
        "offices": max(2, data.area // 25),
        "malls": max(1, data.population // 80000),
        "factories": 0,
        "police": max(1, data.population // 100000),
        "fire_stations": max(1, data.population // 120000),
        "railways": 0,
        "parks": max(1, int(data.area) // 20),
        "solar_plants": 1 if data.surroundings in ["coastal", "plain"] else 0,
        "wind_turbines": 1 if data.surroundings == "coastal" else 0,
    }

    # Adjustments based on soil
    if data.soil_type == "clay":
        recs["factories"] = 1
    elif data.soil_type == "rocky":
        recs["railways"] = 1

    # Feasibility
    feasible = data.population > 10000 and data.area > 10

    # Summary
    summary = (
        f"City {data.city_name} is planned with a population of {data.population} "
        f"and area {data.area} sq km. The soil is {data.soil_type}, "
        f"surrounded by {data.surroundings}. Recommended {recs['hospitals']} hospitals, "
        f"{recs['schools']} schools, {recs['parks']} parks, and {recs['offices']} office areas."
    )

    # Map placeholder (you can generate actual images later)
    map_url = f"maps/{data.city_name}_map.png"

    return CityPlanResponse(
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


# ---------- ROUTE ----------
@router.post("/plan", response_model=CityPlanResponse)
def plan_city(request: CityPlanRequest):
    return generate_plan(request)
