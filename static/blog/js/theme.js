(function () {
    var KEY = "theme";
    var root = document.documentElement;
    var query = matchMedia("(prefers-color-scheme: dark)");

    function stored() {
        try {
            return localStorage.getItem(KEY);
        } catch (e) {
            return null;
        }
    }

    function apply(theme) {
        root.setAttribute("data-bs-theme", theme);
    }

    apply(stored() || (query.matches ? "dark" : "light"));

    query.addEventListener("change", function () {
        if (!stored()) apply(query.matches ? "dark" : "light");
    });

    document.addEventListener("DOMContentLoaded", function () {
        var button = document.getElementById("theme-toggle");
        if (!button) return;
        button.addEventListener("click", function () {
            var next = root.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
            apply(next);
            try {
                localStorage.setItem(KEY, next);
            } catch (e) {}
        });
    });
})();
