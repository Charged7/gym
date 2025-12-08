document.addEventListener("DOMContentLoaded", () => {
    const track = document.querySelector(".feedback-slider");
    if (!track) return;

    let currentIndex = 0;
    let isTransitioning = false;
    const ORIGINAL_SELECTOR = ".feedbackContainer-wrapper:not(.clone)";

    // Отримуємо тільки оригінальні картки
    function getOriginalCards() {
        return Array.from(track.querySelectorAll(ORIGINAL_SELECTOR));
    }

    const originalCards = getOriginalCards();
    const originalCount = originalCards.length;
    if (originalCount === 0) return;

    // Видаляємо старі клони
    function removeClones() {
        track.querySelectorAll(".clone").forEach(n => n.remove());
    }

    // Розрахунок параметрів слайдера
    function getSliderData() {
        const cards = getOriginalCards();
        if (cards.length === 0) return null;

        const firstCard = cards[0];
        const gap = parseFloat(window.getComputedStyle(track).gap) || 0;
        const cardWidth = firstCard.offsetWidth;

        return { cardWidth: cardWidth + gap };
    }

    // Клонуємо картки для безкінечного циклу
    function cloneCards() {
        removeClones();

        const originals = getOriginalCards();

        // Клонуємо всі картки двічі для плавного циклу
        originals.forEach(card => {
            const clone = card.cloneNode(true);
            clone.classList.add("clone");
            track.appendChild(clone);
        });
    }

    // Функція слайду
    function slide() {
        if (isTransitioning) return;

        const data = getSliderData();
        if (!data) return;

        isTransitioning = true;
        currentIndex++;

        track.style.transition = "transform 0.5s ease";
        track.style.transform = `translateX(-${data.cardWidth * currentIndex}px)`;

        // Коли дійшли до кінця оригіналів - миттєво скидаємо на початок
        if (currentIndex >= originalCount) {
            setTimeout(() => {
                track.style.transition = "none";
                currentIndex = 0;
                track.style.transform = `translateX(0)`;

                // Повертаємо transition через мікрозатримку
                setTimeout(() => {
                    isTransitioning = false;
                }, 50);
            }, 500); // Чекаємо завершення анімації
        } else {
            setTimeout(() => {
                isTransitioning = false;
            }, 500);
        }
    }

    // Ініціалізація
    cloneCards();
    track.style.transform = `translateX(0)`;

    // Інтервал автопрокрутки
    let intervalId = setInterval(slide, 3500);

    // Обробка resize
    let resizeTimeout;
    window.addEventListener("resize", () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            const data = getSliderData();
            if (!data) return;

            // Перестворюємо клони
            cloneCards();

            // Встановлюємо правильну позицію
            track.style.transition = "none";
            track.style.transform = `translateX(-${data.cardWidth * currentIndex}px)`;

            // Перезапускаємо інтервал
            clearInterval(intervalId);
            intervalId = setInterval(slide, 3500);
        }, 250);
    });

    // Очищення при виході зі сторінки
    window.addEventListener("beforeunload", () => {
        clearInterval(intervalId);
    });
});