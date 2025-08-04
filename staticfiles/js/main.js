// Add event listener when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Handle messages/alerts dismissal
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0'; // Fade out the message
            setTimeout(() => message.remove(), 300); // Remove after fade out
        }, 3000);
    });




    
});

