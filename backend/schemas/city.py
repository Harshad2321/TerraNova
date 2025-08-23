from pydantic import BaseModel

class CityRequest(BaseModel):
    city_name: str
    population: int
    area: float  # in square km
    soil_type: str
    surroundings: str

class CityResponse(BaseModel):
    feasible: bool
    summary: str
    recommendations: dict
    map_url: str
