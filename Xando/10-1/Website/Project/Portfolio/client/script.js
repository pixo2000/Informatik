document.addEventListener('DOMContentLoaded', function() {
    // Work in Progress Popup
    const wipPopup = document.getElementById('wip-popup');
    const wipCloseBtn = document.querySelector('.wip-popup-close');
    const wipContinueBtn = document.querySelector('.wip-continue-btn');
    const wipContactBtn = document.querySelector('.wip-contact-btn');

    // Check if user has already seen the popup today
    const today = new Date().toDateString();
    const lastSeen = localStorage.getItem('wip-popup-seen');
    
    if (lastSeen !== today) {
        // Show popup after a short delay
        setTimeout(() => {
            wipPopup.classList.remove('hidden');
        }, 1000);
    } else {
        // Hide popup immediately if already seen today
        wipPopup.classList.add('hidden');
    }

    // Close popup and remember choice
    function closePopup() {
        wipPopup.classList.add('hidden');
        localStorage.setItem('wip-popup-seen', today);
    }

    // Event listeners for popup
    if (wipCloseBtn) {
        wipCloseBtn.addEventListener('click', closePopup);
    }

    if (wipContinueBtn) {
        wipContinueBtn.addEventListener('click', closePopup);
    }

    if (wipContactBtn) {
        wipContactBtn.addEventListener('click', () => {
            closePopup();
            // Scroll to contact section
            setTimeout(() => {
                document.querySelector('#contact').scrollIntoView({
                    behavior: 'smooth'
                });
            }, 500);
        });
    }

    // Close popup when clicking outside
    wipPopup.addEventListener('click', (e) => {
        if (e.target === wipPopup) {
            closePopup();
        }
    });

    // Close popup with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !wipPopup.classList.contains('hidden')) {
            closePopup();
        }
    });

    // Mobile Navigation
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');
    const body = document.body;

    burger.addEventListener('click', () => {
        // Toggle Navigation
        nav.classList.toggle('active');
        burger.classList.toggle('active');
        body.classList.toggle('nav-active');

        // Animate Links
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
            }
        });
    });

    // Close mobile menu when clicking a link
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (nav.classList.contains('active')) {
                nav.classList.remove('active');
                burger.classList.remove('active');
                body.classList.remove('nav-active');
                
                navLinks.forEach(link => {
                    link.style.animation = '';
                });
            }
        });
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Portfolio filtering
    const filterButtons = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');

    // Ensure all portfolio items are visible initially
    portfolioItems.forEach(item => {
        item.style.display = 'block';
        item.style.opacity = '1';
        item.style.transform = 'translateY(0)';
    });

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');

            const filterValue = button.getAttribute('data-filter');

            portfolioItems.forEach((item, index) => {
                const itemCategory = item.getAttribute('data-category');
                
                if (filterValue === 'all' || itemCategory === filterValue) {
                    // Show item
                    item.style.display = 'block';
                    
                    // Animate in with delay
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'translateY(0)';
                    }, index * 100);
                } else {
                    // Hide item
                    item.style.opacity = '0';
                    item.style.transform = 'translateY(-20px)';
                    
                    setTimeout(() => {
                        item.style.display = 'none';
                    }, 300);
                }
            });
        });
    });

    // Form submission with enhanced validation
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const company = document.getElementById('company').value.trim();
            const service = document.getElementById('service').value;
            const subject = document.getElementById('subject').value.trim();
            const message = document.getElementById('message').value.trim();
            
            // Enhanced form validation
            if (!name || !email || !message || !service) {
                showNotification('Bitte füllen Sie alle Pflichtfelder (*) aus.', 'error');
                return;
            }

            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                showNotification('Bitte geben Sie eine gültige E-Mail-Adresse ein.', 'error');
                return;
            }

            // Show loading state
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Wird gesendet...';
            submitBtn.disabled = true;

            // Simulate form submission (replace with actual API call)
            setTimeout(() => {
                showNotification('Vielen Dank für Ihre Nachricht! Ich melde mich innerhalb von 24 Stunden bei Ihnen.', 'success');
                
                // Reset form
                contactForm.reset();
                
                // Reset button
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }

    // Notification system
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notification => notification.remove());

        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            z-index: 10000;
            min-width: 300px;
            max-width: 500px;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        notification.querySelector('.notification-content').style.cssText = `
            display: flex;
            align-items: center;
            gap: 10px;
        `;

        notification.querySelector('.notification-close').style.cssText = `
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            margin-left: auto;
            padding: 0;
            font-size: 1.2rem;
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, 5000);
    }

    // Scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation - including portfolio items
    const animatedElements = document.querySelectorAll('.service-card, .portfolio-item, .factor, .price-category');
    animatedElements.forEach((el, index) => {
        // Only animate if not portfolio item (portfolio items have their own animation)
        if (!el.classList.contains('portfolio-item')) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            // Add staggered delay
            el.style.transitionDelay = `${index * 0.1}s`;
        }
        observer.observe(el);
    });

    // Ensure sections are visible on page load
    const sections = document.querySelectorAll('#services, #portfolio');
    sections.forEach(section => {
        section.style.display = 'block';
        section.style.visibility = 'visible';
    });

    // Header scroll effect
    window.addEventListener('scroll', () => {
        const header = document.querySelector('header');
        if (window.scrollY > 100) {
            header.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
            header.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
            header.style.boxShadow = '0 1px 2px 0 rgba(0, 0, 0, 0.05)';
        }
    });
});
