document.addEventListener('DOMContentLoaded', function() {
    const buttonsOutsideMenu = document.querySelectorAll('button:not(#header-avatar-btn)');
    const linksOutsideMenu = document.querySelectorAll('a.acept-btn, a.cancel-btn');
    
    const headerAvatarBtn = document.getElementById('header-avatar-btn');
    const navItemsUser = document.querySelector('.nav-items-user');

    document.addEventListener('click', function(event) {
        if (headerAvatarBtn){
            if (event.target !== headerAvatarBtn && event.target !== _toggle && 
                !headerAvatarBtn.contains(event.target) && !_toggle.contains(event.target)) {
                closeMenus();
                enableButtonsAndLinks();
            }
        }else{
            if (event.target !== _toggle && 
                !_toggle.contains(event.target)) {
                closeMenus();
                enableButtonsAndLinks();
            }
        }
    });
    
    _toggle.onclick = () => {
        _items.classList.toggle("open");
        _toggle.classList.toggle("close");
        disableButtonsAndLinks();
        if (headerAvatarBtn && navItemsUser){
            headerAvatarBtn.classList.remove('active');
            navItemsUser.classList.remove('active');
        }
    }    

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
                userAvatar.alt = "image avatar";
                if  (currentUserAvatar){
                    currentUserAvatar.src = imageUrl;
                }
            }
        })
        .catch(error => {
            userAvatar.alt = "image avatar";
        });
    }
    
});
