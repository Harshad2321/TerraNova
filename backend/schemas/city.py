from pydantic import BaseModel
from typing import Dict, List, Optional

class CityRequest(BaseModel):
    """Schema for basic city request with width/height/population"""
    name: Optional[str] = "NeoCity"
    width: int = 10
    height: int = 10
    population: int = 1000

class CityResponse(BaseModel):
    """Schema for grid-based city response"""
    name: str
    population: int
    width: int
    height: int
    layout: List[List[str]]
    recommendations: List[str]
    plan: List[List[str]]  # For backwards compatibility

class DetailedCityRequest(BaseModel):
    """Schema for detailed city planning request"""
    city_name: str
    population: int
    area: float  # in square km
    soil_type: str
    surroundings: str

class DetailedCityResponse(BaseModel):
    """Schema for detailed city planning response"""
    city_name: str
    population: int
    area: float
    soil_type: str
    surroundings: str
    feasible: bool
    summary: str
    recommendations: Dict[str, int]
    map_url: str
