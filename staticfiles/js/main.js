// Add event listener when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Handle messages/alerts dismissal
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 3000);
    });

    // Course card hover effects
    const courseCards = document.querySelectorAll('.card');
    courseCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});