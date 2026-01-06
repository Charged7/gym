export default function BigDropdownMenu() {
  const dropdown = document.querySelector(".block-dropdown-menu");
  if (!dropdown) return; // Якщо елементу немає — просто вийти

  const menu = dropdown.querySelector(".dropdown-menu");
  if (!menu) return;

  gsap.set(menu, {
    opacity: 0,
    y: -10,
    pointerEvents: "none"
  });

  let hideTimeout;

  dropdown.addEventListener("mouseenter", () => {
    clearTimeout(hideTimeout);

    gsap.to(menu, {
      opacity: 1,
      y: 0,
      duration: 0.25,
      pointerEvents: "auto",
      ease: "power2.out"
    });
  });

  dropdown.addEventListener("mouseleave", () => {
    hideTimeout = setTimeout(() => {
      gsap.to(menu, {
        opacity: 0,
        y: -10,
        duration: 0.2,
        pointerEvents: "none",
        ease: "power2.in"
      });
    }, 150);
  });
}