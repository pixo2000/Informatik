// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeTabs();
    initializeScrollEffects();
    initializeForms();
    initializeLazyLoading();
    initializeAnimations();
});

// Navigation functionality
function initializeNavigation() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Mobile menu toggle
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
        
        // Animate hamburger bars
        const bars = hamburger.querySelectorAll('.bar');
        if (hamburger.classList.contains('active')) {
            bars[0].style.transform = 'rotate(-45deg) translate(-5px, 6px)';
            bars[1].style.opacity = '0';
            bars[2].style.transform = 'rotate(45deg) translate(-5px, -6px)';
        } else {
            bars[0].style.transform = 'none';
            bars[1].style.opacity = '1';
            bars[2].style.transform = 'none';
        }
    });

    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            resetHamburgerBars();
        });
    });

    // Smooth scrolling for anchor links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Active navigation highlight
    window.addEventListener('scroll', updateActiveNavigation);
}

function resetHamburgerBars() {
    const bars = document.querySelectorAll('.hamburger .bar');
    bars.forEach(bar => {
        bar.style.transform = 'none';
        bar.style.opacity = '1';
    });
}

function updateActiveNavigation() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    const scrollPosition = window.scrollY + 100;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (scrollPosition >= sectionTop && scrollPosition <= sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

// Tab functionality
function initializeTabs() {
    // Schedule tabs
    const scheduleTabBtns = document.querySelectorAll('.schedule-tabs .tab-btn');
    const scheduleTables = document.querySelectorAll('.schedule-table');

    scheduleTabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const location = this.getAttribute('data-location');
            
            // Update active tab
            scheduleTabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Show corresponding table
            scheduleTables.forEach(table => {
                table.classList.remove('active');
                if (table.id === `${location}-schedule`) {
                    table.classList.add('active');
                }
            });
        });
    });

    // Pricing tabs
    const pricingTabBtns = document.querySelectorAll('.pricing-tabs .tab-btn');
    const pricingTables = document.querySelectorAll('.pricing-table');

    pricingTabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const location = this.getAttribute('data-pricing');
            
            // Update active tab
            pricingTabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Show corresponding table
            pricingTables.forEach(table => {
                table.classList.remove('active');
                if (table.id === `${location}-pricing`) {
                    table.classList.add('active');
                }
            });
        });
    });
}

// Scroll effects
function initializeScrollEffects() {
    const navbar = document.getElementById('navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });

    // Parallax effect for hero section
    const hero = document.querySelector('.hero');
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallax = scrolled * 0.5;
        if (hero) {
            hero.style.transform = `translateY(${parallax}px)`;
        }
    });
}

// Form handling
function initializeForms() {
    const contactForm = document.querySelector('.contact-form form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmission(this);
        });
    }

    // Form validation
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
}

function handleFormSubmission(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Show loading state
    const originalText = submitButton.innerHTML;
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Wird gesendet...';
    submitButton.disabled = true;

    // Simulate form submission (replace with actual form handling)
    setTimeout(() => {
        showNotification('Nachricht erfolgreich gesendet!', 'success');
        form.reset();
        
        // Reset button
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
    }, 2000);
}

function validateField(e) {
    const field = e.target;
    const value = field.value.trim();
    
    // Remove existing error
    clearFieldError(e);
    
    // Validation rules
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, 'Dieses Feld ist erforderlich');
        return false;
    }
    
    if (field.type === 'email' && value && !isValidEmail(value)) {
        showFieldError(field, 'Bitte geben Sie eine gültige E-Mail-Adresse ein');
        return false;
    }
    
    return true;
}

function clearFieldError(e) {
    const field = e.target;
    const errorElement = field.parentNode.querySelector('.field-error');
    if (errorElement) {
        errorElement.remove();
    }
    field.style.borderColor = '';
}

