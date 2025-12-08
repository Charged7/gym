document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.burger-menu');
    const sideMenu = document.querySelector('.menu-right-side');

    button?.addEventListener("click", () => {
        button.classList.toggle("active");
        sideMenu.classList.toggle("active-menu");
    });

  function handleResizeLogic() {
  if (window.innerWidth > 992) {
    sideMenu?.classList.remove('active-menu');
    button?.classList.remove('active');
  }
}

  window.addEventListener("resize", handleResizeLogic);
  handleResizeLogic();

});