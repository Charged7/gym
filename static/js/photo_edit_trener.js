document.addEventListener('DOMContentLoaded', () => {
 const input = document.getElementById("photoInput");
  const preview = document.getElementById("preview");

  input.addEventListener("change", () => {
    const files = Array.from(input.files);

    files.forEach(file => {
      if (!file.type.startsWith("image/")) return;

      const img = document.createElement("img");
      img.src = URL.createObjectURL(file);
      img.classList.add('preview-img');
      preview.append(img);
    });

    input.value = "";
  });
});