// 1:1 Advisory Modal Handlers
const advisoryModal = document.getElementById('advisoryModal');
const consultationButtons = document.querySelectorAll('.free-consultancy-btn');
const closeAdvisoryModal = document.getElementById('closeAdvisoryModal');
const advisoryForm = document.getElementById('advisoryForm');
const submitBtn = document.getElementById("consultationSubmitBtn");

const btnText = submitBtn.querySelector(".btn-text");

const btnLoader = submitBtn.querySelector(".btn-loader");
const phoneInput = document.getElementById('advPhone');
const phoneError = document.getElementById('phoneErrorMsg');

phoneInput.addEventListener("input", function () {

    let value = this.value;

    // Remove anything except digits and +
    value = value.replace(/[^\d+]/g, "");

    // + is only allowed at the beginning
    if (value.includes("+")) {
        value = "+" + value.replace(/\+/g, "");
    }

    this.value = value;
});

// Glass Success Popup Handlers
const advisorySuccessPopup = document.getElementById('advisorySuccessPopup');
const closeSuccessPopup = document.getElementById('closeSuccessPopup');

consultationButtons.forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault();
        advisoryModal.classList.add('show');
    });
});

closeAdvisoryModal.addEventListener('click', () => {
    advisoryModal.classList.remove('show');
    phoneError.classList.add('hidden');
    phoneInput.classList.remove('border-red-500');
});

closeSuccessPopup.addEventListener('click', () => {
    advisorySuccessPopup.classList.remove('show');
});

// Close overlays when clicking outside the boxes
window.addEventListener('click', function (event) {
    if (event.target === advisoryModal) {
        advisoryModal.classList.remove('show');
        phoneError.classList.add('hidden');
        phoneInput.classList.remove('border-red-500');
    }
    if (event.target === advisorySuccessPopup) {
        advisorySuccessPopup.classList.remove('show');
    }
});

// Handle Form Submit & Validation
// ==========================================================
// Consultation Form Submission
// ==========================================================

advisoryForm.addEventListener("submit", async function (e) {

    e.preventDefault();
    if (submitBtn.disabled) {
        return;
    }

    const phoneVal = phoneInput.value.trim();

    // Accepts:
    // +9715XXXXXXXX
    // 05XXXXXXXX
    const uaeRegex = /^(\+9715\d{8}|05\d{8})$/;

    if (!uaeRegex.test(phoneVal)) {

        phoneError.classList.remove("hidden");

        phoneInput.style.borderColor = "#fb7185";

        phoneInput.focus();

        return;

    }

    phoneError.classList.add("hidden");

    phoneInput.style.borderColor = "";

    const formData = new FormData(advisoryForm);
    submitBtn.disabled = true;

    btnText.style.display = "none";

    btnLoader.style.display = "flex";

    const csrfToken = advisoryForm.querySelector(
        '[name=csrfmiddlewaretoken]'
    ).value;

    try {

        const response = await fetch(advisoryForm.action, {

            method: "POST",

            headers: {

                "X-CSRFToken": csrfToken,

            },

            body: formData,

        });

        const data = await response.json();

        if (data.success) {

            advisoryModal.classList.remove("show");

            advisorySuccessPopup.classList.add("show");

            advisoryForm.reset();

            submitBtn.disabled = false;

            btnLoader.style.display = "none";

            btnText.style.display = "inline";

        }

        else {
            submitBtn.disabled = false;

            btnLoader.style.display = "none";

            btnText.style.display = "inline";

            alert("Please correct the highlighted errors.");

            console.log(data.errors);

        }

    }

    catch (error) {
        submitBtn.disabled = false;

        btnLoader.style.display = "none";

        btnText.style.display = "inline";

        console.error(error);

        alert("Something went wrong. Please try again.");

    }

});