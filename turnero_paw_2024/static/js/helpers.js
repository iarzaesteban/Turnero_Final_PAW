export function getMonthName(indice) {
    const meses = ["Enero", "Febrero", "Marzo", 
                    "Abril", "Mayo", "Junio", 
                    "Julio", "Agosto", "Septiembre", "Octubre", 
                    "Noviembre", "Diciembre"];

    return meses[indice];
}

export function setCurrentDay(currentYear, currentMonth, currentDay){
    const currentDateDay = document.getElementById('current-date-day');
    const currentDateDate = document.getElementById('current-date-date');
    const selectedDate = new Date(currentYear, currentMonth, currentDay);
    const dayOfWeek = selectedDate.toLocaleDateString
                                        ('es-ES', { weekday: 'long' }).
                                            replace(/^\w/, (c) => c.toUpperCase());

    currentDateDay.textContent = `${currentDay}  ${dayOfWeek}`;
    currentDateDate.textContent = getMonthName(currentMonth) + ` de ${currentYear}`;
}

export function getClassDay(dia, thisMonth) {
    if (thisMonth === currentMonth) {
        if (dia < currentDay) {
            return "anterior";
        } else if (dia === currentDay) {
            return "actual";
        } else {
            return "posterior";
        }
    } else {
        return "posterior";
    }
}