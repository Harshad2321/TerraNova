from fastapi import FastAPI
from backend.routers import city
from fastapi.middleware.cors import CORSMiddleware


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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://127.0.0.1:5500"] if running from Live Server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)