document.getElementById("cityForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    name: document.getElementById("name").value,
    width: parseInt(document.getElementById("width").value),
    height: parseInt(document.getElementById("height").value),
    parks: parseInt(document.getElementById("parks").value),
    homes: parseInt(document.getElementById("homes").value),
    roads: parseInt(document.getElementById("roads").value),
    buildings: parseInt(document.getElementById("buildings").value),
    visuals: true
  };

  const res = await fetch("http://127.0.0.1:8000/city/plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const city = await res.json();
  renderCity(city.layout);
});

function renderCity(layout) {
  const output = document.getElementById("output");
  output.innerHTML = "";

  const grid = document.createElement("div");
  grid.className = "grid";
  grid.style.gridTemplateColumns = `repeat(${layout[0].length}, 40px)`;

  layout.forEach(row => {
    row.forEach(cell => {
      const div = document.createElement("div");
      div.className = "cell";
      div.textContent = cell;
      grid.appendChild(div);
    });
  });

  output.appendChild(grid);
}
