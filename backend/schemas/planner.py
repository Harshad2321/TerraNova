from pydantic import BaseModel
from typing import List, Dict, Optional

class Zone(BaseModel):
    id: str
    name: str
    coordinates: List[float]   # [lat, lon]
    capacity: Optional[int] = None

class Road(BaseModel):
    id: str
    type: str
    from_: str
    to: str
    length_km: float

class Amenity(BaseModel):
    id: str
    type: str
    name: str
    coordinates: List[float]

class Infrastructure(BaseModel):
    river: bool
    railway_station: bool
    airports: int
    metro_lines: int

class CityRequest(BaseModel):
    city_name: str
    population: int
    river: bool
    railway_station: bool
    parks: int
    buildings: int

class CityPlan(BaseModel):
    city_name: str
    population: int
    zones: Dict[str, List[Zone]]
    roads: List[Road]
    public_amenities: List[Amenity]
    infrastructure: Infrastructure
