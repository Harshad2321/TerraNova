# backend/services/planner.py
import random
from backend.schemas.city import CityRequest, CityResponse

def generate_city_layout(request: CityRequest) -> CityResponse:
    width, height = request.width, request.height
    layout = [["empty" for _ in range(width)] for _ in range(height)]
    recommendations = []

    # Place residential areas
    for _ in range(request.population // 100):
        x, y = random.randint(0, height - 1), random.randint(0, width - 1)
        layout[x][y] = "residential"

    # Place commercial areas
    for _ in range(max(1, request.population // 300)):
        x, y = random.randint(0, height - 1), random.randint(0, width - 1)
        layout[x][y] = "commercial"

    # Place schools
    school_count = max(1, request.population // 500)
    for _ in range(school_count):
        x, y = random.randint(0, height - 1), random.randint(0, width - 1)
        layout[x][y] = "school"
    recommendations.append(f"Schools needed: {school_count}")

    # Place hospitals
    hospital_count = max(1, request.population // 1000)
    for _ in range(hospital_count):
        x, y = random.randint(0, height - 1), random.randint(0, width - 1)
        layout[x][y] = "hospital"
    recommendations.append(f"Hospitals needed: {hospital_count}")

    # Place parks
    park_count = max(1, (width * height) // 50)
    for _ in range(park_count):
        x, y = random.randint(0, height - 1), random.randint(0, width - 1)
        layout[x][y] = "park"
    recommendations.append(f"Parks for sustainability: {park_count}")

    # Soil quality check
    soil_quality = random.choice(["good", "average", "poor"])
    if soil_quality == "good":
        recommendations.append("Soil quality is good for building.")
    elif soil_quality == "average":
        recommendations.append("Soil quality is average. Suitable with reinforcement.")
    else:
        recommendations.append("Soil quality is poor. Avoid heavy construction here.")

    return CityResponse(layout=layout, recommendations=recommendations)
