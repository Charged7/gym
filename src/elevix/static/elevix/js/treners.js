document.addEventListener("DOMContentLoaded", () => {
  const track = document.getElementById("slider-track");
  if (!track) return;

  let currentIndex = 0;

  function getSliderData() {
    const card = track.querySelector(".state-wrapper");
    if (!card) return null;

    const cardWidth = card.getBoundingClientRect().width;
    const containerWidth = track.parentElement.offsetWidth;
    const cardsPerView = Math.floor(containerWidth / cardWidth);
    const maxIndex = Math.max(track.children.length - cardsPerView, 0);

    return { cardWidth, cardsPerView, maxIndex };
  }

  function updateSlider() {
    const data = getSliderData();
    if (!data) return;

    currentIndex = Math.max(0, Math.min(currentIndex, data.maxIndex));
    let offset = currentIndex * data.cardWidth;

    if (currentIndex === data.maxIndex) {
      offset = track.children.length * data.cardWidth - track.parentElement.offsetWidth;
    }

    track.style.transform = `translateX(-${offset}px)`;
  }

  document.querySelector(".btn-prev button").addEventListener("click", () => {
    currentIndex = Math.max(currentIndex - 1, 0);
    updateSlider();
  });

  document.querySelector(".btn-next button").addEventListener("click", () => {
    const data = getSliderData();
    if (!data) return;

    currentIndex = Math.min(currentIndex + 1, data.maxIndex);
    updateSlider();
  });

  window.addEventListener("resize", updateSlider);
  updateSlider();
});

