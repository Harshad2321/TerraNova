// TerraNova - Smart City Planner Frontend

// API base URL - change this for production
const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Switch between tabs in the UI
 * @param {string} tabId - The ID of the tab to show
 */
function switchTab(tabId) {
    // Hide all tabs and deactivate all buttons
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show the selected tab and activate its button
    document.getElementById(tabId).classList.add('active');
    document.querySelector(`button[onclick="switchTab('${tabId}')"]`).classList.add('active');
}

/**
 * Plan a city using the grid-based view
 * This uses the simple city planning API
 */
async function planCity() {
    try {
        const name = document.getElementById("name").value;
        const width = parseInt(document.getElementById("width").value);
        const height = parseInt(document.getElementById("height").value);
        const population = parseInt(document.getElementById("population").value);

        // Show loading state
        document.getElementById("grid").innerHTML = "<p>Generating your city plan...</p>";
        document.getElementById("recommendations").innerHTML = "";

        // Make API request
        const response = await fetch(`${API_BASE_URL}/city/plan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, width, height, population }),
        });

        if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
        }

        const data = await response.json();

        // Check if we have a visual map available
        const gridDiv = document.getElementById("grid");
        gridDiv.innerHTML = "";

        if (data.visual_map_available && data.map_url) {
            // Display the visual map
            const mapContainer = document.createElement("div");
            mapContainer.className = "visual-map";

            // Create map image
            const mapImage = document.createElement("img");
            mapImage.src = data.map_url;
            mapImage.alt = `${data.name} City Map`;
            mapImage.className = "city-map-image";
            mapContainer.appendChild(mapImage);

            // Add a view toggle button
            const toggleButton = document.createElement("button");
            toggleButton.innerText = "View Grid Layout";
            toggleButton.className = "toggle-view-btn";
            toggleButton.onclick = function () {
                const gridView = document.getElementById("grid-view");
                const mapView = document.getElementById("map-view");

                if (gridView.style.display === "none") {
                    gridView.style.display = "block";
                    mapView.style.display = "none";
                    toggleButton.innerText = "View Visual Map";
                } else {
                    gridView.style.display = "none";
                    mapView.style.display = "block";
                    toggleButton.innerText = "View Grid Layout";
                }
            };

            // Create container for visual map
            const mapView = document.createElement("div");
            mapView.id = "map-view";
            mapView.appendChild(mapImage);

            // Create container for grid view (initially hidden)
            const gridView = document.createElement("div");
            gridView.id = "grid-view";
            gridView.style.display = "none";
            gridView.style.gridTemplateColumns = `repeat(${width}, 1fr)`;

            // Create grid cells with color-coding for the grid view
            data.layout.forEach(row => {
                const rowDiv = document.createElement("div");
                rowDiv.className = "grid-row";

                row.forEach(cell => {
                    const cellDiv = document.createElement("div");
                    cellDiv.className = `grid-cell cell-${cell}`;
                    cellDiv.innerText = cell;
                    rowDiv.appendChild(cellDiv);
                });

                gridView.appendChild(rowDiv);
            });

            gridDiv.appendChild(mapView);
            gridDiv.appendChild(gridView);
            gridDiv.appendChild(toggleButton);
        } else {
            // Fallback to grid layout if visual map isn't available
            gridDiv.style.gridTemplateColumns = `repeat(${width}, 1fr)`;

            // Create grid cells with color-coding
            data.layout.forEach(row => {
                const rowDiv = document.createElement("div");
                rowDiv.className = "grid-row";

                row.forEach(cell => {
                    const cellDiv = document.createElement("div");
                    cellDiv.className = `grid-cell cell-${cell}`;
                    cellDiv.innerText = cell;
                    rowDiv.appendChild(cellDiv);
                });

                gridDiv.appendChild(rowDiv);
            });
        }        // Display recommendations
        const recDiv = document.getElementById("recommendations");
        recDiv.innerHTML = "<h3>Planning Recommendations:</h3>";
        const ul = document.createElement("ul");

        data.recommendations.forEach(rec => {
            const li = document.createElement("li");
            li.innerText = rec;
            ul.appendChild(li);
        });

        recDiv.appendChild(ul);

    } catch (error) {
        console.error("Error planning city:", error);
        document.getElementById("grid").innerHTML =
            `<p>Error: ${error.message || "Failed to generate city plan"}</p>`;
    }
}

/**
 * Plan a detailed city using the advanced planning system
 * This uses the detailed planning API with more parameters
 */
async function planDetailedCity() {
    try {
        const city_name = document.getElementById("city_name").value;
        const population = parseInt(document.getElementById("detailed_population").value);
        const area = parseFloat(document.getElementById("area").value);
        const soil_type = document.getElementById("soil_type").value;
        const surroundings = document.getElementById("surroundings").value;

        // Show loading state
        const resultsDiv = document.getElementById("detailed-results");
        resultsDiv.style.display = "block";
        resultsDiv.innerHTML = "<p>Analyzing city requirements...</p>";

        // Make API request to the planner endpoint
        const response = await fetch(`${API_BASE_URL}/planner/plan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                city_name,
                population,
                area,
                soil_type,
                surroundings
            }),
        });

        if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
        }

        const data = await response.json();

        // Build the results UI
        resultsDiv.innerHTML = `
            <h2>🏙️ ${data.city_name} Analysis</h2>
            <div class="result-card">
                <div id="feasibility" class="${data.feasible ? 'feasible' : 'not-feasible'}">
                    ${data.feasible ? '✅ City plan is feasible' : '⚠️ City plan may not be feasible'}
                </div>
                
                <div id="summary">
                    <h3>Summary</h3>
                    <p>${data.summary}</p>
                </div>
                
                <div id="detailed-recommendations">
                    <h3>Infrastructure Recommendations</h3>
                    <ul>
                        ${Object.entries(data.recommendations).map(([key, value]) =>
            `<li><strong>${key.replace('_', ' ')}</strong>: ${value}</li>`
        ).join('')}
                    </ul>
                </div>
                
                <div id="map-container">
                    <h3>City Map</h3>
                    <img src="${data.map_url}" alt="${data.city_name} Map" onerror="this.src='maps/NeoCity_map.png'">
                </div>
            </div>
        `;

    } catch (error) {
        console.error("Error planning detailed city:", error);
        document.getElementById("detailed-results").innerHTML =
            `<p>Error: ${error.message || "Failed to generate detailed city plan"}</p>`;
    }
}
