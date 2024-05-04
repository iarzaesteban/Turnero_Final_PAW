document.addEventListener("DOMContentLoaded", function() {
    const formContainer = document.getElementById('form-updates-footer');
    
    document.getElementById("icon").addEventListener("change", function() {
        const file = this.files[0];
        const reader = new FileReader();
        
        reader.onload = function(event) {
            const base64Icon = event.target.result;
            document.getElementById("hidden-icon").value = base64Icon;
        };
        
        reader.readAsDataURL(file);
    });

    document.getElementById("form-updates-footer").addEventListener("submit", function(event) {
        event.preventDefault();
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const title = document.getElementById("id_title").value;
        const description = document.getElementById("id_description").value;
        const link = document.getElementById("id_link").value;
        const icon = document.getElementById("hidden-icon").value;
        const formData = new FormData();
        formData.append("csrfmiddlewaretoken", csrfToken);
        formData.append("title", title);
        formData.append("description", description);
        formData.append("link", link);
        formData.append("icon_base64", icon);
        fetch('/update-footer/', {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (response.ok) {
                const message = "Se ha creado una nueva card para el footer";
                const messageCreateAditionalInfo = document.createElement('p');
                messageCreateAditionalInfo.textContent = message;
                const firstChild = formContainer.firstChild;
                formContainer.insertBefore(messageCreateAditionalInfo, firstChild);
                setTimeout(() => window.location.reload(), 5000);
            } else {
                const message = "Error al procesar el formulario";
                const messageCreateAditionalInfo = document.createElement('p');
                messageCreateAditionalInfo.textContent = message;
                const firstChild = formContainer.firstChild;
                formContainer.insertBefore(messageCreateAditionalInfo, firstChild);
                throw new Error('Error al procesar el formulario');
            }
        })
        .catch(error => {
            setTimeout(() => window.location.reload(), 5000);
        });
    });

});
