
    const btnup = document.querySelector('.btn-up');
    btnup.addEventListener("click", function () {
      const h = window.screenY;
      const speed = (h * 600) / 4400;
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    })