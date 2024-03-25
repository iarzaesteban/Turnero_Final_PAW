document.addEventListener('DOMContentLoaded', function() {
    _toggle.onclick = () => {
        _items.classList.toggle("open");
        _toggle.classList.toggle("close");
    }

    document.getElementById('header-avatar-btn').addEventListener('click', function() {
        this.classList.toggle('active');
    });

    const userAvatar = document.getElementById('user-avatar');
    
    const userAvatarUrl = '/get-user-avatar-url';

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
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});