from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import city

app = FastAPI(title="TerraNova – Eco Future City Builder (Backend)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "TerraNova backend is live 🚀", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(city.router, prefix="/city", tags=["city"])
