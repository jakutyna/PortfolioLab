document.addEventListener("DOMContentLoaded", function() {

    document.querySelector("header").classList.add("header--form-page");

//    const stepOneCheckboxes = document.querySelectorAll("[data-step='1']")[1].querySelectorAll(".form-group--checkbox");
//
//    Array.from(stepOneCheckboxes).forEach(el => {
//        const checkboxLabel = el.firstElementChild;
//        const checkboxInput = checkboxLabel.firstElementChild;
//        const checkboxInnerText = checkboxLabel.innerText;
//
//        console.log(checkboxInput.outerHTML + "\n<span class='checkbox'></span>\n<span class='description'>" +
//                     checkboxInnerText + "</span>");
//
//        checkboxLabel.innerHTML = (checkboxInput.outerHTML + "\n<span class='checkbox'></span>\n<span class='description'>" +
//                     checkboxInnerText + "</span>");
//    })

    const stepThree = document.querySelectorAll("[data-step='3']")
    if (stepThree[1] !== undefined) {
            const stepThreeCheckboxes = stepThree[1].querySelectorAll(".form-group--checkbox");

            [...stepThreeCheckboxes].forEach(el => {

            const checkboxLabel = el.querySelector(".title")
            const checkboxDescr = el.querySelector(".subtitle")

            let labelSplit = checkboxLabel.innerText.split("<br>")

            checkboxLabel.innerText = labelSplit[0]
            checkboxDescr.innerText += labelSplit[1]

        })
    }


})