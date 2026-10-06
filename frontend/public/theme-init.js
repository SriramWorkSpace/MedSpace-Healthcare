// Apply the saved theme before first paint to avoid a flash.
(function () {
  try {
    var t = localStorage.getItem("ms-theme");
    var dark =
      t === "dark" || (t !== "light" && matchMedia("(prefers-color-scheme: dark)").matches);
    document.documentElement.dataset.theme = dark ? "dark" : "light";
  } catch {
    // Storage blocked (private mode): the CSS falls back to the system theme.
  }
})();
