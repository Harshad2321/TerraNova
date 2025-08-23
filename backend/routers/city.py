# backend/routers/city.py
from fastapi import APIRouter
from backend.schemas.city import CityRequest, CityResponse
from backend.services.planner import generate_city_layout

router = APIRouter()

@router.post("/plan", response_model=CityResponse)
async def plan_city(request: CityRequest):
    return generate_city_layout(request)
