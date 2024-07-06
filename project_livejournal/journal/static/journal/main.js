document.addEventListener('DOMContentLoaded', function() {
    const submenuLinks = document.querySelectorAll('.submenu a');
    const rubrikaLink = document.getElementById('rubrikaLink');

    const currentUrl = window.location.href;
    submenuLinks.forEach(link => {
        if (currentUrl === link.href) {
            rubrikaLink.classList.add('active');
        }
    });

    submenuLinks.forEach(link => {
        link.addEventListener('click', function() {
            rubrikaLink.classList.add('active');
        });
    });

    const navLinks = document.querySelectorAll('.navbar-nav a');
    navLinks.forEach(link => {
        if (!link.classList.contains('submenu')) {
            link.addEventListener('click', function() {
                rubrikaLink.classList.remove('active');
            });
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll(".button-user button");

    function deactivateButtons() {
        buttons.forEach(button => {
            button.classList.remove("active");
        });
    }

    buttons.forEach(button => {
        button.addEventListener("click", function() {
            deactivateButtons();
            this.classList.add("active");
        });
    });

    const currentUrl = window.location.href;
    buttons.forEach(button => {
        const buttonLink = button.closest("a").getAttribute("href");
        if (currentUrl.includes(buttonLink)) {
            deactivateButtons();
            button.classList.add("active");
        }
    });
});

