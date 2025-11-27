window.addEventListener("load", () => {
 const hasPlayedIntro = sessionStorage.getItem("hasPlayedIntro");

    const intro = document.getElementById("intro");
    const logo = document.getElementById("intro-logo");
    const textUnderTitle = document.querySelector(".txt-under-title");

    function showText() {
        textUnderTitle.classList.add("show");
    }

    if (!hasPlayedIntro) {
        setTimeout(() => {
            intro.classList.add("fade-out");
            logo.classList.add("move");

            logo.addEventListener("transitionend", () => {
                intro.style.display = "none";
                showText();
            }, { once: true });

        }, 2000);   

        sessionStorage.setItem("hasPlayedIntro", "true");
    } else {
        intro.style.display = "none";
        showText();
    }
});