from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import random

app = FastAPI(title="TerraNova API")

# ----- SCHEMAS -----
class CityRequest(BaseModel):
    city_name: str
    population: int
    terrain: str
    eco_priority: int
    size: int

# ----- ENDPOINT -----
@app.post("/city/generate_plan")
def generate_plan(req: CityRequest):
    N = req.size
    grid = np.zeros((N, N), dtype=int)

    legend = {
        0: "EMPTY", 1: "WATER", 2: "MOUNTAIN", 3: "FARM", 4: "PARK",
        5: "HOME", 6: "OFFICE", 7: "HOSPITAL", 8: "SCHOOL",
        9: "METRO", 10: "STATION", 11: "WALK", 12: "ROAD"
    }

    # Example filling — coastline on top rows
    if req.terrain == "coastal":
        grid[0:5, :] = 1
    if req.terrain == "mountain":
        grid[:, -5:] = 2

    # Add random homes, parks, etc
    for _ in range(req.population // 100000):
        x, y = random.randint(0, N-1), random.randint(0, N-1)
        grid[y, x] = random.choice([5, 6, 7, 8, 4])

    # Add roads
    grid[N//2, :] = 12
    grid[:, N//3] = 12

    # Dummy metrics
    metrics = {
        "green_cover_pct": random.randint(20, 60),
        "walkability_index": random.randint(40, 90),
        "transit_coverage_pct": random.randint(30, 80),
        "renewable_potential": random.randint(50, 100),
        "est_co2_per_capita": round(random.uniform(3, 8), 2)
    }

    notes = [
        "Focus on public transit expansion.",
        "Increase renewable integration near coastline.",
        "Preserve green corridors."
    ]

    return {
        "plan_grid": grid.tolist(),
        "legend": legend,
        "metrics": metrics,
        "notes": notes
    }
