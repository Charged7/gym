document.addEventListener('DOMContentLoaded', () => {
  const texnology = ["zal", "boks", "mma", "macaz", "swim"];

  const mn = {
    "year_2020": { zal: 85, boks: 60, mma: 50, macaz: 70, swim: 50 },
    "year_2021": { zal: 110, boks: 70, mma: 70, macaz: 90, swim: 70 },
    "year_2022": { zal: 130, boks: 80, mma: 90, macaz: 80, swim: 90 },
    "year_2023": { zal: 160, boks: 100, mma: 110, macaz: 95, swim: 80 },
    "year_2024": { zal: 95, boks: 60, mma: 60, macaz: 105, swim: 50 },
  };

  let chartInterval = setInterval(doAutoChart, 3000);
  let descInterval = null;

  function doChart(el) {
    const buttons = document.querySelectorAll("button");
    const index = Array.from(buttons).indexOf(el);
    document.getElementById("num").value = index;
    drawChart(index);

    clearInterval(chartInterval);
    chartInterval = setInterval(doAutoChart, 3000);
  }

  function doAutoChart() {
    const numInput = document.getElementById("num");
    let nextIndex = Number(numInput.value) + 1;
    if (nextIndex > 4) nextIndex = 0;
    numInput.value = nextIndex;
    drawChart(nextIndex);
  }

  function drawChart(index) {
    const buttons = document.querySelectorAll("button");
    const btn = buttons[index];
    if (!btn) return;

    const yearKey = btn.id;

    texnology.forEach(tech => {
      const value = mn[yearKey][tech];
      const elem = document.getElementById(tech);
      if (elem) {
        elem.style.height = (value + 30) + "px";
      }
    });

    doBut(index);
    doDscrb();
  }

  function doBut(index) {
    document.querySelectorAll(".open").forEach(el => el.classList.remove("open"));
    const buttons = document.querySelectorAll(".cntnt_btn button");
    if (buttons[index]) {
      buttons[index].classList.add("open");
    }
  }

  function doDscrb() {
    clearInterval(descInterval);
    descInterval = setInterval(() => {
      const states = document.querySelectorAll(".state_wrp");
      const descs = document.querySelectorAll(".dscrpt");

      states.forEach((el, i) => {
        const height = el.offsetHeight;
        const value = Math.round(height) - 30;
        if (descs[i]) {
          descs[i].textContent = value;
        }
      });
    }, 50);
  }

  drawChart(0);

  document.querySelectorAll(".cntnt_btn button").forEach(btn => {
    btn.addEventListener("click", () => doChart(btn));
  });
});