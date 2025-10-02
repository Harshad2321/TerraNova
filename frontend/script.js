const colorMap = {
    0: '#f5f5f5',
    1: '#4fc3f7',
    2: '#8d6e63',
    3: '#aed581',
    4: '#66bb6a',
    5: '#ffb74d',
    6: '#90a4ae',
    7: '#f06292        metricsList.innerHTML = "<li style='color:red;'>Failed to generate city. Please check if the backend is running on port 8000.</li>";,
    8: '#fff176',
    9: '#9c27b0',
    10: '#ff8a65',
    11: '#a1887f',
    12: '#424242'
};


const API_CONFIG = {

    getBaseURL() {
        const hostname = window.location.hostname;


        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://127.0.0.1:8000';
        }


        if (hostname.includes('vercel.app')) {
            return `${window.location.protocol}//${hostname}/api`;
        }


        if (hostname.includes('netlify.app')) {
            return 'https://your-backend-url.railway.app';
        }


        if (hostname.includes('github.io')) {
            return 'https://your-backend-url.railway.app';
        }


        return `${window.location.protocol}//${hostname}/api`;
    }
};


document.addEventListener('DOMContentLoaded', function () {
    initializeApp();
});

function initializeApp() {

    document.getElementById("generateBtn").addEventListener("click", generateCity);
    document.getElementById("ecoPriority").addEventListener("input", updateEcoValue);
    document.getElementById("downloadBtn").addEventListener("click", downloadMap);
    document.getElementById("shareBtn").addEventListener("click", shareCity);


    updateEcoValue();


    loadSampleData();
}

function updateEcoValue() {
    const ecoSlider = document.getElementById("ecoPriority");
    const ecoDisplay = document.getElementById("ecoValue");
    ecoDisplay.textContent = ecoSlider.value;
}

function loadSampleData() {

    const sampleCities = [
        "Neo Greenfield", "EcoTopia", "Sustainable Springs", "Green Haven",
        "Future City", "Carbon Zero", "Solar Vista", "Wind Harbor"
    ];

    const cityNameInput = document.getElementById("cityName");
    cityNameInput.setAttribute("list", "cityList");


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


    generateBtn.disabled = true;
    btnText.style.display = "none";
    spinner.style.display = "block";
    metricsList.innerHTML = "<li class='placeholder-metric'>Generating city plan...</li>";
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


        setTimeout(() => displayCityInfo(data.city_info), 300);
        setTimeout(() => renderMap(data.plan_grid, data.legend), 600);
        setTimeout(() => displayMetrics(data.metrics), 900);
        setTimeout(() => displayNotes(data.notes), 1200);


        mapControls.style.display = "flex";


        window.currentCityData = data;

        showSuccess("City generated successfully!");

    } catch (error) {
        console.error("Error:", error);
        showError(`Could not connect to backend: ${error.message}`);
        metricsList.innerHTML = "<li style='color:red;'>Failed to generate city. Please check if the backend is running on port 8000.</li>";
    } finally {

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


    ctx.clearRect(0, 0, canvas.width, canvas.height);


    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            const cellType = grid[i][j];
            const color = colorMap[cellType] || '#ffffff';

            ctx.fillStyle = color;
            ctx.fillRect(j * cellSize, i * cellSize, cellSize, cellSize);


            if (cellSize > 8) {
                ctx.strokeStyle = 'rgba(0,0,0,0.1)';
                ctx.lineWidth = 0.5;
                ctx.strokeRect(j * cellSize, i * cellSize, cellSize, cellSize);
            }
        }
    }


    addLegend(legend);
}

function addLegend(legend) {

    const existingLegend = document.getElementById('mapLegend');
    if (existingLegend) {
        existingLegend.remove();
    }

    const legendContainer = document.createElement('div');
    legendContainer.id = 'mapLegend';


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

        li.innerHTML = `<strong>${formattedKey}:</strong> ${displayValue}`;


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
        'green_cover_pct': '',
        'walkability_index': '',
        'transit_coverage_pct': '',
        'renewable_potential': '',
        'est_co2_per_capita': ''
    };
    return emojiMap[key] || '';
}

function getMetricColor(key, value) {
    if (key === 'est_co2_per_capita') {

        return value < 3 ? '#16a34a' : value < 5 ? '#f59e0b' : '#dc2626';
    } else {

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


function showAbout() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>About TerraNova</h2>
        <p>TerraNova is an AI-powered city planning tool that helps you design sustainable urban environments.</p>
        <h3>Features:</h3>
        <ul>
            <li>AI-driven city generation</li>
            <li>Sustainability metrics</li>
            <li>Multiple terrain types</li>
            <li>Real-time visualization</li>
            <li>Eco-friendly planning</li>
        </ul>
        <h3>How it works:</h3>
        <p>Our AI analyzes your input parameters and generates a city layout optimized for sustainability, livability, and efficiency. The algorithm considers factors like population density, terrain characteristics, and environmental priorities to create realistic urban plans.</p>
    `;
    document.getElementById('modal').style.display = 'block';
}

function showHelp() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Help & Guide</h2>
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
            <li>Blue: Water bodies</li>
            <li>Brown: Mountains</li>
            <li>Green: Parks and green spaces</li>
            <li>Orange: Residential areas</li>
            <li>Dark gray: Roads</li>
            <li>Purple: Metro lines</li>
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
