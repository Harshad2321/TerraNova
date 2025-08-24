from pydantic import BaseModel, Field
from typing import Dict, List

class CityRequest(BaseModel):
    city_name: str = Field(..., example="Neo Greenfield")
    population: int = Field(..., example=13_000_000)
    terrain: str = Field(..., example="coastal")  # coastal | plains | mountain
    eco_priority: int = Field(..., ge=1, le=10, example=9)
    size: int = Field(60, ge=36, le=96, example=60)

class PlanMetrics(BaseModel):
    green_cover_pct: float
    walkability_index: float
    renewable_potential: float
    est_co2_per_capita: float
    transit_coverage_pct: float

class CityPlan(BaseModel):
    legend: Dict[str, int]
    size: int
    terrain_grid: List[List[int]]
    plan_grid: List[List[int]]
    metrics: PlanMetrics
    notes: List[str]
