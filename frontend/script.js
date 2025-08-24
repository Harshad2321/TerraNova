// Color mapping for different cell types
const colorMap = {
    0: '#f5f5f5',  // EMPTY - light gray
    1: '#4fc3f7',  // WATER - blue
    2: '#8d6e63',  // MOUNTAIN - brown
    3: '#aed581',  // FARM - light green
    4: '#66bb6a',  // PARK - green
    5: '#ffb74d',  // HOME - orange
    6: '#90a4ae',  // OFFICE - gray
    7: '#f06292',  // HOSPITAL - pink
    8: '#fff176',  // SCHOOL - yellow
    9: '#ba68c8',  // METRO - purple
    10: '#ff8a65', // STATION - red-orange
    11: '#a1887f', // WALK - light brown
    12: '#424242'  // ROAD - dark gray
};

// API Configuration - automatically detects environment
const API_CONFIG = {
    // Detect if running locally or in production
    getBaseURL() {
        const hostname = window.location.hostname;

        // Local development
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://127.0.0.1:8000';
        }

        // Vercel deployment
        if (hostname.includes('vercel.app')) {
            return `${window.location.protocol}//${hostname}/api`;
        }

        // Netlify deployment (external backend)
        if (hostname.includes('netlify.app')) {
            return 'https://your-backend-url.railway.app'; // Update this with your backend URL
        }

        // GitHub Pages (external backend)
        if (hostname.includes('github.io')) {
            return 'https://your-backend-url.railway.app'; // Update this with your backend URL
        }

        // Default to current domain with /api path
        return `${window.location.protocol}//${hostname}/api`;
    }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function () {
    initializeApp();
});

function initializeApp() {
    // Set up event listeners
    document.getElementById("generateBtn").addEventListener("click", generateCity);
    document.getElementById("ecoPriority").addEventListener("input", updateEcoValue);
    document.getElementById("downloadBtn").addEventListener("click", downloadMap);
    document.getElementById("shareBtn").addEventListener("click", shareCity);

    // Initialize eco priority display
    updateEcoValue();

    // Add sample data for demo
    loadSampleData();
}

function updateEcoValue() {
    const ecoSlider = document.getElementById("ecoPriority");
    const ecoDisplay = document.getElementById("ecoValue");
    ecoDisplay.textContent = ecoSlider.value;
}

function loadSampleData() {
    // Add some sample cities for quick testing
    const sampleCities = [
        "Neo Greenfield", "EcoTopia", "Sustainable Springs", "Green Haven",
        "Future City", "Carbon Zero", "Solar Vista", "Wind Harbor"
    ];

    const cityNameInput = document.getElementById("cityName");
    cityNameInput.setAttribute("list", "cityList");

    // Create datalist for city suggestions
    const datalist = document.createElement("datalist");
    datalist.id = "cityList";
    sampleCities.forEach(city => {
        const option = document.createElement("option");
        option.value = city;
        datalist.appendChild(option);
    });

    document.body.appendChild(datalist);
}

