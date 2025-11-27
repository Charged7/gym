document.addEventListener('DOMContentLoaded', () => {
  const track = document.getElementById("slider-track");
  const btnPrev = document.getElementById("btn-prev");
  const btnNext = document.getElementById("btn-next");

  let currentIndex = 0;
  let trainers = [];

  function updateSlider() {
    const card = track.querySelector(".trainer-card");
    if (!card) return;

    const cardWidth = card.offsetWidth;
    const containerWidth = track.parentElement.offsetWidth;

    const cardsPerView = Math.floor(containerWidth / cardWidth);
    const maxIndex = Math.max(trainers.length - cardsPerView, 0);

    currentIndex = Math.max(0, Math.min(currentIndex, maxIndex));
    const offset = currentIndex * cardWidth;

    track.style.transform = `translateX(-${offset}px)`;

    btnPrev.disabled = currentIndex === 0;
    btnNext.disabled = currentIndex === maxIndex;
  }

  btnPrev.addEventListener("click", () => {
    currentIndex--;
    updateSlider();
  });

  btnNext.addEventListener("click", () => {
    currentIndex++;
    updateSlider();
  });

  window.addEventListener("resize", updateSlider);

  fetch("/static/json/treners.json") // путь через Flask static
    .then(res => res.json())
    .then(data => {
      trainers = data;

      trainers.forEach(trainer => {
        const link = document.createElement("a");
        // используем переменную trainerPageUrl из index.html
        link.href = `${trainerPageUrl}?name=${encodeURIComponent(trainer.name)}`;
        link.className = "trainer-card";
        link.style.textDecoration = "none"; // забирає підкреслення
        link.innerHTML = `
             <div class='trainer-block-img'>
               <img src="${trainer.photo}" alt="${trainer.name}">
             </div>
             <span>${trainer.name}</span>
             <p>${trainer.experience}</p>
        `;
        track.appendChild(link);
      });

      updateSlider();
    });
});
