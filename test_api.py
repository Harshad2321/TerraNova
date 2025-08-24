"""
Test script to verify API functionality
"""
import httpx
import json

BASE_URL = "http://127.0.0.1:8000"

# Test invalid input - negative population
def test_invalid_input():
    print("Testing invalid input handling...")
    response = httpx.post(
        f"{BASE_URL}/planner/plan",
        json={
            "city_name": "TestCity",
            "population": -100,
            "area": 20,
            "soil_type": "loamy",
            "surroundings": "plain"
        }
    )
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test valid input for grid-based city
def test_grid_city():
    print("\nTesting grid-based city planning...")
    response = httpx.post(
        f"{BASE_URL}/city/plan",
        json={
            "name": "GridCity",
            "width": 5,
            "height": 5,
            "population": 50000
        }
    )
    print(f"Status code: {response.status_code}")
    result = response.json()
    print(f"City name: {result['name']}")
    print(f"Grid dimensions: {result['width']}x{result['height']}")
    print(f"Population: {result['population']}")
    print(f"Recommendations: {len(result['recommendations'])}")

# Test valid input for detailed city planning
def test_detailed_city():
    print("\nTesting detailed city planning...")
    response = httpx.post(
        f"{BASE_URL}/planner/plan",
        json={
            "city_name": "DetailedCity",
            "population": 50000,
            "area": 25.5,
            "soil_type": "loamy",
            "surroundings": "plain"
        }
    )
    print(f"Status code: {response.status_code}")
    result = response.json()
    print(f"City name: {result['city_name']}")
    print(f"Feasible: {result['feasible']}")
    print(f"Summary: {result['summary']}")
    print(f"Recommendations count: {len(result['recommendations'])}")

if __name__ == "__main__":
    print("Running TerraNova API tests")
    print("==========================")
    
    try:
        test_invalid_input()
        test_grid_city()
        test_detailed_city()
        print("\nAll tests completed!")
    except Exception as e:
        print(f"Error during tests: {e}")
