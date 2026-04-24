// JS code to show the strenght of the password as the user is typing
const input = document.querySelector('input[name="password"]');
const indicator = document.getElementById('live-strength');

input.addEventListener('input', function() {
    const password = input.value;
    let score = 0;

    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password)) score++;

    const labels = {
        0: "Weak ❌",
        1: "Weak ❌",
        2: "Fair ⚠️",
        3: "Strong 👍",
        4: "Very Strong 💪"
    };

    indicator.textContent = password.length === 0 ? "" : labels[score];
});