document.addEventListener('DOMContentLoaded', function() {
    const descriptionTextarea = document.getElementById('cancel-description');
    const charCountElement = document.getElementById('char-count');
    const maxLength = 200;
    if (descriptionTextarea){
        descriptionTextarea.addEventListener('input', function(event) {
            const textLength = descriptionTextarea.value.length; 
            const remainingChars = maxLength - textLength;
            if (textLength >= maxLength) {
                descriptionTextarea.value = descriptionTextarea.value.slice(0, maxLength);
            }
            charCountElement.innerHTML = `<strong>${remainingChars}</strong> caracteres restantes`;
        });
    }
});