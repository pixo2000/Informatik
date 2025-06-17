document.addEventListener('DOMContentLoaded', function() {
    // Dark mode functionality
    const darkModeToggle = document.getElementById('darkModeToggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 
                        (prefersDarkScheme.matches ? 'dark' : 'light');
    
    // Apply theme on page load
    applyTheme(currentTheme);
    
    // Dark mode toggle event listener
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
    
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        if (darkModeToggle) {
            darkModeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }
    
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navList = document.querySelector('.nav-list');
    const body = document.body;
    
    if (mobileMenuToggle && navList) {
        mobileMenuToggle.addEventListener('click', function() {
            const isActive = navList.classList.contains('active');
            
            if (isActive) {
                navList.classList.remove('active');
                mobileMenuToggle.innerHTML = '☰';
                body.style.overflow = '';
            } else {
                navList.classList.add('active');
                mobileMenuToggle.innerHTML = '✕';
                body.style.overflow = 'hidden';
            }
        });
    }

    // Navigation handling for both single page and multi-page
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // If it's a hash link (single page navigation)
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetSection = document.querySelector(href);
                
                if (targetSection) {
                    const headerHeight = document.querySelector('.header').offsetHeight;
                    const targetPosition = targetSection.offsetTop - headerHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
            
            // Close mobile menu after clicking
            if (navList) {
                navList.classList.remove('active');
                if (mobileMenuToggle) {
                    mobileMenuToggle.innerHTML = '☰';
                }
                body.style.overflow = '';
            }
        });
    });

    // Active navigation highlighting for single page
    function updateActiveNav() {
        const sections = document.querySelectorAll('section[id]');
        const scrollPos = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    // Header scroll effect
    function handleHeaderScroll() {
        const header = document.querySelector('.header');
        if (header) {
            if (window.scrollY > 100) {
                header.style.background = document.documentElement.getAttribute('data-theme') === 'dark' 
                    ? 'rgba(52, 73, 94, 0.95)' 
                    : 'rgba(255, 255, 255, 0.95)';
                header.style.backdropFilter = 'blur(10px)';
            } else {
                header.style.background = '';
                header.style.backdropFilter = 'none';
            }
        }
    }

    // Scroll event listeners
    window.addEventListener('scroll', function() {
        updateActiveNav();
        handleHeaderScroll();
        animateOnScroll();
    });

    // Animation on scroll
    function animateOnScroll() {
        const elements = document.querySelectorAll('.news-card, .service-card, .stat, .feature-card, .event-item, .value-card, .form-card');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('fade-in');
            }
        });
    }

    // Contact form handling
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const firstName = contactForm.querySelector('#firstName')?.value || '';
            const lastName = contactForm.querySelector('#lastName')?.value || '';
            const email = contactForm.querySelector('#email')?.value || '';
            const message = contactForm.querySelector('#message')?.value || '';
            const privacy = contactForm.querySelector('#privacy')?.checked || false;
            
            // Basic validation
            if (!firstName || !lastName || !email || !message) {
                showNotification('Bitte füllen Sie alle Pflichtfelder aus.', 'error');
                return;
            }
            
            if (!privacy) {
                showNotification('Bitte stimmen Sie der Datenschutzerklärung zu.', 'error');
                return;
            }
            
            // Simulate form submission
            showNotification('Nachricht wird gesendet...', 'info');
            
            setTimeout(() => {
                showNotification('Ihre Nachricht wurde erfolgreich gesendet!', 'success');
                contactForm.reset();
            }, 1000);
        });
    }

    // Calendar filter functionality
    const filterCheckboxes = document.querySelectorAll('.filter-checkbox input[type="checkbox"]');
    
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const filterType = this.getAttribute('data-filter');
            const eventItems = document.querySelectorAll('.event-item');
            
            eventItems.forEach(item => {
                const eventType = item.querySelector('.event-type');
                if (eventType && eventType.classList.contains(filterType)) {
                    item.style.display = this.checked ? 'flex' : 'none';
                }
            });
        });
    });

    // Notification system
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 9999;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        
        // Set background color based on type
        switch(type) {
            case 'success':
                notification.style.backgroundColor = '#28a745';
                break;
            case 'error':
                notification.style.backgroundColor = '#dc3545';
                break;
            case 'info':
                notification.style.backgroundColor = '#17a2b8';
                break;
            default:
                notification.style.backgroundColor = '#6c757d';
        }
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto remove after 4 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }, 4000);
    }

    // Initialize animations
    animateOnScroll();

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (navList && !e.target.closest('.nav') && navList.classList.contains('active')) {
            navList.classList.remove('active');
            if (mobileMenuToggle) {
                mobileMenuToggle.innerHTML = '☰';
            }
            body.style.overflow = '';
        }
    });

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navList && navList.classList.contains('active')) {
            navList.classList.remove('active');
            if (mobileMenuToggle) {
                mobileMenuToggle.innerHTML = '☰';
            }
            body.style.overflow = '';
        }
    });

    // System theme change detection
    prefersDarkScheme.addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Initialize current page navigation highlighting
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    navLinks.forEach(link => {
        const linkHref = link.getAttribute('href');
        if (linkHref === currentPage || (currentPage === '' && linkHref === 'index.html')) {
            link.classList.add('active');
        }
    });
});
