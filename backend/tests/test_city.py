from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_city_plan():
    response = client.post("/city/plan", json={"name": "NeoCity", "width": 5, "height": 5})
    assert response.status_code == 200
    data = response.json()
    assert "plan" in data
    assert len(data["plan"]) == 5
    assert len(data["plan"][0]) == 5
