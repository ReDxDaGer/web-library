// JavaScript for toggling dark mode
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}

let items = document.querySelectorAll(".main");
function mobMenu(){
for(let i = 0; i<4; i++){
        items[i].classList.toggle("hide");
        }
}