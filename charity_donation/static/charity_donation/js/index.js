document.addEventListener("DOMContentLoaded", function() {

    document.querySelector("header").classList.add("header--main-page");

    const registerButton = document.querySelector(".nav--actions").lastElementChild.firstElementChild
    registerButton.classList.add("btn--highlighted");
    registerButton.classList.remove("btn--without-border");

    const navLinks = Array.from(document.querySelector(".nav--actions").nextElementSibling.children)

    navLinks[1].firstElementChild.href = "#steps"
    navLinks[2].firstElementChild.href = "#about-us"
    navLinks[3].firstElementChild.href = "#help"
    navLinks[5].firstElementChild.href = "#contact"

})