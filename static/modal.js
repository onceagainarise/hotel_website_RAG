// Get modal, buttons, and toggles
const loginModal = document.getElementById("login-modal");
const loginBtn = document.getElementById("login-btn");
const closeModal = document.querySelector(".close-btn");
const toggleSignup = document.getElementById("toggle-signup");
const toggleLogin = document.getElementById("toggle-login");
const loginFields = document.getElementById("login-fields");
const signupFields = document.getElementById("signup-fields");

// Show modal when "Login/Signup" is clicked
loginBtn.addEventListener("click", (e) => {
    e.preventDefault();
    loginModal.style.display = "flex";
    document.body.style.overflow = "hidden"; // Prevent background scroll
});

// Close modal when "X" is clicked
closeModal.addEventListener("click", () => {
    loginModal.style.display = "none";
    document.body.style.overflow = "auto"; // Restore background scroll
});

// Toggle to Signup form
toggleSignup.querySelector("a").addEventListener("click", (e) => {
    e.preventDefault();
    loginFields.style.display = "none";
    signupFields.style.display = "block";
    toggleSignup.style.display = "none";
    toggleLogin.style.display = "block";
});

// Toggle to Login form
toggleLogin.querySelector("a").addEventListener("click", (e) => {
    e.preventDefault();
    loginFields.style.display = "block";
    signupFields.style.display = "none";
    toggleSignup.style.display = "block";
    toggleLogin.style.display = "none";
});

// Close modal when clicking outside modal content
window.addEventListener("click", (e) => {
    if (e.target === loginModal) {
        loginModal.style.display = "none";
        document.body.style.overflow = "auto"; // Restore background scroll
    }
});
