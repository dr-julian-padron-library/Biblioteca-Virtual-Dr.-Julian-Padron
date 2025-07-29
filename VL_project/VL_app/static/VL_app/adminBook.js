// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {
    // Mostrar formulario de agregar libro
    document.getElementById('btn-agregar-libro').addEventListener('click', function () {
        document.getElementById('formulario-agregar').style.display = 'block';
    });

    // Ocultar formulario de agregar libro
    function ocultarFormularioAgregar() {
        document.getElementById('formulario-agregar').style.display = 'none';
    }

    // Mostrar formulario de edición
    function mostrarFormularioEdicion(id) {
        const formularioEdicion = document.getElementById('formulario-edicion')
        const formEditarLibro = document.getElementById('form-editar-libro')

        // Actualizar la URL del formulario con el ID del libro
        formEditarLibro.action = `/editBook/${id}/`

        // Obtener los datos del libro mediante una solicitud AJAX
        fetch(`/getBook/${id}/`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Error al obtener los datos del libro')
                }
                return response.json()
            })
            .then((data) => {
                // Llenar los campos del formulario con los datos del libro
                document.getElementById('editar-id').value = data.id
                document.getElementById('editar-titulo').value = data.titulo
                document.getElementById('editar-sinopsis').value = data.sinopsis
                document.getElementById('editar-paginas').value = data.paginas
                document.getElementById('editar-autor').value = data.autor
                document.getElementById('editar-editorial').value = data.editorial
                document.getElementById('editar-tipo').value = data.tipo
                document.getElementById('editar-isbn').value = data.isbn
                document.getElementById('editar-año-publicacion').value = data.anno_publicacion
                document.getElementById('editar-disponibilidad').checked = data.disponibilidad

                // Mostrar el formulario de edición
                formularioEdicion.style.display = 'block'
            })
            .catch((error) => {
                console.error('Error al obtener los datos del libro:', error)
                alert('Error al cargar los datos del libro. Inténtalo de nuevo.')
            })
    }
    // Exponer la función al alcance global
    window.mostrarFormularioEdicion = mostrarFormularioEdicion;

    // Ocultar formulario de edición
    function ocultarFormularioEdicion() {
        document.getElementById('formulario-edicion').style.display = 'none';
    }

    // Asignar la función ocultarFormularioAgregar al botón de cancelar
    const botonCancelarAgregar = document.querySelector('#formulario-agregar button[type="button"]');
    if (botonCancelarAgregar) {
        botonCancelarAgregar.addEventListener('click', ocultarFormularioAgregar);
    }

    // Asignar la función ocultarFormularioEdicion al botón de cancelar
    const botonCancelarEdicion = document.querySelector('#formulario-edicion button[type="button"]');
    if (botonCancelarEdicion) {
        botonCancelarEdicion.addEventListener('click', ocultarFormularioEdicion);
    }
});