function showFieldError(field, message) {
    field.style.borderColor = '#e74c3c';
    
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.style.color = '#e74c3c';
    errorElement.style.fontSize = '0.875rem';
    errorElement.style.marginTop = '0.25rem';
    errorElement.textContent = message;
    
    field.parentNode.appendChild(errorElement);
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#2ecc71' : '#3498db'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove
    setTimeout(() => {
        removeNotification(notification);
    }, 5000);
    
    // Close button
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => removeNotification(notification));
}

function removeNotification(notification) {
    notification.style.transform = 'translateX(400px)';
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

// Lazy loading for images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => img.classList.add('loaded'));
    }
}

// Scroll animations
function initializeAnimations() {
    const animatedElements = document.querySelectorAll('.info-card, .class-card, .location-card, .pricing-card');
    
    if ('IntersectionObserver' in window) {
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        animatedElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            animationObserver.observe(el);
        });
    }
}

// Utility functions
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

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add scroll to top button
function addScrollToTopButton() {
    const scrollButton = document.createElement('button');
    scrollButton.innerHTML = '<i class="fas fa-chevron-up"></i>';
    scrollButton.className = 'scroll-to-top';
    scrollButton.setAttribute('aria-label', 'Scroll to top');
    
    scrollButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: var(--accent-color);
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        font-size: 1.2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        transform: scale(0.8);
    `;
    
    document.body.appendChild(scrollButton);
    
    // Show/hide based on scroll position
    window.addEventListener('scroll', debounce(() => {
        if (window.scrollY > 300) {
            scrollButton.style.opacity = '1';
            scrollButton.style.visibility = 'visible';
            scrollButton.style.transform = 'scale(1)';
        } else {
            scrollButton.style.opacity = '0';
            scrollButton.style.visibility = 'hidden';
            scrollButton.style.transform = 'scale(0.8)';
        }
    }, 100));
    
    scrollButton.addEventListener('click', scrollToTop);
}

// Initialize scroll to top button
addScrollToTopButton();

// Handle external links
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'A' && e.target.hostname !== window.location.hostname) {
        e.target.setAttribute('target', '_blank');
        e.target.setAttribute('rel', 'noopener noreferrer');
    }
});

// Keyboard navigation improvements
document.addEventListener('keydown', function(e) {
    // Escape key closes mobile menu
    if (e.key === 'Escape') {
        const navMenu = document.getElementById('nav-menu');
        const hamburger = document.getElementById('hamburger');
        
        if (navMenu.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            resetHamburgerBars();
        }
    }
});

// Performance optimization: Lazy load non-critical resources
function loadNonCriticalResources() {
    // Load additional fonts or scripts that aren't immediately needed
    const additionalCSS = document.createElement('link');
    additionalCSS.rel = 'stylesheet';
    additionalCSS.href = 'https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&display=swap';
    document.head.appendChild(additionalCSS);
}

// Load non-critical resources after page load
window.addEventListener('load', loadNonCriticalResources);

// Error handling for missing images
document.addEventListener('error', function(e) {
    if (e.target.tagName === 'IMG') {
        e.target.style.display = 'none';
        
        // Add placeholder div
        const placeholder = document.createElement('div');
        placeholder.style.cssText = `
            width: 100%;
            height: 200px;
            background: var(--light-pink);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-light);
            font-style: italic;
        `;
        placeholder.textContent = 'Bild wird geladen...';
        
        e.target.parentNode.insertBefore(placeholder, e.target);
    }
}, true);

// Analytics and tracking (placeholder)
function trackEvent(category, action, label) {
    // Replace with actual analytics implementation
    console.log('Event tracked:', category, action, label);
}

// Track form submissions
document.addEventListener('submit', function(e) {
    if (e.target.closest('.contact-form')) {
        trackEvent('Contact', 'Form Submit', 'Contact Form');
    }
});

// Track navigation clicks
document.addEventListener('click', function(e) {
    if (e.target.closest('.nav-link')) {
        const linkText = e.target.textContent.trim();
        trackEvent('Navigation', 'Click', linkText);
    }
});

// Service worker registration for offline support
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}
