document.addEventListener('DOMContentLoaded', () => {

    // ნავბარისთვის ეფექტი
    const header = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
            header.style.padding = '0.8rem 0';
        } else {
            header.style.boxShadow = 'none';
            header.style.padding = '1.2rem 0';
        }
    });

    // 2. კონფირმაცია წაშლისთვის
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const confirmAction = confirm("Are you sure you want to remove this listing?");
            if (!confirmAction) {
                e.preventDefault();
            }
        });
    });

// 3. ძიების ფილტრი
    const searchInput = document.getElementById('jobSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', () => {
            const filter = searchInput.value.toLowerCase();
            const cards = document.querySelectorAll('.job-card');

            cards.forEach(card => {
                const titleElement = card.querySelector('h2');
                const titleText = titleElement ? titleElement.innerText.toLowerCase() : "";

                if (titleText.includes(filter)) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    }

// flash-ის ავტომატურად გასაქრობად
const alerts = document.querySelectorAll('.alert');
alerts.forEach(alert => {
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    }, 5000);
});