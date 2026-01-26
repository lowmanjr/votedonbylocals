// This function runs when the page content is fully loaded.
document.addEventListener('DOMContentLoaded', function() {
    
    /**
     * --- Reusable Components (Header & Footer) ---
     * Fetches HTML from component files and injects it into the correct place.
     */
    const loadComponent = (elementId, filePath) => {
        const element = document.getElementById(elementId);
        if (element) {
            fetch(filePath)
                .then(response => response.text())
                .then(data => {
                    element.innerHTML = data;
                    // After the header is loaded, initialize the mobile menu functionality
                    if (elementId === 'main-header') {
                        initMobileMenu();
                    }
                })
                .catch(error => console.error(`Error loading component from ${filePath}:`, error));
        }
    };

    /**
     * --- Mobile Menu Toggle ---
     * This new function handles the hamburger menu logic.
     */
    const initMobileMenu = () => {
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');

        if (mobileMenuButton && mobileMenu) {
            mobileMenuButton.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
            });
        }
    };

    // Load the header and footer on every page
    loadComponent('main-header', '/components/header.html');
    loadComponent('main-footer', '/components/footer.html');

    console.log("Voted On By Locals site initialized!");
});