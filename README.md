# TerraNova - Smart City Planner

TerraNova is an AI-driven city planning tool that helps urban designers and architects visualize and plan cities based on various parameters such as population, area, soil type, and surroundings.

## Features

- **Grid-Based City Planning**: Create visual representations of city layouts with roads, buildings, parks, etc.
- **Detailed City Analysis**: Get recommendations for city infrastructure based on population and area
- **Feasibility Assessment**: Check if your city plan is feasible based on parameters
- **Interactive UI**: User-friendly interface for creating and visualizing city plans

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI (Python)
- **Testing**: Pytest

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js (optional, for frontend development)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Harshad2321/TerraNova.git
   cd TerraNova
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn backend.main:app --reload
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/frontend
   ```

## API Documentation

Once the server is running, you can access the API documentation at:
```
http://127.0.0.1:8000/docs
```

### Key Endpoints

- `GET /` - API Root
- `GET /frontend` - Frontend interface
- `POST /city/plan` - Grid-based city planning
- `POST /planner/plan` - Detailed city planning and analysis

## Testing

Run tests using pytest:
```
pytest backend/tests/
```

## Project Structure

```
TerraNova/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   ├── city.py
│   │   └── planner.py
│   ├── schemas/
│   │   └── city.py
│   ├── services/
│   │   ├── planner.py
│   │   └── tiles.py
│   ├── static/
│   │   └── dd_map.png
│   ├── tests/
│   │   └── test_city.py
│   └── utils/
│       ├── __init__.py
│       └── config.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── maps/
│   └── NeoCity_map.png
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Icons and emojis used in the city visualization
- FastAPI for the excellent backend framework