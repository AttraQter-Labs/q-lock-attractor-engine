// Smooth scroll for all internal navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute("href")).scrollIntoView({
      behavior: "smooth"
    });
  });
});

// Fade-in animation for hero sections
window.addEventListener("load", () => {
  const hero = document.querySelector(".hero");
  if (hero) {
    hero.style.opacity = 0;
    hero.style.transition = "opacity 1.2s ease";
    setTimeout(() => { hero.style.opacity = 1 }, 150);
  }
});
