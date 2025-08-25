// Mobile navigation menu toggle
document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            menuToggle.setAttribute(
                'aria-expanded', 
                menuToggle.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
            );
        });
    }

    // Close mobile menu when clicking on a nav link
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                navMenu.classList.remove('active');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Adjust for header height
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add animation to cards when they come into view
    const observeElements = document.querySelectorAll('.info-card, .link-card, .seminar-card, .story-card, .resource-card, .accordion-item');

    if ('IntersectionObserver' in window) {
        // Add animation class to prepare for animation
        observeElements.forEach(element => {
            element.classList.add('animate-on-scroll');
        });

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    observer.unobserve(entry.target); // Stop observing once animated
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        observeElements.forEach(element => {
            observer.observe(element);
        });
    }

    // Initialize accordion with simplified behavior
    const accordionButtons = document.querySelectorAll('.accordion-button');
    
    accordionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const accordionItem = button.parentElement;
            
            // Toggle active class immediately without transitions
            accordionItem.classList.toggle('active');
            
            // Close other accordion items (single open mode)
            const allAccordionItems = document.querySelectorAll('.accordion-item');
            allAccordionItems.forEach(item => {
                if (item !== accordionItem && item.classList.contains('active')) {
                    item.classList.remove('active');
                }
            });
        });
    });

    // Set item-index custom property for staggered animation
    const navItems = document.querySelectorAll('.nav-menu li');
    navItems.forEach((item, index) => {
        item.style.setProperty('--item-index', index);
    });

    // Highlight active section in navigation - Fixed to only target anchor links
    function highlightNavOnScroll() {
        const scrollY = window.pageYOffset;
        const sections = document.querySelectorAll('section[id]');
        
        // Only select navigation links that point to sections on current page (starting with #)
        const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');
        
        sections.forEach(section => {
            const sectionHeight = section.offsetHeight;
            const sectionTop = section.offsetTop - 100;
            const sectionId = section.getAttribute('id');
            
            if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if(link.getAttribute('href') === '#' + sectionId) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', highlightNavOnScroll);
});
