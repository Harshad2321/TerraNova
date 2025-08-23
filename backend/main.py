from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import routers
from backend.routers import city, planner, upload, visualize


app = FastAPI(title="TerraNova City Planner")

# ✅ CORS middleware so frontend can access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount static files for maps
app.mount("/maps", StaticFiles(directory="generated_maps"), name="maps")
app.mount("/uploads", StaticFiles(directory="uploaded_files"), name="uploads")

# ✅ Include routers
app.include_router(city.router, prefix="/city", tags=["City"])
app.include_router(planner.router, prefix="/planner", tags=["Planner"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(visualize.router, prefix="/visualize", tags=["Visualize"])


@app.get("/")
def root():
    return {"message": "🌍 Welcome to TerraNova Backend API!"}
from fastapi import FastAPI
from backend.routers import planner

app = FastAPI(title="City Planner API")

app.include_router(planner.router, prefix="/planner", tags=["Planner"])
