from fastapi import APIRouter
from backend.schemas.planner import CityRequest, CityPlan
import folium
import os

router = APIRouter()

# Directory where maps will be saved
MAPS_DIR = "generated_maps"
os.makedirs(MAPS_DIR, exist_ok=True)


@router.post("/plan", response_model=CityPlan)
def create_plan(request: CityRequest):
    """
    Returns a simple JSON city plan
    """
    return CityPlan(
        city_name=request.city_name,
        roads=["Main Road", "Ring Road"],
        residential_zones=["Sector-1", "Sector-2"],
        commercial_zones=["Market Square"],
        public_amenities=[
            "Park-1",
            "Railway Station" if request.railway_station else None,
            "Riverfront" if request.river else None
        ]
    )


@router.post("/plan/map")
def create_plan_with_map(request: CityRequest):
    """
    Returns a JSON city plan and generates a Folium map with markers
    """
    # Build the plan
    plan = CityPlan(
        city_name=request.city_name,
        roads=["Main Road", "Ring Road"],
        residential_zones=["Sector-1", "Sector-2"],
        commercial_zones=["Market Square"],
        public_amenities=[
            "Park-1",
            "Railway Station" if request.railway_station else None,
            "Riverfront" if request.river else None
        ]
    )

    # Create a Folium map centered on India (example)
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=6)

    # Add markers
    folium.Marker(
        [20.60, 78.96],
        tooltip="Main Road",
        icon=folium.Icon(color="blue", icon="road", prefix="fa")
    ).add_to(m)

    if request.railway_station:
        folium.Marker(
            [20.61, 78.97],
            tooltip="Railway Station",
            icon=folium.Icon(color="red", icon="train", prefix="fa")
        ).add_to(m)

    if request.river:
        folium.Marker(
            [20.62, 78.94],
            tooltip="Riverfront",
            icon=folium.Icon(color="cadetblue", icon="tint", prefix="fa")
        ).add_to(m)

    # Parks
    for i in range(request.parks):
        folium.Marker(
            [20.63 + i * 0.01, 78.95 + i * 0.01],
            tooltip=f"Park-{i+1}",
            icon=folium.Icon(color="green", icon="tree", prefix="fa")
        ).add_to(m)

    # Commercial
    folium.Marker(
        [20.64, 78.96],
        tooltip="Market Square",
        icon=folium.Icon(color="orange", icon="shopping-cart", prefix="fa")
    ).add_to(m)

    # Save map
    map_path = os.path.join(MAPS_DIR, f"{request.city_name}_map.html")
    m.save(map_path)

    return {
        "plan": plan,
        "map_url": f"http://127.0.0.1:8000/maps/{request.city_name}_map.html"
    }
from fastapi import APIRouter
from backend.schemas.planner import CityRequest, CityPlan
from backend.services.planner import generate_city_plan, generate_city_map

router = APIRouter()

@router.post("/plan", response_model=CityPlan)
def create_plan(req: CityRequest):
    plan = generate_city_plan(req)
    map_path = generate_city_map(plan)
    return {"plan": plan, "map_file": map_path}
