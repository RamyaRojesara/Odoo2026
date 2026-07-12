/** @odoo-module **/

import { ready } from "@web/core/utils/hooks";

// Plain ES6 JS for Login Interactions (Loaded on public login page without full OWL framework initialized yet)
document.addEventListener("DOMContentLoaded", () => {
    
    const loginForm = document.querySelector(".to-auth__form");
    const passwordInput = document.querySelector("#password");
    const passwordToggleBtn = document.querySelector(".js-password-toggle");
    const submitBtn = document.querySelector(".to-auth__submit-btn");

    // SVG Icons for password visibility
    const eyeIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`;
    const eyeOffIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`;

    if (passwordToggleBtn && passwordInput) {
        // Initial state
        passwordToggleBtn.innerHTML = eyeIcon;

        passwordToggleBtn.addEventListener("click", (e) => {
            e.preventDefault();
            const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
            passwordInput.setAttribute("type", type);
            passwordToggleBtn.innerHTML = type === "password" ? eyeIcon : eyeOffIcon;
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            // Client-side validation is handled by HTML5 `required` attribute.
            // On valid submit, add loading state to button to prevent double submission
            if (loginForm.checkValidity()) {
                submitBtn.classList.add("is-loading");
                // Allow the form to submit naturally
            }
        });
    }
});
