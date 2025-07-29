// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {
    // Mostrar/ocultar secciones de usuarios y empleados
    document.getElementById('btn-usuarios').addEventListener('click', function () {
        document.getElementById('seccion-usuarios').style.display = 'block'
        document.getElementById('seccion-empleados').style.display = 'none'
        document.getElementById('btn-usuarios').classList.add('activo')
        document.getElementById('btn-empleados').classList.remove('activo')
    })

    document.getElementById('btn-empleados').addEventListener('click', function () {
        document.getElementById('seccion-usuarios').style.display = 'none'
        document.getElementById('seccion-empleados').style.display = 'block'
        document.getElementById('btn-empleados').classList.add('activo')
        document.getElementById('btn-usuarios').classList.remove('activo')
    })

    // Mostrar formulario de edición
    function mostrarFormularioEdicion(id) {
        // Obtener los datos del usuario desde la tabla
        var fila = document.querySelector(`button[onclick="mostrarFormularioEdicion('${id}')"]`).closest('tr')
        var nombre = fila.cells[0].textContent
        var apellido = fila.cells[1].textContent
        var correo = fila.cells[2].textContent

        // Llenar los campos del formulario
        document.getElementById('editar-id').value = id
        document.getElementById('editar-nombre').value = nombre
        document.getElementById('editar-apellido').value = apellido
        document.getElementById('editar-correo').value = correo

        // Mostrar el formulario
        document.getElementById('formulario-edicion').style.display = 'block'

    }
    // Exponer la función al alcance global
    window.mostrarFormularioEdicion = mostrarFormularioEdicion;

    // Ocultar formulario de edición
    function ocultarFormularioEdicion() {
        document.getElementById('formulario-edicion').style.display = 'none'
    }
    // Exponer la función al alcance global
    window.ocultarFormularioEdicion = ocultarFormularioEdicion;


    // Mostrar formulario de añadir usuario
    function mostrarFormularioAñadirUsuario() {
        document.getElementById('formulario-añadir-usuario').style.display = 'block';
    }
    // Exponer la función al alcance global
    window.mostrarFormularioAñadirUsuario = mostrarFormularioAñadirUsuario;

    // Ocultar formulario de añadir usuario
    function ocultarFormularioAñadirUsuario() {
        document.getElementById('formulario-añadir-usuario').style.display = 'none';
    }
    // Exponer la función al alcance global
    window.ocultarFormularioAñadirUsuario = ocultarFormularioAñadirUsuario;
});