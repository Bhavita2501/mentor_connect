document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    }
    
    // Add animation to elements with data-animate attribute
    const animatedElements = document.querySelectorAll('[data-animate]');
    animatedElements.forEach(element => {
        element.classList.add('animate-fade-in');
    });
    
    // Initialize rating stars if they exist
    const ratingInputs = document.querySelectorAll('.rating-input');
    if (ratingInputs.length > 0) {
        initRatingStars();
    }
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Function to initialize rating stars
function initRatingStars() {
    const ratingContainers = document.querySelectorAll('.rating-select');
    
    ratingContainers.forEach(container => {
        const stars = container.querySelectorAll('.rating-star');
        const input = container.nextElementSibling;
        
        stars.forEach((star, index) => {
            star.addEventListener('click', () => {
                const rating = index + 1;
                
                // Update input value
                input.value = rating;
                
                // Update star styling
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.add('selected');
                        s.innerHTML = '<i class="fas fa-star"></i>';
                    } else {
                        s.classList.remove('selected');
                        s.innerHTML = '<i class="far fa-star"></i>';
                    }
                });
            });
        });
    });
}

// Debounce function for performance optimization
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}