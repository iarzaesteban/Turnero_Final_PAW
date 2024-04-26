document.addEventListener('DOMContentLoaded', function() {
    //Modal de borrar y editar.
    const modal = document.getElementById('confirmation-modal');
    const editModal = document.getElementById('edit-modal');
    //Botones Confirmar y Cancelar del modal de borrar registro. 
    const confirmButton = document.getElementById('confirm-button');
    const cancelButton = document.getElementById('cancel-button');
    //Botones del form para borrar o editar
    const deleteButtons = document.querySelectorAll('.btn-delete');
    const editButtons = document.querySelectorAll('.btn-edit');
    
    //Botones de Editar y Cancelar edición de registro
    const editCancelButton = document.getElementById('edit-cancel-button');
    const editSaveButton = document.getElementById('edit-save-button');
    //Atributos a editar
    const editTitleInput = document.getElementById('edit-title');
    const editDescriptionInput = document.getElementById('edit-description');
    const editLinkInput = document.getElementById('edit-link');

    //Manejo del icono
    const editIconInput = document.getElementById('edit-icon');
    const editIconPreview = document.getElementById('edit-icon-preview');

    editIconInput.addEventListener('change', function() {
        const file = this.files[0];
        const reader = new FileReader();
    
        reader.onload = function(event) {
            const base64Icon = event.target.result;
            editIconPreview.src = base64Icon;
        };
    
        reader.readAsDataURL(file);
    });

    // token para el metodo POST
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    function showModal(id) {
        
        modal.classList.add('show');
        confirmButton.addEventListener('click', function() {
            closeModal();
            fetch(`/aditionals/delete-aditional-information/${id}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    console.error('Error al eliminar el elemento');
                }
            })
            .catch(error => {
                console.error('Error al eliminar el elemento:', error);
            });
        });
    }

    function showEditModal(id, title, description, icon, link) {
        editTitleInput.value = title;
        editDescriptionInput.value = description;
        editLinkInput.value = link ;
        if (icon) {
            editIconPreview.src = icon;
        } else {
            editIconPreview.src = "assets/not-image.png";
        }
        editModal.classList.add('show');
        editSaveButton.addEventListener('click', function() {
            closeModal();
            
            const iconFile = editIconInput.files[0];
            const reader = new FileReader();
        
            reader.onload = function(event) {
                const base64Icon = event.target.result;
        
                fetch(`/aditionals/update-aditional-information/${id}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        title: editTitleInput.value,
                        description: editDescriptionInput.value,
                        link: editLinkInput.value,
                        icon_base64: base64Icon
                    })
                })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        console.error('Error al editar el elemento');
                    }
                })
                .catch(error => {
                    console.error('Error al editar el elemento:', error);
                });
            };
        
            if (iconFile) {
                reader.readAsDataURL(iconFile);
            } else {
                reader.readAsDataURL(new Blob());
            }
        });
    }

    function closeModal() {
        modal.classList.remove('show');
        editModal.classList.remove('show');
    }

    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const id = button.dataset.id;
            showModal(id);
        });
    });

    editButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const section = button.closest('.updates-footer-container__information');
            const id = section.dataset.id;
            const title = section.dataset.title;
            const description = section.dataset.description;
            const icon = section.dataset.icon;
            const link = section.dataset.link !== 'None' ? section.dataset.link : "No hay link disponible";
            showEditModal(id, title, description, icon, link);
        });
    });

    if (cancelButton) {
        cancelButton.addEventListener('click', function() {
            closeModal();
        });
    }

    if (editCancelButton) {
        editCancelButton.addEventListener('click', function() {
            closeModal();
        });
    }
});
