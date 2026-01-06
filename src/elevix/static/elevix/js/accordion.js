document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector(".block-accordions");
    if (!container) return;


    document.querySelectorAll('.accordion-details').forEach(details => {
    details.addEventListener('toggle', () => {
    if (details.open) {
      document.querySelectorAll('.accordion-details').forEach(d => {
        if (d !== details) d.open = false;
      });
    }
  });
});

});