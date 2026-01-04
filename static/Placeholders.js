function updatePlaceholder() {
    var sourceSelect = document.getElementById("sourceSelect");
    var sourceInput = document.getElementById("sourceInput");

    if (sourceSelect.value === "myself") {
        sourceInput.style.display = "none"
        sourceInput.required = false
    } else if (sourceSelect.value === "the tv series") {
        sourceInput.placeholder = `${sourceSelect.value}' name`
        sourceInput.style.display = "inline"
        sourceInput.required = true
    } else {
        sourceInput.placeholder = `${sourceSelect.value}'s name`
        sourceInput.style.display = "inline"
        sourceInput.required = true
    }
}