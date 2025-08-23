from fastapi import APIRouter
from backend.schemas.city import CitySchema

router = APIRouter()

# Example city details
@router.get("/info")
def get_city_info():
    return {"city": "TerraNova", "population": 500000, "area_km2": 250}
