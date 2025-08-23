from fastapi import APIRouter
from backend.services.visualization import generate_visual_map

router = APIRouter()

@router.get("/")
def visualize_map():
    path = generate_visual_map()
    return {"visual_map": path}
