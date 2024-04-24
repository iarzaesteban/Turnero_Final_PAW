document.addEventListener('DOMContentLoaded', function() {
    const getShiftsBtns = document.querySelectorAll('.get-shifts-btn');

    getShiftsBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            window.location.href = url;
        });
    });
});