# backend/schemas/city.py
from pydantic import BaseModel
from typing import List, Dict, Any

class CityRequest(BaseModel):
    width: int
    height: int
    population: int

class CityResponse(BaseModel):
    layout: List[List[str]]
    recommendations: List[str]
