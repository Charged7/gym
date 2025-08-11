document.addEventListener('DOMContentLoaded', () => {
  function onEntry(entries) {
    entries.forEach((change) => {
      if (change.isIntersecting) {
        if (change.target.classList.contains('service-item')) {
          change.target.classList.add('element-show');
        }
        if (change.target.classList.contains('h2-element')) {
          change.target.classList.add('h2-show');
        }
        if (change.target.classList.contains('ul-animate')) {
          change.target.classList.add('ul-animate-show');
        }
      }
    });
  }

  let options = { threshold: [0.6] };
  let observer = new IntersectionObserver(onEntry, options);
  let elements = document.querySelectorAll('.service-item, .title-animate, .h2-element,.ul-animate');
  elements.forEach(elm => observer.observe(elm));
});