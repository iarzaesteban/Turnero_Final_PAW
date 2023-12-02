function cargarLocalidades() {
    var provinciaSeleccionada = $("#id_provincia").val();
    $.ajax({
        url: "api/obtener_localidades.php",
        type: "POST",
        data: { provincia: provinciaSeleccionada },
        success: function (response) {
            $("#localidad").html(response);
        }
    });
}

function cargarProvincias() {
    $.ajax({
        url: "api/obtener_provincias.php",
        type: "GET",
        success: function (response) {
            $("#provincia").html(response);
        }
    });
}
