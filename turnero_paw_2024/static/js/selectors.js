import {
    getMonthName
} from './helpers.js';

export function cleanSelectors(monthSelected, yearSelected){
    monthSelected.innerHTML = "";
    yearSelected.innerHTML = "";
}

export function updateSelectors(monthSelected, yearSelected, thisMonth, currentYear) {
    // Limpiamos los selectores
    cleanSelectors(monthSelected, yearSelected);
    const option = document.createElement("option");
    option.value = 0;
    monthSelected.add(option);
    // Generamos options para el selector de mes
    for (let i = thisMonth; i < thisMonth + 3; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.text = getMonthName(i);
        monthSelected.add(option);
    }
    // Establecemos el mes actual como seleccionado
    monthSelected.selectedIndex = currentMonth;

    const yearOption = document.createElement("option");
    yearOption.value = 0;
    yearOption.text = currentYear;
    yearSelected.add(yearOption);
    if (thisMonth > 9) {
        const yearOption = document.createElement("option");
        yearOption.value = 1;
        yearOption.text = currentYear + 1;
        yearSelected.add(yearOption);
    }

    // Establecemos el año actual como seleccionado
    yearSelected.selectedIndex = 0;
}