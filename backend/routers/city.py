from fastapi import APIRouter
from backend.schemas.city import CityRequest, CityResponse
from backend.services.planner import evaluate_city

router = APIRouter()

@router.post("/plan", response_model=CityResponse)
async def plan_city(request: CityRequest):
    return evaluate_city(request)
from fastapi import APIRouter
from backend.services.planner import CityPlanRequest, CityPlanResponse, generate_city_layout

router = APIRouter()

@router.post("/plan", response_model=CityPlanResponse)
def plan_city(request: CityPlanRequest):
    return generate_city_layout(request)
