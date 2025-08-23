from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routers import city

app = FastAPI(
    title="TerraNova - Smart City Planner",
    description="AI-driven city planning system",
    version="1.0.0"
)

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (for maps)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(city.router, prefix="/city", tags=["City Planner"])

@app.get("/")
def root():
    return {"message": "Welcome to TerraNova - Smart City Planner API 🚀"}
