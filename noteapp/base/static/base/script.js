const noteButton = document.querySelector(".create-note-button")


noteButton.onclick = function changeDisplay () {
    const form = document.querySelector("#create-note-form");
    const formDisplay = window.getComputedStyle(form).display;
    console.log(`formdisplay is currently ${formDisplay}`);
    form.style.display = formDisplay == "none" ? "block" : "none";

    buttonText = noteButton.textContent;
    noteButton.textContent = buttonText == "Create new note" ? "Hide note form" : "Create new note";
}