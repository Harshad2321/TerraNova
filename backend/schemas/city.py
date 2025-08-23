from pydantic import BaseModel

class CitySchema(BaseModel):
    name: str
    population: int
    area_km2: float
