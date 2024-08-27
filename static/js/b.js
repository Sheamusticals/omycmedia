document.addEventListener("DOMContentLoaded", function() {
    var menuButton = document.getElementById('menu-button');
    var menuIcon = document.getElementById('menu-icon');
    var closeIcon = document.getElementById('close-icon');
    var menu = document.getElementById('menu');

    menuButton.addEventListener('click', function() {
        // Toggle the menu's visibility
        if (menu.classList.contains('hidden')) {
            menu.classList.remove('hidden');
            menuIcon.classList.add('hidden');
            closeIcon.classList.remove('hidden');
        } else {
            menu.classList.add('hidden');
            closeIcon.classList.add('hidden');
            menuIcon.classList.remove('hidden');
        }
    });
});