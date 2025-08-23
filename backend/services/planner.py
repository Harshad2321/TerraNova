# backend/services/planner.py
from backend.schemas.city import CityRequest, CityResponse

def generate_city_layout(request: CityRequest) -> CityResponse:
    """
    Generates a simple 2D city layout using symbols:
    - 🏡 = Home
    - 🏢 = Building
    - 🌳 = Park
    - 🛣️ = Road
    """
    grid = [["⬜" for _ in range(request.width)] for _ in range(request.height)]

    # Place parks
    for i in range(min(request.parks, request.width * request.height)):
        grid[i % request.height][i % request.width] = "🌳"

    # Place homes
    for i in range(request.homes):
        x, y = (i * 2) % request.width, (i * 3) % request.height
        grid[y][x] = "🏡"

    # Place buildings
    for i in range(request.buildings):
        x, y = (i * 3) % request.width, (i * 2) % request.height
        grid[y][x] = "🏢"

    # Place roads
    for i in range(request.roads):
        x, y = (i * 4) % request.width, (i * 5) % request.height
        grid[y][x] = "🛣️"

    return CityResponse(
        city=request.name,
        dimensions=f"{request.width}x{request.height}",
        parks=request.parks,
        homes=request.homes,
        roads=request.roads,
        buildings=request.buildings,
        visuals_enabled=request.visuals,
        layout=grid
    )
