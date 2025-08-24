from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import os
import logging
from backend.routers import city, planner
from backend.utils.config import APP_NAME, VERSION
from backend.utils.error_handlers import (
    validation_exception_handler,
    pydantic_validation_handler,
    general_exception_handler
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("terranova")

# Initialize FastAPI app
app = FastAPI(
    title=APP_NAME,
    description="AI-driven city planning system",
    version=VERSION
)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, pydantic_validation_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Allow frontend access with CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (for maps)
# Make sure the static directory exists
os.makedirs("backend/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Make sure maps directory exists
os.makedirs("maps", exist_ok=True)
app.mount("/maps", StaticFiles(directory="maps"), name="maps")

# Frontend static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Routers
app.include_router(city.router, prefix="/city", tags=["City"])
app.include_router(planner.router, prefix="/planner", tags=["Planner"])

@app.get("/")
def root():
    return {"message": f"Welcome to {APP_NAME} API 🚀 - v{VERSION}"}

@app.get("/app")
def serve_frontend():
    """Serve the frontend index.html file"""
    return FileResponse("frontend/index.html")
