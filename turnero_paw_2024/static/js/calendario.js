let date = new Date();

const thisYear = date.getFullYear();
const thisMonth = date.getMonth();
const thisDay = date.getDate();

let mesActual = date.getMonth();
let anioActual = date.getFullYear();
let diaActual = date.getDate();

let firstDayMonth = new Date(anioActual, mesActual, 1);
let lastDayMonth = new Date(anioActual, mesActual + 1, 0);

let daysWeek = lastDayMonth.getDate();

let firstDayWeek = firstDayMonth.getDay();

let cuerpoCalendario = document.getElementById("calendario-cuerpo");

function generarCalendario() {
    let dia = 1;
    for (let i = 0; i < 6; i++) { 
        const fila = cuerpoCalendario.insertRow();
    
        for (let j = 0; j < 7; j++) {
            const cell = fila.insertCell();
    
            if (i === 0 && j < firstDayWeek) {
                cell.textContent = "";
            } else if (dia > daysWeek) {
                cell.textContent = "";
            } else {
                cell.textContent = dia;
                
                if (thisMonth == mesActual){
                    if (dia < diaActual) {
                        cell.classList.add("anterior");
                    } else if (dia === diaActual) {
                        cell.classList.add("actual");
                    } else {
                        cell.classList.add("posterior");
                    }
                }else{
                    cell.classList.add("posterior");
                }
                    
    
                if (dia < diaActual) {
                    cell.removeEventListener("click", null);
                } else {
                    cell.addEventListener("click", () => {
                        // Manejar clic en el día (puedes agregar tu lógica aquí)
                        alert(`Día seleccionado: ${dia}`);
                    });
                }
    
                dia++;
            }
        }
    }
}

function updateAtributesDate(){
    if(mesActual == thisMonth){
        diaActual = date.getDate();
    }
   
    firstDayMonth = new Date(anioActual, mesActual, 1);
    lastDayMonth = new Date(anioActual, mesActual + 1, 0);
    daysWeek = lastDayMonth.getDate();
    firstDayWeek = firstDayMonth.getDay();
}

function cambiarMes(value) {
    console.log("value es ",value);
    let changeMonth = mesActual + value
    console.log("changeMonth es ",changeMonth);

    if (changeMonth < 0 && changeMonth < thisMonth) {
        mesActual = 11;
        anioActual--;
    } else if (changeMonth > 11 ) {
        mesActual = 0;
        anioActual++;
    }else if (changeMonth < thisMonth){
        mesActual = thisMonth;
    }else{
        mesActual = changeMonth;
    }
    console.log("mesActual es ",mesActual);
    cuerpoCalendario.innerHTML = "";
    updateAtributesDate();

    generarCalendario();
    selectMes.selectedIndex = mesActual;
    selectAnio.selectedIndex = 0;
}


function actualizarSelectores() {
    const selectMes = document.getElementById("selectMes");
    const selectAnio = document.getElementById("selectAnio");

    // Limpiar los selectores
    selectMes.innerHTML = "";
    selectAnio.innerHTML = "";
    const option = document.createElement("option");
    option.value = 0;
    selectMes.add(option);
    // Generar options para el selector de mes
    for (let i = mesActual; i < mesActual + 3; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.text = obtenerNombreMes(i);
        selectMes.add(option);
    }

    // Establecer el mes actual como seleccionado
    selectMes.selectedIndex = mesActual;
    const yearOption = document.createElement("option");
    yearOption.value = 0;
    yearOption.text = anioActual;
    selectAnio.add(yearOption);
    if (mesActual > 9) {
        const yearOption = document.createElement("option");
        yearOption.value = 1;
        yearOption.text = anioActual + 1;
        selectAnio.add(yearOption);
    }

    // Establecer el año actual como seleccionado
    selectAnio.selectedIndex = 0;
}

function obtenerNombreMes(indice) {
    const meses = ["Enero", "Febrero", "Marzo", 
                    "Abril", "Mayo", "Junio", 
                    "Julio", "Agosto", "Septiembre", "Octubre", 
                    "Noviembre", "Diciembre"];

    return meses[indice];
}


// Llamada a la función de inicialización del calendario
generarCalendario();
// Llamada a la función para actualizar los selectores
actualizarSelectores();