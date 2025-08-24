from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import random
import os

app = FastAPI(title="TerraNova API", version="1.0.0")

# CORS configuration for production
origins = [
    "http://localhost:3000",  # Local development
    "http://127.0.0.1:3000",  # Local development
    "https://*.vercel.app",   # Vercel deployments
    "https://*.netlify.app",  # Netlify deployments
    "https://*.github.io",    # GitHub Pages
    "*"  # Allow all origins for now (restrict in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ----- SCHEMAS -----
class CityRequest(BaseModel):
    city_name: str
    population: int
    terrain: str
    eco_priority: int
    size: int

# ----- ENDPOINTS -----
@app.get("/")
def read_root():
    return {"message": "TerraNova Backend is running!", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "TerraNova API"}
@app.post("/city/generate_plan")
def generate_plan(req: CityRequest):
    N = req.size
    grid = np.zeros((N, N), dtype=int)

    legend = {
        0: "EMPTY", 1: "WATER", 2: "MOUNTAIN", 3: "FARM", 4: "PARK",
        5: "HOME", 6: "OFFICE", 7: "HOSPITAL", 8: "SCHOOL",
        9: "METRO", 10: "STATION", 11: "WALK", 12: "ROAD"
    }

    # Initialize terrain based on type
    if req.terrain == "coastal":
        # Add coastline (water) on one edge
        coast_width = max(2, N // 10)
        grid[0:coast_width, :] = 1
        
    elif req.terrain == "mountain":
        # Add mountains on one side
        mountain_width = max(3, N // 8)
        grid[:, -mountain_width:] = 2
        
    elif req.terrain == "plains":
        # Add some farms around the edges
        farm_border = max(1, N // 15)
        grid[0:farm_border, :] = 3
        grid[-farm_border:, :] = 3
        grid[:, 0:farm_border] = 3
        grid[:, -farm_border:] = 3

    # Create main road network
    main_road_h = N // 2
    main_road_v = N // 3
    secondary_road_v = 2 * N // 3
    
    # Horizontal roads
    grid[main_road_h, :] = 12
    if N > 40:
        grid[N // 4, :] = 12
        grid[3 * N // 4, :] = 12
    
    # Vertical roads
    grid[:, main_road_v] = 12
    grid[:, secondary_road_v] = 12

    # Add residential areas (homes)
    density_factor = req.population // 1000000  # Adjust for population
    home_count = min(N * N // 10, density_factor * 50)
    
    for _ in range(home_count):
        x, y = random.randint(0, N-1), random.randint(0, N-1)
        if grid[y, x] == 0:  # Only place on empty land
            grid[y, x] = 5

    # Add commercial/office areas near roads
    office_count = home_count // 3
    for _ in range(office_count):
        x, y = random.randint(0, N-1), random.randint(0, N-1)
        # Place offices near roads
        if (abs(y - main_road_h) <= 2 or abs(x - main_road_v) <= 2 or abs(x - secondary_road_v) <= 2) and grid[y, x] == 0:
            grid[y, x] = 6

    # Add essential services
    services = [7, 8]  # Hospitals, Schools
    service_count = max(5, N // 10)
    
    for service_type in services:
        for _ in range(service_count):
            x, y = random.randint(0, N-1), random.randint(0, N-1)
            if grid[y, x] == 0:
                grid[y, x] = service_type

    # Add parks based on eco priority
    park_count = req.eco_priority * N // 8
    for _ in range(park_count):
        x, y = random.randint(0, N-1), random.randint(0, N-1)
        if grid[y, x] == 0:
            grid[y, x] = 4

    # Add metro stations and lines for larger cities
    if req.population > 5000000 and N > 50:
        metro_stations = min(8, N // 10)
        for _ in range(metro_stations):
            x, y = random.randint(N//4, 3*N//4), random.randint(N//4, 3*N//4)
            if grid[y, x] in [0, 12]:  # Place on empty or road
                grid[y, x] = 10
                # Add metro lines connecting stations
                if y > 0 and grid[y-1, x] == 0:
                    grid[y-1, x] = 9

    # Calculate realistic metrics based on the generated plan
    total_cells = N * N
    water_cells = np.count_nonzero(grid == 1)
    park_cells = np.count_nonzero(grid == 4)
    home_cells = np.count_nonzero(grid == 5)
    road_cells = np.count_nonzero(grid == 12)
    metro_cells = np.count_nonzero(grid == 9) + np.count_nonzero(grid == 10)
    
    green_cover = ((park_cells + np.count_nonzero(grid == 3)) / total_cells) * 100
    walkability = min(90, 30 + (road_cells / total_cells) * 200 + req.eco_priority * 5)
    transit_coverage = min(80, (metro_cells / max(1, home_cells)) * 500 + (road_cells / total_cells) * 100)
    renewable_potential = req.eco_priority * 8 + (20 if req.terrain == "coastal" else 10)
    co2_per_capita = max(2.0, 8.0 - req.eco_priority * 0.8 - (green_cover / 100) * 2)

    metrics = {
        "green_cover_pct": round(green_cover, 1),
        "walkability_index": round(walkability, 1),
        "transit_coverage_pct": round(transit_coverage, 1),
        "renewable_potential": round(renewable_potential, 1),
        "est_co2_per_capita": round(co2_per_capita, 2)
    }

    # Generate context-aware notes
    notes = []
    
    if green_cover < 25:
        notes.append("🌱 Increase green spaces - current coverage is below recommended 25%")
    elif green_cover > 40:
        notes.append("🌿 Excellent green coverage achieved!")
        
    if walkability < 60:
        notes.append("🚶 Improve walkability with more pedestrian paths and mixed-use development")
    
    if transit_coverage < 50:
        notes.append("🚇 Expand public transit network for better connectivity")
    
    if req.terrain == "coastal":
        notes.append("🌊 Leverage coastal location for renewable energy (wind/tidal)")
        notes.append("🏖️ Implement coastal protection measures")
    
    if req.eco_priority >= 8:
        notes.append("♻️ Prioritize circular economy and waste reduction initiatives")
        notes.append("⚡ Integrate smart grid technology for energy efficiency")
    
    if req.population > 10000000:
        notes.append("🏙️ Implement smart city IoT systems for traffic and resource management")

    return {
        "plan_grid": grid.tolist(),
        "legend": legend,
        "metrics": metrics,
        "notes": notes,
        "city_info": {
            "name": req.city_name,
            "population": req.population,
            "terrain": req.terrain,
            "size": f"{N}x{N}"
        }
    }
