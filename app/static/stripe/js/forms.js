// Handles AJAX
// Stops page from reloading after form submission
// Stops page from reloading if email already exists
// Remove form if submission is succesfull

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('interestForm');
    const formContainer = document.getElementById('register-form-container');
    const flashMessages = document.getElementById('flash-messages');

    if (form) {  // Ensure form exists (won't if name is set)
        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await response.json();

                // Clear previous messages
                flashMessages.innerHTML = '';

                if (data.success) {
                    // Hide form and show success message
                    formContainer.style.display = 'none';
                    flashMessages.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
                } else {
                    // Show error message, keep form visible
                    flashMessages.innerHTML = `<div class="alert alert-warning">${data.message}</div>`;
                }
            } catch (error) {
                flashMessages.innerHTML = '<div class="alert alert-danger">Something went wrong. Please try again.</div>';
            }
        });
    }
});