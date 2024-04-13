document.addEventListener('DOMContentLoaded', function() {
    const buttonsOutsideMenu = document.querySelectorAll('button:not(#header-avatar-btn)');
    const linksOutsideMenu = document.querySelectorAll('a.acept-btn, a.cancel-btn');
    document.addEventListener('click', function(event) {
        if (headerAvatarBtn){
            if (event.target !== headerAvatarBtn && event.target !== _toggle && 
                !headerAvatarBtn.contains(event.target) && !_toggle.contains(event.target)) {
                closeMenus();
                enableButtonsAndLinks();
            }
        }
    });
    
    _toggle.onclick = () => {
        _items.classList.toggle("open");
        _toggle.classList.toggle("close");
        disableButtonsAndLinks();
        headerAvatarBtn.classList.remove('active');
        navItemsUser.classList.remove('active');
    }
    
    const headerAvatarBtn = document.getElementById('header-avatar-btn');
    const navItemsUser = document.querySelector('.nav-items-user');

    function closeMenus() {
        _items.classList.remove("open");
        _toggle.classList.remove("close");
        if (headerAvatarBtn) {
            headerAvatarBtn.classList.remove('active');
        }
        if (navItemsUser) {
            navItemsUser.classList.remove('active');
        }
    }
    if (headerAvatarBtn){
        headerAvatarBtn.addEventListener('click', function() {
            this.classList.toggle('active');
            disableButtonsAndLinks();
            _items.classList.remove("open");
            _toggle.classList.remove("close");
        });
    }
    

    const userAvatar = document.getElementById('user-avatar');
    const currentUserAvatar = document.getElementById('current-user-avatar');
    
    const userAvatarUrl = '/get-user-avatar-url';
    
    function disableButtonsAndLinks() {
        buttonsOutsideMenu.forEach(button => {
            button.style.pointerEvents = "none";
        });
        linksOutsideMenu.forEach(link => {
            link.style.pointerEvents = "none";
        });
    }

    function enableButtonsAndLinks() {
        buttonsOutsideMenu.forEach(button => {
            button.style.pointerEvents = "auto";
        });
        linksOutsideMenu.forEach(link => {
            link.style.pointerEvents = "auto";
        });
    }
    
    if(userAvatar){
        fetch(userAvatarUrl)
        .then(response => {
            if (response.ok) {
                return response.blob();
            }
            throw new Error('Error al obtener la imagen del usuario');
        })
        .then(blob => {
            if (blob.type === 'image/jpeg') {
                const imageUrl = URL.createObjectURL(blob);
                userAvatar.src = imageUrl;
                if  (currentUserAvatar){
                    currentUserAvatar.src = imageUrl;
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    
});
