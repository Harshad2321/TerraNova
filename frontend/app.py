from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend is working!"}

@app.post("/generate_plan")
def generate_plan(data: dict):
    city = data.get("city_name", "Unknown City")
    return {"plan": f"This is a waste reduction plan for {city}."}
