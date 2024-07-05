
document.addEventListener('DOMContentLoaded', function() {
    const submenuLinks = document.querySelectorAll('.submenu a');
    const rubrikaLink = document.getElementById('rubrikaLink');

    const currentUrl = window.location.href;
    submenuLinks.forEach(link => {
        if (currentUrl === link.href) {
            rubrikaLink.classList.add('active-rubrika');
        }
    });

    submenuLinks.forEach(link => {
        link.addEventListener('click', function() {
            rubrikaLink.classList.add('active-rubrika');
        });
    });

    const navLinks = document.querySelectorAll('.navbar-nav a');
    navLinks.forEach(link => {
        if (!link.classList.contains('submenu')) {
            link.addEventListener('click', function() {
                rubrikaLink.classList.remove('active-rubrika');
            });
        }
    });
});



