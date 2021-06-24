document.addEventListener("DOMContentLoaded", function() {

    // Adds header class specific for this page
    document.querySelector("header").classList.add("header--form-page");


    // Step 3 in donation form
    const stepThree = document.querySelector("div[data-step='3']")

    // Splits form fields labels to different tags so they are properly displayed on page
     if (stepThree !== undefined) {
             const stepThreeCheckboxes = stepThree.querySelectorAll(".form-group--checkbox");

             // ... - unpacks iterable (here I use it to convert querySelectorAll object to list
             [...stepThreeCheckboxes].forEach(el => {

             const checkboxLabel = el.querySelector(".title")
             const checkboxDescr = el.querySelector(".subtitle")

             let labelSplit = checkboxLabel.innerText.split("<br>")

             checkboxLabel.innerText = labelSplit[0]
             checkboxDescr.innerText += labelSplit[1]
         })
     }

})