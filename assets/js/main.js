// This function runs when the page content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    /**
     * --- Reusable Components (Header & Footer) ---
     * This is a modern way to avoid copying and pasting your header and footer HTML on every page.
     * It fetches the HTML from the component files and injects it into the correct place.
     * @param {string} elementId - The ID of the element to load the component into.
     * @param {string} filePath - The path to the HTML component file.
     */
    const loadComponent = (elementId, filePath) => {
        const element = document.getElementById(elementId);
        if (element) {
            fetch(filePath)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.text();
                })
                .then(data => {
                    element.innerHTML = data;
                })
                .catch(error => console.error(`Error loading component from ${filePath}:`, error));
        }
    };

    // Load the header and footer into their respective placeholder divs
    loadComponent('main-header', '/components/header.html');
    loadComponent('main-footer', '/components/footer.html');

    // --- You can add other site-wide logic here ---
    // For example, logic for a mobile navigation menu, analytics, etc.
    console.log("By Locals.. site initialized!");

});