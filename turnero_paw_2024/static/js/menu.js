document.addEventListener('DOMContentLoaded', function() {
    _toggle.onclick = () => {
        console.log("click")
        _items.classList.toggle("open");
        _toggle.classList.toggle("close");
    }
});