// frontend/script.js
async function planCity() {
    const width = document.getElementById("width").value;
    const height = document.getElementById("height").value;
    const population = document.getElementById("population").value;

    const response = await fetch("http://127.0.0.1:8000/city/plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ width, height, population }),
    });

    const data = await response.json();

    // Display grid
    const gridDiv = document.getElementById("grid");
    gridDiv.innerHTML = "";
    data.layout.forEach(row => {
        const rowDiv = document.createElement("div");
        rowDiv.style.display = "flex";
        row.forEach(cell => {
            const cellDiv = document.createElement("div");
            cellDiv.innerText = cell[0].toUpperCase(); // First letter
            cellDiv.style.width = "30px";
            cellDiv.style.height = "30px";
            cellDiv.style.border = "1px solid black";
            cellDiv.style.textAlign = "center";
            rowDiv.appendChild(cellDiv);
        });
        gridDiv.appendChild(rowDiv);
    });

    // Display recommendations
    const recDiv = document.getElementById("recommendations");
    recDiv.innerHTML = "<h3>Recommendations:</h3>";
    const ul = document.createElement("ul");
    data.recommendations.forEach(rec => {
        const li = document.createElement("li");
        li.innerText = rec;
        ul.appendChild(li);
    });
    recDiv.appendChild(ul);
}
