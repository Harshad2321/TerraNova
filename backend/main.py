from fastapi import FastAPI
from backend.routers import city

app = FastAPI(
    title="TerraNova City Planner",
    description="AI-driven smart city planning API",
    version="1.0.0"
)

# Include routers
app.include_router(city.router, prefix="/city", tags=["City Planner"])

@app.get("/")
def root():
    return {"message": "Welcome to TerraNova City Planner API 🚀"}
