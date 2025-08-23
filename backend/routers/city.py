from fastapi import APIRouter
from backend.schemas import CityRequest, CityPlan, PlanMetrics
from backend.services.planner import build_plan

router = APIRouter()

@router.post("/generate_plan", response_model=CityPlan)
def generate_plan(req: CityRequest):
    plan = build_plan(
        size=req.size,
        terrain_kind=req.terrain,
        population=req.population,
        eco_priority=req.eco_priority,
        seed=42
    )
    return CityPlan(
        legend=plan["legend"],
        size=plan["size"],
        terrain_grid=plan["terrain_grid"],
        plan_grid=plan["plan_grid"],
        metrics=PlanMetrics(**plan["metrics"]),
        notes=plan["notes"]
    )
