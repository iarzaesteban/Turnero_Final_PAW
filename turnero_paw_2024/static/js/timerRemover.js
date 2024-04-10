document.addEventListener('DOMContentLoaded', function() {
    const messagesSection = document.getElementById('messages');
    
    if (messagesSection) {
        const messages = messagesSection.querySelectorAll('.message');
        
        messages.forEach(function(message) {
            setTimeout(function() {
                message.remove();
            }, 5000);
        });
    }
});