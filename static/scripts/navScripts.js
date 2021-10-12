const hamburger = document.querySelector(".fa-bars");
const dropdownMenu = document.querySelector(".nav-menu");

hamburger.addEventListener('click', function () { dropdownMenu.classList.toggle("dropdown") });