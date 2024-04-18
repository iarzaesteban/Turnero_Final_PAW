document.addEventListener('DOMContentLoaded', function() {
    const footerCardsContainer = document.getElementById('footer-cards-container');
    
    fetch('/aditionals/aditional-information/')
        .then(response => response.json())
        .then(data => {
            
            data.forEach(info => {
                const card = document.createElement('section');
                card.classList.add('footer-card');

                const icon = document.createElement('img');
                icon.classList.add('footer-card-icon');
                icon.src = info.icon;

                const content = document.createElement('span');
                content.classList.add('footer-card-content');
                const title = document.createElement('h3');
                title.textContent = info.title;
                const description = document.createElement('p');
                description.textContent = info.description;

                content.appendChild(title);
                content.appendChild(description);

                card.appendChild(icon);
                card.appendChild(content);

                footerCardsContainer.appendChild(card);
            });

            const footerContainer = document.querySelector('footer');

            const footerRect = footerCardsContainer.getBoundingClientRect();
            const windowHeight = window.innerHeight;

            const spaceBelowFooter = windowHeight - footerRect.bottom;
            if(spaceBelowFooter > 0){
                footerCardsContainer.style.position = "absolute";
                footerCardsContainer.style.bottom = "0";
            }
            
        })
        .catch(error => console.error('Error fetching additional information:', error));
});



// document.addEventListener('DOMContentLoaded', function() {
//     fetch('/aditionals/aditional-information/')
//         .then(response => response.json())
//         .then(data => {
//             const footerCardsContainer = document.getElementById('footer-cards-container');
//             data.forEach(info => {
//                 const card = document.createElement('section');
//                 card.classList.add('footer-card');

//                 const icon = document.createElement('img');
//                 icon.classList.add('footer-card-icon');
//                 icon.src = info.icon;

//                 const content = document.createElement('span');
//                 content.classList.add('footer-card-content');
//                 const title = document.createElement('h3');
//                 title.textContent = info.title;
//                 const description = document.createElement('p');
//                 description.textContent = info.description;

//                 content.appendChild(title);
//                 content.appendChild(description);

//                 card.appendChild(icon);
//                 card.appendChild(content);

//                 footerCardsContainer.appendChild(card);
//             });
//         })
//         .catch(error => console.error('Error fetching additional information:', error));
// });
