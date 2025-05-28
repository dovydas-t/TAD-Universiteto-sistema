document.addEventListener("DOMContentLoaded", function () {
    const select = document.getElementById("facultySelect");
    const infoCard = document.getElementById("faculty-info");
    const nameEl = document.getElementById("faculty-name");
    const descEl = document.getElementById("faculty-description");

    select.addEventListener("change", function () {
        const selected = select.options[select.selectedIndex];
        const name = selected.text;
        const description = selected.getAttribute("data-description") || "No description available.";

        nameEl.textContent = name;
        descEl.textContent = description;

        infoCard.style.display = "block";
    });

    if (select.value) {
        select.dispatchEvent(new Event('change'));
    }
});
