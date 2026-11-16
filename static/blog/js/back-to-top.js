(function () {
  var SHOW_AFTER = 400;
  var button = document.getElementById("back-to-top");
  if (!button) return;
  var reduce = matchMedia("(prefers-reduced-motion: reduce)");

  function update() {
    button.classList.toggle("is-visible", window.scrollY > SHOW_AFTER);
  }

  window.addEventListener("scroll", update, { passive: true });
  button.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: reduce.matches ? "auto" : "smooth" });
  });
  update();
})();
