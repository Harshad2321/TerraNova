from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_city_grid_plan():
    """Test the grid-based city planning endpoint"""
    response = client.post("/city/plan", json={
        "name": "NeoCity", 
        "width": 5, 
        "height": 5,
        "population": 10000
    })
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert "plan" in data
    assert "layout" in data
    assert "recommendations" in data
    
    # Check dimensions
    assert len(data["plan"]) == 5
    assert len(data["plan"][0]) == 5
    assert len(data["layout"]) == 5
    assert len(data["layout"][0]) == 5
    
    # Check recommendations
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) > 0

def test_detailed_city_plan():
    """Test the detailed city planning endpoint"""
    response = client.post("/planner/plan", json={
        "city_name": "NeoCity",
        "population": 50000,
        "area": 25.5,
        "soil_type": "loamy",
        "surroundings": "plain"
    })
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    assert "city_name" in data
    assert "feasible" in data
    assert "recommendations" in data
    assert "summary" in data
    assert "map_url" in data
    
    # Verify data types
    assert isinstance(data["feasible"], bool)
    assert isinstance(data["recommendations"], dict)
    assert isinstance(data["summary"], str)
    
def test_invalid_input_handling():
    """Test error handling for invalid input"""
    # Test invalid soil type
    response = client.post("/planner/plan", json={
        "city_name": "NeoCity",
        "population": 50000,
        "area": 25.5,
        "soil_type": "invalid",
        "surroundings": "plain"
    })
    assert response.status_code == 400
    
    # Test negative population
    response = client.post("/planner/plan", json={
        "city_name": "NeoCity",
        "population": -1000,
        "area": 25.5,
        "soil_type": "loamy",
        "surroundings": "plain"
    })
    assert response.status_code == 400
