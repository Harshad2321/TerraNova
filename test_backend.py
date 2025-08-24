import requests
import json

def test_backend():
    """Test the TerraNova backend API"""
    
    print("🧪 Testing TerraNova Backend API")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Health check: {response.status_code}")
        print(f"📝 Response: {response.json()}")
        print()
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test city generation endpoint
    try:
        test_data = {
            "city_name": "Test City",
            "population": 1000000,
            "terrain": "coastal",
            "eco_priority": 8,
            "size": 40
        }
        
        response = requests.post(f"{base_url}/city/generate_plan", json=test_data)
        print(f"✅ City generation: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Generated {len(data['plan_grid'])}x{len(data['plan_grid'][0])} grid")
            print(f"🌱 Green cover: {data['metrics']['green_cover_pct']}%")
            print(f"🚶 Walkability: {data['metrics']['walkability_index']}")
            print(f"💡 Notes: {len(data['notes'])} recommendations")
            print()
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ City generation failed: {e}")
        return False

if __name__ == "__main__":
    success = test_backend()
    if success:
        print("🎉 All tests passed! Backend is working correctly.")
        print("🌐 You can now use the frontend at: file:///frontend/index.html")
    else:
        print("⚠️ Some tests failed. Check if the backend is running on port 8000.")
