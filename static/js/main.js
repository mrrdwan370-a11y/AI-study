const menuBtn = document.getElementById("menuBtn");
const sidebar = document.getElementById("sidebar");

if (menuBtn) {
    menuBtn.addEventListener("click", () => {
        sidebar.classList.toggle("show");
    });
}


/* =========================
   DARK MODE
========================= */

const darkModeToggle =
    document.getElementById("darkModeToggle");

if (darkModeToggle) {

    darkModeToggle.addEventListener("click", (event) => {

        event.preventDefault();

        document.body.classList.toggle("dark-mode");

        const isDark =
            document.body.classList.contains("dark-mode");

        localStorage.setItem(
            "darkMode",
            isDark
        );
    });
}


if (localStorage.getItem("darkMode") === "true") {

    document.body.classList.add("dark-mode");

}