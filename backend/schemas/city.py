# backend/schemas/city.py
from pydantic import BaseModel
from typing import List, Optional

class CityRequest(BaseModel):
    name: str
    width: int
    height: int
    parks: Optional[int] = 1
    homes: Optional[int] = 5
    roads: Optional[int] = 3
    buildings: Optional[int] = 2
    visuals: Optional[bool] = True


class CityResponse(BaseModel):
    city: str
    dimensions: str
    parks: int
    homes: int
    roads: int
    buildings: int
    visuals_enabled: bool
    layout: List[List[str]]   # 2D grid layout
