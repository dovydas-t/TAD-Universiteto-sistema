// list-dropdown.js
document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const button = dropdown.querySelector('.dropbtn');
        const content = dropdown.querySelector('.dropdown-content');
        
        // Show on mouse enter
        dropdown.addEventListener('mouseenter', function() {
            this.classList.add('active');
        });
        
        // Hide on mouse leave
        dropdown.addEventListener('mouseleave', function() {
            this.classList.remove('active');
        });
    });
});