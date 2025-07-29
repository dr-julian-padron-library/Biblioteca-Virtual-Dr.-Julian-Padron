// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {
    // Mostrar formulario de añadir préstamo
    function mostrarFormularioAñadirPrestamo() {
        document.getElementById('formulario-añadir-prestamo').style.display = 'block';
    }
    // Exponer la función al alcance global
    window.mostrarFormularioAñadirPrestamo = mostrarFormularioAñadirPrestamo;

    // Ocultar formulario de añadir préstamo
    function ocultarFormularioAñadirPrestamo() {
        document.getElementById('formulario-añadir-prestamo').style.display = 'none';
    }
    // Exponer la función al alcance global
    window.ocultarFormularioAñadirPrestamo = ocultarFormularioAñadirPrestamo;

    // Mostrar formulario de edición de préstamo
    function mostrarFormularioEdicionPrestamo(id) {
        // Obtener los datos del préstamo desde la tabla
        var fila = document.querySelector(`button[onclick="mostrarFormularioEdicionPrestamo('${id}')"]`).closest('tr');
        var libro = fila.cells[3].textContent;
        var fechaPrestamo = fila.cells[4].textContent;
        var fechaDevolucion = fila.cells[5].textContent;
        var estado = fila.cells[6].textContent;

        // Llenar los campos del formulario
        document.getElementById('editar-id-prestamo').value = id;
        document.getElementById('editar-libro').value = libro;
        document.getElementById('editar-fecha-prestamo').value = fechaPrestamo;
        document.getElementById('editar-fecha-devolucion').value = fechaDevolucion;
        document.getElementById('editar-estado').value = estado;

        // Mostrar el formulario
        document.getElementById('formulario-edicion-prestamo').style.display = 'block';
    }
    // Exponer la función al alcance global
    window.mostrarFormularioEdicionPrestamo = mostrarFormularioEdicionPrestamo;

    // Ocultar formulario de edición de préstamo
    function ocultarFormularioEdicionPrestamo() {
        document.getElementById('formulario-edicion-prestamo').style.display = 'none';
    }
    // Exponer la función al alcance global
    window.ocultarFormularioEdicionPrestamo = ocultarFormularioEdicionPrestamo;

});