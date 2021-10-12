const hamburger = document.querySelector(".fa-bars");
const dropdownMenu = document.querySelector(".nav-menu");

hamburger.addEventListener('click', mobileMenu);

function mobileMenu() {
    dropdownMenu.classList.toggle("dropdown");
}