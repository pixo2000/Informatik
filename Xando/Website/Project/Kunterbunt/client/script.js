document.addEventListener('DOMContentLoaded', function() {
    // Show copyright popup on first visit
    const showCopyrightPopup = function() {
        if (!localStorage.getItem('copyrightPopupShown')) {
            const popup = document.getElementById('copyright-popup');
            popup.classList.add('active');
            
            // Close popup when clicking X button
            const closeBtn = document.querySelector('.close-popup');
            closeBtn.addEventListener('click', function() {
                popup.classList.remove('active');
                localStorage.setItem('copyrightPopupShown', 'true');
            });
            
            // Close popup when clicking "Verstanden" button
            const acceptBtn = document.getElementById('accept-btn');
            acceptBtn.addEventListener('click', function() {
                popup.classList.remove('active');
                localStorage.setItem('copyrightPopupShown', 'true');
            });
        }
    };
    
    // Show popup when page loads
    showCopyrightPopup();
    
    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    menuToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });

    // Close menu when a nav link is clicked
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
        });
    });

    // Login button is now active and will navigate to login.html
    // The preventDefault and alert have been removed
});
