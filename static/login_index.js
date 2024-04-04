function toggleForm() {
    var loginForm = document.getElementById('login-form');
    var signupForm = document.getElementById('signup-form');
    var switchButton = document.getElementById('switchButton');

    if (loginForm.style.display === 'none') {
        loginForm.style.display = 'block';
        signupForm.style.display = 'none';
        switchButton.textContent = 'Switch to Sign Up';
    } else {
        loginForm.style.display = 'none';
        signupForm.style.display = 'block';
        switchButton.textContent = 'Switch to Login';
    }
}

function validatePasswords() {
    var password = document.getElementById("password").value;
    var confirm_password = document.getElementById("confirm_password").value;

    if (password !== confirm_password) {
        alert("Passwords do not match.");
    }
}
