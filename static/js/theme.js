(function () {
    "use strict";
    var KEY = "asha-care-theme";
    var root = document.documentElement;
    var saved = localStorage.getItem(KEY);
    var initial = (saved === "dark" || saved === "neon") ? saved : "light";
    root.setAttribute("data-theme", initial);

    function mountThemePicker() {
        if (document.querySelector(".asha-theme-picker")) return;
        var wrap = document.createElement("div");
        wrap.className = "asha-theme-picker";
        wrap.setAttribute("aria-label", "Theme selector");

        var label = document.createElement("label");
        label.htmlFor = "asha-theme-select";
        label.textContent = "Theme";

        var select = document.createElement("select");
        select.id = "asha-theme-select";
        select.setAttribute("aria-label", "Choose theme");
        select.innerHTML = '<option value="light">Light</option><option value="dark">Dark</option><option value="neon">Neon</option>';
        select.value = root.getAttribute("data-theme") || "light";
        select.addEventListener("change", function () {
            root.setAttribute("data-theme", select.value);
            localStorage.setItem(KEY, select.value);
        });

        wrap.appendChild(label);
        wrap.appendChild(select);
        document.body.appendChild(wrap);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", mountThemePicker);
    } else {
        mountThemePicker();
    }
})();
