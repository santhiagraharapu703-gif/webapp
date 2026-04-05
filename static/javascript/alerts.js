document.addEventListener("DOMContentLoaded", function () {
    const checkBtn = document.getElementById("checkAlertBtn");
    const stateInput = document.getElementById("stateInput");
    const resultBox = document.getElementById("alertResult");

    function formatNumber(value) {
        if (value === null || value === undefined || value === "N/A") {
            return "N/A";
        }

        const num = Number(value);
        if (isNaN(num)) {
            return value;
        }

        return num.toFixed(2);
    }

    if (checkBtn) {
        checkBtn.addEventListener("click", async function () {
            const stateName = stateInput.value.trim();

            if (!stateName) {
                resultBox.innerHTML = `<p>Please enter a state name.</p>`;
                return;
            }

            try {
                const response = await fetch(`/api/check-alert?state_name=${encodeURIComponent(stateName)}`);
                const data = await response.json();

                resultBox.innerHTML = `
                    <h2>${data.title}</h2>
                    <p><strong>State:</strong> ${data.state_name ?? "N/A"}</p>
                    <p><strong>Year:</strong> ${data.year ?? "N/A"}</p>
                    <p><strong>AQI:</strong> ${formatNumber(data.aqi)}</p>
                    <p><strong>Forest Cover %:</strong> ${formatNumber(data.forest_cover)}</p>
                    <p><strong>CO₂ Emissions:</strong> ${formatNumber(data.co2)}</p>
                    <p><strong>Risk Score:</strong> ${formatNumber(data.risk_score)}</p>
                    <p><strong>Status:</strong> ${data.message ?? "N/A"}</p>
                    <p><strong>Recommended Action:</strong> ${data.action ?? "N/A"}</p>
                `;
            } catch (error) {
                resultBox.innerHTML = `<p>Something went wrong while fetching alert data.</p>`;
                console.error(error);
            }
        });
    }
});