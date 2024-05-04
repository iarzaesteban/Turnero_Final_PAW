document.addEventListener('DOMContentLoaded', function() {
    const footerCardsContainer = document.getElementById('footer-cards-container');
    

    function getWindowWidth() {
        return window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    }

    fetch('/aditionals/aditional-information/')
        .then(response => response.json())
        .then(data => {
            
            data.forEach(info => {
                const card = document.createElement('section');
                card.classList.add('footer-card');

                const icon = document.createElement('img');
                icon.classList.add('footer-card-icon');
                icon.src = info.icon;
                icon.alt = info.title

                const content = document.createElement('span');
                content.classList.add('footer-card-content');
                const title = document.createElement('h3');
                title.textContent = info.title;
                const description = document.createElement('p');
                description.textContent = info.description;
                description.style.fontWeight = "bold";
                const link = document.createElement('a');
                link.href = info.link;
                link.textContent = info.link;

                content.appendChild(title);
                content.appendChild(description);

                card.appendChild(icon);
                card.appendChild(content);
                card.appendChild(link);

                footerCardsContainer.appendChild(card);
            });

            const footerRect = footerCardsContainer.getBoundingClientRect();
            const windowHeight = window.innerHeight;

            const spaceBelowFooter = windowHeight - footerRect.bottom;
            const windowWidth = getWindowWidth();

            if(spaceBelowFooter >= 0){
                footerCardsContainer.style.position = "relative";
                if (windowWidth <= 768 ) {
                    footerCardsContainer.style.top = "15rem";
                }else{
                    footerCardsContainer.style.top = "25rem";
                }
                
            }
        })
        .catch(error => {
            const card = document.createElement('section');
            card.classList.add('footer-card');
            footerCardsContainer.appendChild(card);
        });
});
