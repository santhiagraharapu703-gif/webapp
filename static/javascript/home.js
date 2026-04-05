document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.getElementById("navbar");
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");
    const revealElements = document.querySelectorAll(".reveal");

    // Navbar scroll effect
    window.addEventListener("scroll", function () {
        if (window.scrollY > 40) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });

    // Mobile menu toggle
    menuToggle.addEventListener("click", function () {
        navLinks.classList.toggle("show");
    });

    // Reveal animation on scroll
    function revealOnScroll() {
        const triggerBottom = window.innerHeight * 0.88;

        revealElements.forEach((element) => {
            const top = element.getBoundingClientRect().top;

            if (top < triggerBottom) {
                element.classList.add("active");
            }
        });
    }

    revealOnScroll();
    window.addEventListener("scroll", revealOnScroll);
});