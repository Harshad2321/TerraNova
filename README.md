# 🏙️ TerraNova - AI Future City Builder

> **100% Streamlit-Free | Pure HTML/CSS/JavaScript Frontend**

TerraNova is a modern, AI-powered city planning application that generates sustainable urban layouts using pure web technologies. No Streamlit, no complex frameworks - just clean HTML, CSS, and JavaScript with a powerful FastAPI backend.

- 🔗 **[View Project](https://parth2619.github.io/TerraNova/)**  
- 💻 **[GitHub Repository](https://github.com/Parth2619/TerraNova)** 

## 🌟 Features

### 🤖 **AI-Powered City Generation**
- Intelligent urban planning algorithms
- Population-based density optimization
- Terrain-adaptive layouts
- Eco-priority focused design

### 🎨 **Modern Web Interface**
- **Pure HTML/CSS/JavaScript** - No framework dependencies
- Responsive design for all devices
- Real-time interactive map visualization
- Smooth animations and transitions
- Progressive Web App features

### 🌱 **Sustainability Focus**
- Green coverage optimization
- Walkability index calculation
- Public transit planning
- Renewable energy potential assessment
- CO2 emission tracking

### 📊 **Advanced Analytics**
- Real-time sustainability metrics
- AI-generated recommendations
- Color-coded zone visualization
- Downloadable city maps
- Shareable city designs

## 🚀 Quick Start

### Option 1: One-Click Launch
```bash
python run_app.py
```

### Option 2: Manual Setup

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Start Backend (Terminal 1)**
```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**3. Start Frontend (Terminal 2)**
```bash
python serve_frontend.py
```

**4. Open in Browser**
- **Main App**: http://localhost:3000
- **Landing Page**: Open `index.html` in browser
- **API Docs**: http://127.0.0.1:8000/docs

## 🎮 How to Use

### 1. **City Configuration**
- **🏙️ City Name**: Enter your desired city name
- **👥 Population**: Set between 50K - 30M residents
- **🌍 Terrain**: Choose from Coastal, Plains, or Mountain
- **♻️ Eco Priority**: Scale 1-10 (higher = more sustainable)
- **📐 Grid Size**: Select from 36×36 to 84×84 for detail level

### 2. **Generation Process**
- Click "🚀 Generate City Plan"
- Watch AI create your sustainable city
- View real-time progress indicators

### 3. **Explore Results**
- **Interactive Map**: Zoom and explore your city
- **Sustainability Metrics**: View environmental impact
- **AI Recommendations**: Get optimization suggestions
- **Download/Share**: Export maps or share designs

## 🗺️ Understanding the City Map

| Zone | Color | Description | Purpose |
|------|-------|-------------|---------|
| 🌊 Water | Blue | Rivers, lakes, coastline | Natural features, recreation |
| ⛰️ Mountain | Brown | Mountainous terrain | Natural barriers, scenic areas |
| 🌾 Farm | Light Green | Agricultural zones | Food production, rural areas |
| 🌳 Parks | Green | Green spaces, recreation | Environmental health, quality of life |
| 🏠 Residential | Orange | Housing areas | Living spaces for citizens |
| 🏢 Commercial | Gray | Business districts | Economic centers, jobs |
| 🏥 Healthcare | Pink | Hospitals, clinics | Medical services |
| 🏫 Education | Yellow | Schools, universities | Learning institutions |
| 🚇 Metro | Purple | Subway lines | Mass transit system |
| 🚉 Stations | Red-Orange | Transit hubs | Transport connections |
| 🚶 Walkways | Light Brown | Pedestrian paths | Walkable infrastructure |
| 🛣️ Roads | Dark Gray | Street network | Vehicle transportation |

## 📊 Sustainability Metrics Explained

### 🌱 **Green Cover Percentage**
- **Target**: 25%+ for optimal sustainability
- **Impact**: Air quality, temperature regulation, biodiversity
- **Factors**: Parks, farms, natural areas vs total city area

### 🚶 **Walkability Index** (0-100)
- **Excellent**: 80+ (Highly pedestrian-friendly)
- **Good**: 60-79 (Moderately walkable)
- **Poor**: <60 (Car-dependent)
- **Factors**: Pedestrian paths, mixed-use development, proximity to amenities

### 🚇 **Transit Coverage** (0-100%)
- **Excellent**: 70%+ (Comprehensive public transport)
- **Good**: 50-69% (Adequate coverage)
- **Poor**: <50% (Limited access)
- **Factors**: Metro lines, stations, service area coverage

### ⚡ **Renewable Potential** (0-100)
- **Factors**: Terrain type, climate conditions, available space
- **Coastal**: Wind and tidal energy opportunities
- **Mountain**: Hydroelectric and wind potential
- **Plains**: Solar and wind energy capacity

### 🌍 **CO2 Per Capita** (tons/year)
- **Excellent**: <3 tons (Carbon negative/neutral)
- **Good**: 3-5 tons (Low carbon footprint)
- **Poor**: >5 tons (High emissions)
- **Factors**: Energy mix, transport systems, urban density

## 🛠️ Technical Architecture

### **Frontend Stack**
```
📁 frontend/
├── 📄 index.html     # Main application UI
├── 🎨 style.css      # Modern responsive styling
└── ⚡ script.js      # Interactive functionality
```

**Technologies:**
- **HTML5**: Semantic markup and Canvas API
- **CSS3**: Grid, Flexbox, animations, variables
- **JavaScript ES6+**: Async/await, modules, modern APIs
- **Canvas API**: Real-time map rendering
- **Progressive Web App**: Offline capabilities

### **Backend Stack**
```
📁 backend/
├── 🐍 main.py        # FastAPI application
├── 📋 schemas.py     # Data models
├── 📁 routers/       # API endpoints
└── 📁 services/      # Business logic
```

**Technologies:**
- **FastAPI**: High-performance async API framework
- **Pydantic**: Data validation and serialization
- **NumPy**: Numerical computations for city generation
- **CORS**: Cross-origin resource sharing

### **AI City Generation Algorithm**

1. **Terrain Analysis**: Adapt layout based on geographical features
2. **Population Distribution**: Calculate optimal density zones
3. **Infrastructure Planning**: Road networks and transit systems
4. **Zoning Optimization**: Mixed-use development patterns
5. **Sustainability Integration**: Green spaces and renewable energy
6. **Metrics Calculation**: Real-time sustainability assessment

## 🔧 API Reference

### **Generate City Plan**
```http
POST /city/generate_plan
Content-Type: application/json

{
  "city_name": "string",
  "population": integer (50000-30000000),
  "terrain": "coastal" | "plains" | "mountain",
  "eco_priority": integer (1-10),
  "size": integer (36-84)
}
```

**Response:**
```json
{
  "plan_grid": "number[][]",
  "legend": "object",
  "metrics": {
    "green_cover_pct": "number",
    "walkability_index": "number",
    "transit_coverage_pct": "number",
    "renewable_potential": "number",
    "est_co2_per_capita": "number"
  },
  "notes": "string[]",
  "city_info": "object"
}
```

### **Health Check**
```http
GET /
GET /health
```

## 📱 Progressive Web App Features

- **Offline Capability**: Works without internet after first load
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Fast Loading**: Optimized assets and caching
- **App-like Experience**: Can be installed on devices
- **Modern Browser APIs**: Canvas, LocalStorage, Clipboard

## 🧪 Testing & Development

### **Run Tests**
```bash
python test_backend.py
```

### **Development Mode**
```bash
# Backend with hot reload
cd backend && uvicorn main:app --reload

# Frontend with live server
python serve_frontend.py
```

### **Production Deployment**
```bash
# Backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Frontend (serve static files)
# Deploy frontend/ folder to any static hosting service
```

## 🌍 Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 80+ | ✅ Full Support |
| Firefox | 75+ | ✅ Full Support |
| Safari | 13+ | ✅ Full Support |
| Edge | 80+ | ✅ Full Support |

**Required Features:**
- HTML5 Canvas API
- CSS Grid and Flexbox
- JavaScript ES6+ (async/await)
- Fetch API

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Clone your fork
3. Install dependencies: `pip install -r requirements.txt`
4. Make your changes
5. Test thoroughly
6. Submit a pull request

### **Code Style**
- **Python**: Follow PEP 8
- **JavaScript**: ES6+ with modern practices
- **CSS**: BEM methodology preferred
- **HTML**: Semantic markup

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support & Troubleshooting

### **Common Issues**

**❌ "Could not connect to backend"**
- Ensure backend is running: `cd backend && uvicorn main:app --reload`
- Check port 8000 is available
- Verify CORS settings

**❌ "Map not rendering"**
- Enable JavaScript in browser
- Check browser console (F12) for errors
- Ensure Canvas API is supported

**❌ "Dependencies failed to install"**
- Update pip: `python -m pip install --upgrade pip`
- Use virtual environment
- Check Python version (3.8+ required)

### **Performance Optimization**

**For Large Cities (>60×60):**
- Use smaller grid sizes for faster generation
- Close other browser tabs to free memory
- Consider using a more powerful device

**For Slow Networks:**
- Use smaller grid sizes initially
- Enable browser caching
- Use local development setup

## 🎯 Roadmap

### **Version 2.0 Planned Features**
- [ ] 3D city visualization
- [ ] Multiple city comparison
- [ ] Historical city evolution
- [ ] Climate change simulation
- [ ] Economic impact modeling
- [ ] Population growth scenarios
- [ ] Export to common GIS formats
- [ ] Collaborative city planning
- [ ] Mobile app version
- [ ] VR/AR city exploration

---

## 🏆 **TerraNova: Building Sustainable Cities with AI**

**No Streamlit. No complexity. Just pure web technology creating the future of urban planning.**

Built with ❤️ for sustainable urban development by the TerraNova team.
