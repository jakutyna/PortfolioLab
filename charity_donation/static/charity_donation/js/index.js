document.addEventListener("DOMContentLoaded", function() {

    // Adds header class specific for this page
    document.querySelector("header").classList.add("header--main-page");

    // Changes how 'register' button is displayed
    if (document.querySelector(".nav--actions").firstElementChild.classList[0] !== "logged-user") {
        const registerButton = document.querySelector(".nav--actions").lastElementChild.firstElementChild
        registerButton.classList.add("btn--highlighted");
        registerButton.classList.remove("btn--without-border");
    }


    // Add links to page sections in navigation bar
    const navLinks = Array.from(document.querySelector(".nav--actions").nextElementSibling.children)

    navLinks[1].firstElementChild.href = "#steps"
    navLinks[2].firstElementChild.href = "#about-us"
    navLinks[3].firstElementChild.href = "#help"
    navLinks[5].firstElementChild.href = "#contact"

})