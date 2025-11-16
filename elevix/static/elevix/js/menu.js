document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('.burger-menu');
  const sideMenu = document.querySelector('.menu-right-side');
  const dropdownMenu = document.querySelector('.dropdown-menu-small');
  const menuwrap = document.querySelector('.menu_wrap');

  function handleResizeLogic() {
    if (window.innerWidth > 768) {
      sideMenu?.classList.remove('active-menu');
      button?.classList.remove('active');
      dropdownMenu?.classList.remove('dropdown-menu-small-active');
    }

    if (menuwrap && sideMenu) {
      const menuHeight = menuwrap.offsetHeight;
      sideMenu.style.marginTop = menuHeight + 'px';
    }
  }

  button?.addEventListener("click", () => {
    button.classList.toggle("active");
    sideMenu.classList.toggle("active-menu");
  });

  document.querySelector(".drop")?.addEventListener("click", () => {
    dropdownMenu?.classList.toggle("dropdown-menu-small-active");
  });

  window.addEventListener("resize", handleResizeLogic);
  handleResizeLogic();
});