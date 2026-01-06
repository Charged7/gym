export default function SmallDropdownMenu() {
  const toggle = document.querySelector(".menu_item-smal-size.drop");
  const menu = document.querySelector(".dropdown-menu-small");

  if (!toggle || !menu) return;

  gsap.set(menu, {
    height: 0,
    opacity: 0,
    pointerEvents: "none"
  });

  const tl = gsap.timeline({ paused: true });

  tl.to(menu, {
    height: "auto",
    opacity: 1,
    duration: 0.3,
    pointerEvents: "auto",
    ease: "power2.out"
  });

  tl.reverse();

  toggle.addEventListener("click", () => {
    tl.reversed() ? tl.play() : tl.reverse();
  });
}