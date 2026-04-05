const statesData = [
    { name: "Andhra Pradesh", image: "/static/images/AP1.jpg" },
    { name: "Arunachal Pradesh", image: "/static/images/Arunachal Pradesh.jpg" },
    { name: "Assam", image: "/static/images/Assam.jpg" },
    { name: "Bihar", image: "/static/images/Bihar.jpg" },
    { name: "Chhattisgarh", image: "/static/images/Chhattisgarh.jpg" },
    { name: "Goa", image: "/static/images/Goa.jpg" },
    { name: "Gujarat", image: "/static/images/Gujarat.jpg" },
    { name: "Haryana", image: "/static/images/Haryana.jpg" },
    { name: "Himachal Pradesh", image: "/static/images/Himachal Pradesh.jpg" },
    { name: "Jharkhand", image: "/static/images/Jharkhand.jpg" },
    { name: "Karnataka", image: "/static/images/Karnataka.jpg" },
    { name: "Kerala", image: "/static/images/Kerala.jpg" },
    { name: "Madhya Pradesh", image: "/static/images/Madhya Pradesh.jpg" },
    { name: "Maharashtra", image: "/static/images/Maharashtra.jpg" },
    { name: "Manipur", image: "/static/images/Manipur.jpg" },
    { name: "Meghalaya", image: "/static/images/Meghalaya.jpg" },
    { name: "Mizoram", image: "/static/images/Mizoram.jpg" },
    { name: "Nagaland", image: "/static/images/Nagaland.jpg" },
    { name: "Odisha", image: "/static/images/Odisha.jpg" },
    { name: "Punjab", image: "/static/images/Punjab.jpg" },
    { name: "Rajasthan", image: "/static/images/Rajasthan.jpg" },
    { name: "Sikkim", image: "/static/images/Sikkim.jpg" },
    { name: "Tamil Nadu", image: "/static/images/Tamil Nadu.jpg" },
    { name: "Telangana", image: "/static/images/Telangana.jpg" },
    { name: "Tripura", image: "/static/images/Tripura.jpg" },
    { name: "Uttar Pradesh", image: "/static/images/Uttar Pradesh.jpg" },
    { name: "Uttarakhand", image: "/static/images/Uttarakhand.jpg" },
    { name: "West Bengal", image: "/static/images/West Bengal.jpg" }
];

document.addEventListener("DOMContentLoaded", function () {
    const statesGrid = document.getElementById("statesGrid");
    const searchInput = document.getElementById("searchInput");

    function renderStates(data) {
        statesGrid.innerHTML = "";

        if (data.length === 0) {
            statesGrid.innerHTML = `
                <div class="no-results">
                    <p>No states found.</p>
                </div>
            `;
            return;
        }

        data.forEach(state => {
            const stateUrl = state.name.toLowerCase().replace(/\s+/g, "-");

            const card = document.createElement("div");
            card.className = "state-card";

            card.innerHTML = `
                <div class="state-image-box">
                    <img src="${state.image}" alt="${state.name}"
                         onerror="this.onerror=null; this.src='/static/images/logo.jpg';">
                </div>

                <div class="state-card-content">
                    <h3>${state.name}</h3>
                    <p>Explore environmental overview and state-level insights.</p>
                    <a href="/state/${stateUrl}" class="view-btn">View Details</a>
                </div>
            `;

            statesGrid.appendChild(card);
        });
    }

    renderStates(statesData);

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const searchValue = this.value.toLowerCase().trim();

            const filteredStates = statesData.filter(state =>
                state.name.toLowerCase().includes(searchValue)
            );

            renderStates(filteredStates);
        });
    }
});