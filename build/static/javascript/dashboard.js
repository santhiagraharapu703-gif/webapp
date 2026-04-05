console.log("Dashboard Loaded");

// Example animation
document.querySelectorAll(".card").forEach(card => {
  card.addEventListener("mouseover", () => {
    card.style.transform = "scale(1.05)";
  });
});