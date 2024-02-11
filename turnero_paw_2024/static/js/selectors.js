import {
    thisMonth,
    currentYear,
    currentMonth,
    monthSelected,
    yearSelected,
} from './index.js';

import {
    getMonthName
} from './helpers.js';

function cleanSelectors(){
    monthSelected.innerHTML = "";
    yearSelected.innerHTML = "";
}

export function updateSelectors() {
    cleanSelectors();
    const option = document.createElement("option");
    option.value = 0;
    monthSelected.add(option);
    for (let i = thisMonth; i < thisMonth + 3; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.text = getMonthName(i);
        monthSelected.add(option);
    }
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
    
    yearSelected.selectedIndex = 0;
}