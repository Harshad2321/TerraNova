# 🏙️ TerraNova Setup Instructions

## ✅ What's Been Fixed

Your TerraNova application is now fully connected! Here's what was resolved:

### 🔧 Frontend-Backend Connection Issues Fixed:
1. **API Endpoint Mismatch**: Updated frontend to call correct `/city/generate_plan` endpoint
2. **HTML Element Mismatch**: Fixed JavaScript to use correct element IDs
3. **CORS Issues**: Added proper CORS middleware to backend
4. **Data Mapping**: Frontend now sends all required parameters
5. **Visualization**: Added complete map rendering with color-coded legend

### 🎨 Enhanced Features Added:
- **Interactive Map**: Real-time canvas rendering with proper legends
- **Loading States**: Better user feedback during generation
- **City Information**: Display of city parameters and metrics
- **Responsive Design**: Mobile-friendly layout
- **Error Handling**: Proper error messages and status indicators

## 🚀 Quick Start (Choose One Method)

### Method 1: Automatic Runner (Recommended)
```bash
python run_app.py
```

### Method 2: Manual Setup

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
python serve_frontend.py
```

**Or open directly:**
Open `frontend/index.html` in your browser

## 🧪 Testing

Run the test script to verify everything works:
```bash
python test_backend.py
```

## 🌐 URLs

- **Frontend**: http://localhost:3000 (or file:///path/to/frontend/index.html)
- **Backend API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

## 🎮 How to Use

1. **Enter City Details**:
   - City Name: Any name you want
   - Population: 50,000 to 30,000,000
   - Terrain: Coastal, Plains, or Mountain
   - Eco Priority: 1-10 scale (higher = more sustainable)
   - Grid Size: 36x36 to 96x96 (larger = more detailed)

2. **Click "Generate Plan"**: Wait for the AI to create your city

3. **View Results**:
   - **Map**: Interactive color-coded city layout
   - **Metrics**: Sustainability indicators
   - **Notes**: AI recommendations for improvement

## 🗺️ Understanding the Map

| Color | Zone | Description |
|-------|------|-------------|
| 🔵 Blue | Water | Rivers, lakes, coastline |
| 🟤 Brown | Mountain | Mountainous regions |
| 🟢 Green | Parks | Green spaces and recreation |
| 🟠 Orange | Residential | Housing areas |
| ⚫ Dark Gray | Roads | Street network |
| 🟣 Purple | Metro | Public transit |
| 🟡 Yellow | Schools | Educational facilities |
| 🩷 Pink | Hospitals | Healthcare centers |

## 📊 Key Metrics

- **Green Cover %**: Ideal is 25%+ for sustainability
- **Walkability Index**: Higher = more pedestrian-friendly
- **Transit Coverage %**: Public transport accessibility
- **Renewable Potential**: Capacity for clean energy
- **CO2 Per Capita**: Lower is better for environment

## 🆘 Troubleshooting

**"Could not connect to backend":**
- Make sure backend is running on port 8000
- Check if `uvicorn main:app --reload` is running in the backend folder

**Map not showing:**
- Enable JavaScript in your browser
- Check browser console for errors (F12)

**Dependencies missing:**
```bash
pip install fastapi uvicorn numpy pydantic
```

## ✨ Features

- **Real-time Generation**: AI creates cities in seconds
- **Terrain Adaptation**: Different layouts for coastal, mountain, plains
- **Population Scaling**: Realistic density based on population
- **Eco-Friendly Planning**: Sustainability metrics and recommendations
- **Interactive Visualization**: Click and explore your generated city

Your TerraNova application is now ready to use! 🎉
