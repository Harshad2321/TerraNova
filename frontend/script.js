document.getElementById("planForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const city = document.getElementById("city").value;
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "<p>Generating plan... ⏳</p>";

    try {
        const response = await fetch("http://127.0.0.1:8000/generate_plan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ city_name: city })
        });

        if (!response.ok) {
            throw new Error("Backend error: " + response.statusText);
        }

        const data = await response.json();

        resultDiv.innerHTML = `
            <h3>Food Waste Reduction Plan for ${city}</h3>
            <p>${data.plan}</p>
        `;
    } catch (error) {
        console.error("Error:", error);
        resultDiv.innerHTML = "<p style='color:red;'>⚠️ Could not connect to backend. Is it running?</p>";
    }
});
