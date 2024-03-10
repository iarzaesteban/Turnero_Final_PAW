document.addEventListener('DOMContentLoaded', function() {
    console.log("llegando")
    // const menuToggle = document.getElementById('button-menu-toggle-hidde');
    // menuToggle.style.display = 'block';
    // menuToggle.classList.add("button-menu-toggle-show");
    // const menu = document.getElementById('menu');

    // menuToggle.addEventListener('click', function() {
    //     // menu.classList.toggle('show-menu');
    //     menu.classList.add("show-menu");
    // });
    _toggle.onclick = () => {
        console.log("click")
        _items.classList.toggle("open");
        _toggle.classList.toggle("close");
    }
});