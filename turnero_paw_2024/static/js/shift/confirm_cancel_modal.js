document.addEventListener('DOMContentLoaded', function() {
    const descriptionTextarea = document.getElementById('cancel-description');
    const charCountElement = document.getElementById('char-count');

    descriptionTextarea.addEventListener('input', function(event) {
        console.log("actualizar text area")
        const maxLength = 200;
        const textLength = descriptionTextarea.value.length; 
        const remainingChars = maxLength - textLength;

        if (textLength >= maxLength) {
            descriptionTextarea.value = descriptionTextarea.value.slice(0, maxLength);
        }
        
        charCountElement.innerHTML = `<strong>${remainingChars}</strong> caracteres restantes`;
    });
});