async function generateCity() {
    const cityName = document.getElementById("cityName").value.trim();
    const population = parseInt(document.getElementById("population").value);
    const terrain = document.getElementById("terrain").value;
    const ecoPriority = parseInt(document.getElementById("ecoPriority").value);
    const size = parseInt(document.getElementById("size").value);

    // Validation
    if (!cityName) {
        showError("Please enter a city name");
        return;
    }

    if (population < 50000 || population > 30000000) {
        showError("Population must be between 50,000 and 30,000,000");
        return;
    }

    const generateBtn = document.getElementById("generateBtn");
    const btnText = document.getElementById("btnText");
    const spinner = document.getElementById("loadingSpinner");
    const metricsList = document.getElementById("metricsList");
    const notesList = document.getElementById("notesList");
    const cityInfoDiv = document.getElementById("cityInfo");
    const mapControls = document.getElementById("mapControls");

    // Show loading state
    generateBtn.disabled = true;
    btnText.style.display = "none";
    spinner.style.display = "block";
    metricsList.innerHTML = "<li class='placeholder-metric'>🔄 Generating city plan...</li>";
    notesList.innerHTML = "<li class='placeholder-note'>AI is analyzing your requirements...</li>";
    cityInfoDiv.style.display = "none";
    mapControls.style.display = "none";

    try {
        const baseURL = API_CONFIG.getBaseURL();
        const response = await fetch(`${baseURL}/city/generate_plan`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                city_name: cityName,
                population: population,
                terrain: terrain,
                eco_priority: ecoPriority,
                size: size
            })
        });

        if (!response.ok) {
            throw new Error(`Backend error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();

        // Display results with animations
        setTimeout(() => displayCityInfo(data.city_info), 300);
        setTimeout(() => renderMap(data.plan_grid, data.legend), 600);
        setTimeout(() => displayMetrics(data.metrics), 900);
        setTimeout(() => displayNotes(data.notes), 1200);

        // Show map controls
        mapControls.style.display = "flex";

        // Store data for sharing/downloading
        window.currentCityData = data;

        showSuccess("City generated successfully!");

    } catch (error) {
        console.error("Error:", error);
        
        // Check if we're on GitHub Pages and provide demo mode
        const hostname = window.location.hostname;
        if (hostname.includes('github.io')) {
            console.log("Running in demo mode on GitHub Pages");
            showDemoMode(cityName, population, terrain, ecoPriority, size);
        } else {
            showError(`Could not connect to backend: ${error.message}`);
            metricsList.innerHTML = "<li style='color:red;'>⚠️ Failed to generate city. Please check if the backend is running on port 8000.</li>";
        }
    } finally {
        // Reset button state
        generateBtn.disabled = false;
        btnText.style.display = "block";
        spinner.style.display = "none";
    }
}

function renderMap(grid, legend) {
    const canvas = document.getElementById("mapCanvas");
    const ctx = canvas.getContext("2d");

    const gridSize = grid.length;
    const maxCanvasSize = Math.min(window.innerWidth * 0.4, 600);
    const cellSize = Math.floor(maxCanvasSize / gridSize);

    canvas.width = gridSize * cellSize;
    canvas.height = gridSize * cellSize;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw grid with smooth rendering
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            const cellType = grid[i][j];
            const color = colorMap[cellType] || '#ffffff';

            ctx.fillStyle = color;
            ctx.fillRect(j * cellSize, i * cellSize, cellSize, cellSize);

            // Add subtle borders for larger cells
            if (cellSize > 8) {
                ctx.strokeStyle = 'rgba(0,0,0,0.1)';
                ctx.lineWidth = 0.5;
                ctx.strokeRect(j * cellSize, i * cellSize, cellSize, cellSize);
            }
        }
    }

    // Add legend
    addLegend(legend);
}

function addLegend(legend) {
    // Remove existing legend
    const existingLegend = document.getElementById('mapLegend');
    if (existingLegend) {
        existingLegend.remove();
    }

    const legendContainer = document.createElement('div');
    legendContainer.id = 'mapLegend';

    // Create legend items
    Object.entries(legend).forEach(([code, name]) => {
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item';

        const colorBox = document.createElement('div');
        colorBox.className = 'legend-color';
        colorBox.style.backgroundColor = colorMap[code] || '#ffffff';

        const label = document.createElement('span');
        label.textContent = name;

        legendItem.appendChild(colorBox);
        legendItem.appendChild(label);
        legendContainer.appendChild(legendItem);
    });

    document.getElementById('mapArea').appendChild(legendContainer);
}

function displayCityInfo(cityInfo) {
    const cityInfoDiv = document.getElementById("cityInfo");
    const cityNameDisplay = document.getElementById("cityNameDisplay");
    const cityPopulationSpan = document.getElementById("cityPopulation");
    const cityTerrainSpan = document.getElementById("cityTerrain");
    const citySizeSpan = document.getElementById("citySize");

    cityNameDisplay.textContent = cityInfo.name;
    cityPopulationSpan.textContent = `${cityInfo.population.toLocaleString()} residents`;
    cityTerrainSpan.textContent = `${cityInfo.terrain.charAt(0).toUpperCase() + cityInfo.terrain.slice(1)} terrain`;
    citySizeSpan.textContent = `${cityInfo.size} grid`;

    cityInfoDiv.style.display = "grid";
    cityInfoDiv.style.animation = "fadeInUp 0.5s ease";
}

function displayMetrics(metrics) {
    const metricsList = document.getElementById("metricsList");
    metricsList.innerHTML = "";

    Object.entries(metrics).forEach(([key, value], index) => {
        const li = document.createElement("li");
        const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

        // Add appropriate emoji for each metric
        const emoji = getMetricEmoji(key);

        let displayValue;
        if (typeof value === 'number') {
            if (key.includes('pct') || key.includes('index')) {
                displayValue = `${value}%`;
            } else {
                displayValue = value;
            }
        } else {
            displayValue = value;
        }

        li.innerHTML = `${emoji} <strong>${formattedKey}:</strong> ${displayValue}`;

        // Add color coding based on values
        li.style.borderLeftColor = getMetricColor(key, value);

        // Animate appearance
        li.style.opacity = "0";
        li.style.transform = "translateX(-20px)";
        setTimeout(() => {
            li.style.transition = "all 0.3s ease";
            li.style.opacity = "1";
            li.style.transform = "translateX(0)";
        }, index * 100);

        metricsList.appendChild(li);
    });
}

function displayNotes(notes) {
    const notesList = document.getElementById("notesList");
    notesList.innerHTML = "";

    notes.forEach((note, index) => {
        const li = document.createElement("li");
        li.textContent = note;

        // Animate appearance
        li.style.opacity = "0";
        li.style.transform = "translateX(-20px)";
        setTimeout(() => {
            li.style.transition = "all 0.3s ease";
            li.style.opacity = "1";
            li.style.transform = "translateX(0)";
        }, index * 150);

        notesList.appendChild(li);
    });
}

function getMetricEmoji(key) {
    const emojiMap = {
        'green_cover_pct': '🌱',
        'walkability_index': '🚶',
        'transit_coverage_pct': '🚇',
        'renewable_potential': '⚡',
        'est_co2_per_capita': '🌍'
    };
    return emojiMap[key] || '📊';
}

function getMetricColor(key, value) {
    if (key === 'est_co2_per_capita') {
        // Lower is better for CO2
        return value < 3 ? '#16a34a' : value < 5 ? '#f59e0b' : '#dc2626';
    } else {
        // Higher is better for other metrics
        return value > 70 ? '#16a34a' : value > 40 ? '#f59e0b' : '#dc2626';
    }
}

function downloadMap() {
    const canvas = document.getElementById("mapCanvas");
    const cityName = document.getElementById("cityName").value || "TerraNova_City";

    const link = document.createElement('a');
    link.download = `${cityName}_map.png`;
    link.href = canvas.toDataURL();
    link.click();

    showSuccess("Map downloaded successfully!");
}

function shareCity() {
    if (!window.currentCityData) return;

    const cityData = {
        name: document.getElementById("cityName").value,
        population: document.getElementById("population").value,
        terrain: document.getElementById("terrain").value,
        ecoPriority: document.getElementById("ecoPriority").value,
        size: document.getElementById("size").value
    };

    const shareUrl = `${window.location.origin}${window.location.pathname}?city=${encodeURIComponent(JSON.stringify(cityData))}`;

    if (navigator.share) {
        navigator.share({
            title: `TerraNova: ${cityData.name}`,
            text: `Check out my AI-generated sustainable city: ${cityData.name}`,
            url: shareUrl
        });
    } else {
        navigator.clipboard.writeText(shareUrl).then(() => {
            showSuccess("Share link copied to clipboard!");
        });
    }
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        animation: slideInRight 0.3s ease;
        background: ${type === 'success' ? '#16a34a' : '#dc2626'};
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Modal functions
function showAbout() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>🏙️ About TerraNova</h2>
        <p>TerraNova is an AI-powered city planning tool that helps you design sustainable urban environments.</p>
        <h3>Features:</h3>
        <ul>
            <li>🤖 AI-driven city generation</li>
            <li>🌱 Sustainability metrics</li>
            <li>🌍 Multiple terrain types</li>
            <li>📊 Real-time visualization</li>
            <li>♻️ Eco-friendly planning</li>
        </ul>
        <h3>How it works:</h3>
        <p>Our AI analyzes your input parameters and generates a city layout optimized for sustainability, livability, and efficiency. The algorithm considers factors like population density, terrain characteristics, and environmental priorities to create realistic urban plans.</p>
    `;
    document.getElementById('modal').style.display = 'block';
}

function showHelp() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>🆘 Help & Guide</h2>
        <h3>Getting Started:</h3>
        <ol>
            <li>Enter your city name and population</li>
            <li>Select terrain type (affects renewable energy potential)</li>
            <li>Set eco priority (1-10, higher = more sustainable)</li>
            <li>Choose grid size (larger = more detailed)</li>
            <li>Click "Generate City Plan"</li>
        </ol>
        <h3>Understanding the Map:</h3>
        <p>Different colors represent different zones:</p>
        <ul>
            <li>🔵 Blue: Water bodies</li>
            <li>🟤 Brown: Mountains</li>
            <li>🟢 Green: Parks and green spaces</li>
            <li>🟠 Orange: Residential areas</li>
            <li>⚫ Dark gray: Roads</li>
            <li>🟣 Purple: Metro lines</li>
        </ul>
        <h3>Troubleshooting:</h3>
        <p>If you see connection errors, make sure the backend server is running on port 8000.</p>
    `;
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// Load city from URL parameters
window.addEventListener('load', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const cityParam = urlParams.get('city');

    if (cityParam) {
        try {
            const cityData = JSON.parse(decodeURIComponent(cityParam));
            document.getElementById("cityName").value = cityData.name;
            document.getElementById("population").value = cityData.population;
            document.getElementById("terrain").value = cityData.terrain;
            document.getElementById("ecoPriority").value = cityData.ecoPriority;
            document.getElementById("size").value = cityData.size;
            updateEcoValue();

            showSuccess("City loaded from share link!");
        } catch (e) {
            console.error("Error loading shared city:", e);
        }
    }
});

// Demo mode for GitHub Pages deployment
function showDemoMode(cityName, population, terrain, ecoPriority, size) {
    // Generate demo data based on inputs
    const demoData = generateDemoData(cityName, population, terrain, ecoPriority, size);
    
    // Display demo results with animations
    setTimeout(() => displayCityInfo(demoData.city_info), 300);
    setTimeout(() => renderMap(demoData.plan_grid, demoData.legend), 600);
    setTimeout(() => displayMetrics(demoData.metrics), 900);
    setTimeout(() => displayNotes(demoData.notes), 1200);

    // Show map controls
    document.getElementById("mapControls").style.display = "flex";

    // Store data for sharing/downloading
    window.currentCityData = demoData;

    showSuccess("Demo city generated! (Backend not connected - this is simulated data)");
}

function generateDemoData(cityName, population, terrain, ecoPriority, size) {
    // Generate a demo grid based on size
    const gridSize = Math.min(size, 30);
    const grid = [];
    
    for (let i = 0; i < gridSize; i++) {
        const row = [];
        for (let j = 0; j < gridSize; j++) {
            // Simple pattern generation for demo
            let cellType = 0; // Empty by default
            
            // Add some water
            if (i === 0 || j === 0 || i === gridSize-1 || j === gridSize-1) {
                if (Math.random() < 0.3) cellType = 1; // Water
            }
            
            // Add residential areas
            if (i > 2 && i < gridSize-3 && j > 2 && j < gridSize-3) {
                if (Math.random() < 0.4) cellType = 5; // Home
            }
            
            // Add roads
            if (i % 4 === 0 || j % 4 === 0) {
                if (Math.random() < 0.6) cellType = 12; // Road
            }
            
            // Add parks based on eco priority
            if (ecoPriority > 7 && Math.random() < 0.15) {
                cellType = 4; // Park
            }
            
            // Add commercial buildings
            if (Math.random() < 0.1) cellType = 6; // Office
            
            // Add essential services
            if (Math.random() < 0.05) cellType = 7; // Hospital
            if (Math.random() < 0.05) cellType = 8; // School
            
            row.push(cellType);
        }
        grid.push(row);
    }
    
    // Generate demo metrics
    const sustainabilityScore = Math.max(20, ecoPriority * 8 + Math.random() * 20);
    const efficiency = Math.max(60, 70 + Math.random() * 25);
    
    return {
        city_info: {
            name: cityName,
            population: population.toLocaleString(),
            terrain: terrain.charAt(0).toUpperCase() + terrain.slice(1),
            size: `${size}x${size} blocks`
        },
        plan_grid: grid,
        legend: {
            0: "Empty", 1: "Water", 4: "Park", 5: "Residential", 
            6: "Commercial", 7: "Hospital", 8: "School", 12: "Road"
        },
        metrics: [
            `🌱 Sustainability Score: ${sustainabilityScore.toFixed(1)}/100`,
            `⚡ Energy Efficiency: ${efficiency.toFixed(1)}%`,
            `🚶 Walkability Index: ${(60 + Math.random() * 30).toFixed(1)}/100`,
            `🏠 Housing Coverage: ${(population/1000 * 0.8).toFixed(0)} units`,
            `🌳 Green Space: ${(ecoPriority * 2 + 10).toFixed(0)}%`
        ],
        notes: [
            "📍 This is demo data generated for GitHub Pages deployment",
            "🔗 Connect a backend API for real AI-powered city generation",
            "🎨 The visualization system is fully functional",
            "📱 This app works offline and can be installed as a PWA",
            "⚙️ All frontend features are operational in demo mode"
        ]
    };
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); }
        to { transform: translateX(100%); }
    }
`;
document.head.appendChild(style);
