document.addEventListener('DOMContentLoaded', function() {
    const footerCardsContainer = document.getElementById('footer-cards-container');

    const rect = footerCardsContainer.getBoundingClientRect();
    const posicionY = rect.top + window.scrollY;
    console.log('La posición Y del elemento es:', posicionY);

    if (posicionY < 400){
        footerCardsContainer.style.marginTop = "23rem";
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

            // Calcular la altura restante de la pantalla
            // const windowHeight = window.innerHeight;
            // const mainHeight = document.querySelector('main').offsetHeight;
            // const footerHeight = footerCardsContainer.offsetHeight;
            // const remainingHeight = windowHeight - mainHeight;

            // Ajustar la altura del footer para llenar el espacio restante
            // if (remainingHeight > footerHeight) {
            //     footerCardsContainer.style.height = remainingHeight + 'px';
            // }
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
