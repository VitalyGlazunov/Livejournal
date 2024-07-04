
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


function generateUrl(amount, description) {
  const data = {
    "currency": "RUB",
    "amount": amount,
    "order_desc": description,
    "order_id": '{{ uuid.uuid1() }}',
    "merchant_data": '{{ username }}'
  };

  fetch('/generate_checkout_url/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': '{{ csrf_token }}'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    if (data.checkout_url) {
      window.location.href = data.checkout_url;
    } else {
      alert('Ошибка при генерации URL');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}
