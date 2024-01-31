function cargarProvincias() {
    $.ajax({
        url: "api/obtener_provincias.php",
        type: "GET",
        success: function (response) {
            $("#provincia").html(response);
        }
    });
}

function cargarLocalidades() {
    var provinciaSeleccionada = $("#provincia").val();
    $.ajax({
        url: "api/obtener_localidades.php",
        type: "POST",
        data: { provincia: provinciaSeleccionada },
        success: function (response) {
            $("#localidad").html(response);
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    cargarProvincias();
    cargarLocalidades();
    document.getElementById("provincia").addEventListener("change", function () {
        document.getElementById("id_provincia").value = this.value;
        cargarLocalidades();
    });
});