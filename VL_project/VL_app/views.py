from VL_app.models import MaterialBibliografico, PrestamoMaterialBibliografico
from .forms import PerfilForm
from django.shortcuts import redirect, render  # type: ignore
from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash  # type: ignore
from django.contrib.auth.models import User, auth, Group  # type: ignore
from django.contrib.auth.decorators import login_required, user_passes_test  # type: ignore
from django.contrib import messages  # type: ignore
from django.http import HttpResponse, JsonResponse  # type: ignore

# Create your views here.


def es_Bibliotecologo(user):
    return user.groups.filter(name='Bibliotecologo').exists()


def es_Bibliotecario(user):
    return user.groups.filter(name='Bibliotecario').exists()


def es_Empleado(user):
    print("esta verificando")
    if user.groups.filter(name='Bibliotecologo').exists() is not None:
        return user.groups.filter(name='Bibliotecologo').exists()
    elif user.groups.filter(name='Bibliotecario').exists() is not None:
        return user.groups.filter(name='Bibliotecario').exists()

    return None


def es_Usuario(user):
    return user.groups.filter(name='Usuario').exists()


def home(request):

    if es_Bibliotecologo(request.user):
        print("Eres un Bibliotecologo.")

    if es_Bibliotecario(request.user):
        print("Eres un Bibliotecario.")

    if es_Usuario(request.user):
        print("Eres un Usuario.")

    print(request.user)

    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        firstName = request.POST['first--name']
        lastName = request.POST['last--name']

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.info(request, 'El nombre de usuario ya existe')
            return render(request, 'register.html')
        else:
            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=firstName,
                last_name=lastName,
            )
            # Añadir el usuario al grupo "Usuarios"
            try:
                grupo_usuarios = Group.objects.get(name='Usuarios')
                user.groups.add(grupo_usuarios)  # Añadir al grupo
            except Group.DoesNotExist:
                # Si el grupo no existe, puedes manejarlo aquí
                messages.error(request, 'El grupo "Usuarios" no existe')
                return render(request, 'register.html')

            # Redirigir al login
            return redirect('login')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)  # Buscar usuario por email
            user = authenticate(username=user.username,
                                password=password)  # Autenticar con username
            print(user)
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth.login(request, user)
            print('User logged in successfully')
            return redirect('home')
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required
def perfil(request):
    user = request.user

    if request.method == "POST":
        form = PerfilForm(request.POST, instance=user)

        if form.is_valid():
            # Verificar contraseña actual si se quiere cambiar
            current_password = form.cleaned_data.get("current_password")
            new_password = form.cleaned_data.get("new_password")

            if current_password:
                if not user.check_password(current_password):
                    messages.error(request,
                                   "La contraseña actual es incorrecta.")
                    return redirect("perfil")
            form.save()
            # Si cambia la contraseña, actualizar sesión
            if new_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)

            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("perfil")
        else:
            messages.error(request, "Error en la actualización del perfil.")

    else:
        form = PerfilForm(instance=user)

    return render(request, "perfil.html", {"form": form})


def explore(request):
    edu_books = MaterialBibliografico.objects.filter(categoria='Educacion')
    fiction_books = MaterialBibliografico.objects.filter(categoria='Ficcion')
    science_books = MaterialBibliografico.objects.filter(categoria='Ciencia')
    return render(
        request, 'explore.html', {
            'edu_books': edu_books,
            'fiction_books': fiction_books,
            'science_books': science_books
        })


def catalogo(request):
    books = MaterialBibliografico.objects.all()
    return render(request, 'catalogo.html', {'books': books})


@login_required
@user_passes_test(es_Empleado)
def adminUsers(request):
    # Obtener todos los usuarios que pertenecen al grupo "usuario"
    grupo_usuario = Group.objects.get(name='Usuario')
    usuarios = grupo_usuario.user_set.all()

    # Obtener todos los usuarios que pertenecen al grupo "bibliotecario"
    grupo_bibliotecario = Group.objects.get(name='Bibliotecario')
    empleados = grupo_bibliotecario.user_set.all()

    print(usuarios)  # Depuración
    print(empleados)  # Depuración

    return render(request, 'adminUsers.html', {
        'usuarios': usuarios,
        'empleados': empleados,
    })


@login_required
@user_passes_test(es_Empleado)
def addUsers(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        tipo = request.POST.get('tipo')

        # Crear el usuario
        usuario = User.objects.create_user(
            username=correo,  # Usamos el correo como nombre de usuario
            email=correo,
            first_name=nombre,
            last_name=apellido,
            password=
            'password_temporal'  # Puedes generar una contraseña temporal
        )

        # Asignar el grupo correspondiente
        grupo = Group.objects.get(name=tipo)
        usuario.groups.add(grupo)

        messages.success(request, 'Usuario añadido correctamente.')
        return redirect(
            'adminUsers')  # Redirige a la página de administración de usuarios

    return redirect('adminUsers')


@login_required
@user_passes_test(es_Bibliotecologo)
def editBibliotecario(request):
    # Obtener todos los usuarios del grupo "Bibliotecario"
    grupo_bibliotecario = Group.objects.get(name='Bibliotecario')
    empleados = grupo_bibliotecario.user_set.all()

    # Obtener todos los usuarios que pertenecen al grupo "usuario"
    grupo_usuario = Group.objects.get(name='Usuario')
    usuarios = grupo_usuario.user_set.all()

    if request.method == 'POST':
        # Añadir un nuevo usuario al grupo "Bibliotecario"
        if 'añadir' in request.POST:
            username = request.POST.get('username')
            try:
                usuario = User.objects.get(username=username)
                usuario.groups.add(grupo_bibliotecario)
                messages.success(
                    request,
                    f'Usuario {username} añadido al grupo Bibliotecario.')
            except User.DoesNotExist:
                messages.error(request, f'El usuario {username} no existe.')

        # Eliminar un usuario del grupo "Bibliotecario"
        elif 'eliminar' in request.POST:
            user_id = request.POST.get('user_id')
            usuario = User.objects.get(id=user_id)
            usuario.groups.remove(grupo_bibliotecario)
            messages.success(
                request,
                f'Usuario {usuario.username} eliminado del grupo Bibliotecario.'
            )

        # Editar un usuario del grupo "Bibliotecario"
        elif 'editar' in request.POST:
            user_id = request.POST.get('user_id')
            nuevo_username = request.POST.get('nuevo_username')
            usuario = User.objects.get(id=user_id)
            usuario.username = nuevo_username
            usuario.save()
            messages.success(
                request,
                f'Usuario {usuario.username} actualizado correctamente.')

        return redirect('adminUsers')

    return render(request, 'adminUsers.html', {
        'usuarios': usuarios,
        'empleados': empleados,
    })


@login_required
@user_passes_test(es_Empleado)
def editUsuario(request):
    # Obtener todos los usuarios del grupo "Bibliotecario"
    grupo_bibliotecario = Group.objects.get(name='Bibliotecario')
    empleados = grupo_bibliotecario.user_set.all()

    # Obtener todos los usuarios que pertenecen al grupo "usuario"
    grupo_usuario = Group.objects.get(name='Usuario')
    usuarios = grupo_usuario.user_set.all()

    if request.method == 'POST':
        # Añadir un nuevo usuario al grupo "Bibliotecario"
        if 'añadir' in request.POST:
            username = request.POST.get('username')
            try:
                usuario = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, f'El usuario {username} no existe.')

        # Eliminar un usuario del grupo "Bibliotecario"
        elif 'eliminar' in request.POST:
            user_id = request.POST.get('user_id')
            usuario = User.objects.get(id=user_id)

        # Editar un usuario del grupo "Bibliotecario"
        elif 'editar' in request.POST:
            user_id = request.POST.get('user_id')
            nuevo_username = request.POST.get('nuevo_username')
            usuario = User.objects.get(id=user_id)
            usuario.username = nuevo_username
            usuario.save()
            messages.success(
                request,
                f'Usuario {usuario.username} actualizado correctamente.')

        return redirect('adminUsers')

    return render(request, 'adminUsers.html', {
        'usuarios': usuarios,
        'empleados': empleados,
    })


@login_required
@user_passes_test(es_Bibliotecologo)
def editUser(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')

        try:
            usuario = User.objects.get(id=user_id)
            usuario.first_name = nombre
            usuario.last_name = apellido
            usuario.email = correo
            usuario.save()
            messages.success(request, 'Usuario actualizado correctamente.')
        except User.DoesNotExist:
            messages.error(request, 'El usuario no existe.')

    return redirect('/admistrarUsuarios/')


@login_required
@user_passes_test(es_Empleado)
def adminBook(request):
    libros = MaterialBibliografico.objects.all()
    return render(request, 'adminBook.html', {'libros': libros})


@login_required
@user_passes_test(es_Empleado)
def addBook(request):
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            titulo = request.POST.get('titulo')
            sinopsis = request.POST.get('sinopsis')
            paginas = request.POST.get('paginas')
            pdf = request.FILES.get('pdf')
            autor = request.POST.get('autor')
            editorial = request.POST.get('editorial')
            tipo = request.POST.get('tipo')
            isbn = request.POST.get('isbn')
            anno_publicacion = request.POST.get('anno_publicacion')
            disponibilidad = request.POST.get('disponibilidad') == 'on'

            # Validar datos
            if not titulo or not autor or not editorial or not isbn:
                messages.error(
                    request,
                    'Todos los campos obligatorios deben ser llenados.')
                return redirect('adminBook')

            # Crear el libro
            libro = MaterialBibliografico(titulo=titulo,
                                          sinopsis=sinopsis,
                                          paginas=paginas,
                                          pdf=pdf,
                                          autor=autor,
                                          editorial=editorial,
                                          tipo=tipo,
                                          isbn=isbn,
                                          anno_publicacion=anno_publicacion,
                                          disponibilidad=disponibilidad)
            libro.save()

            messages.success(request, 'Libro agregado correctamente.')
            return redirect('adminBook')

        except Exception as e:
            messages.error(request, f'Error al agregar el libro: {str(e)}')
            return redirect('adminBook')

    return render(request, 'adminBook.html')


@login_required
@user_passes_test(es_Empleado)
def editBook(request, id):
    try:
        libro = MaterialBibliografico.objects.get(
            id=id)  # Obtener el libro a editar
        if request.method == 'POST':
            # Obtener datos del formulario
            titulo = request.POST.get('titulo')
            sinopsis = request.POST.get('sinopsis')
            paginas = request.POST.get('paginas')
            pdf = request.FILES.get('pdf')
            autor = request.POST.get('autor')
            editorial = request.POST.get('editorial')
            tipo = request.POST.get('tipo')
            isbn = request.POST.get('isbn')
            anno_publicacion = request.POST.get('anno_publicacion')
            disponibilidad = request.POST.get('disponibilidad') == 'on'

            # Actualizar los campos del libro
            libro.titulo = titulo
            libro.sinopsis = sinopsis
            libro.paginas = paginas
            if pdf:  # Solo actualizar el PDF si se proporciona uno nuevo
                libro.pdf = pdf
            libro.autor = autor
            libro.editorial = editorial
            libro.tipo = tipo
            libro.isbn = isbn
            libro.anno_publicacion = anno_publicacion
            libro.disponibilidad = disponibilidad

            # Guardar los cambios
            libro.save()

            messages.success(request, 'Libro actualizado correctamente.')
            return redirect('adminBook')

        # Si no es POST, devolver los datos del libro para prellenar el formulario
        return JsonResponse({
            'id':
            libro.id,
            'titulo':
            libro.titulo,
            'sinopsis':
            libro.sinopsis,
            'paginas':
            libro.paginas,
            'autor':
            libro.autor,
            'editorial':
            libro.editorial,
            'tipo':
            libro.tipo,
            'isbn':
            libro.isbn,
            'anno_publicacion':
            libro.anno_publicacion.strftime('%Y-%m-%d')
            if libro.anno_publicacion else None,
            'disponibilidad':
            libro.disponibilidad,
        })

    except MaterialBibliografico.DoesNotExist:
        messages.error(request, 'El libro no existe.')
        return redirect('adminBook')
    except Exception as e:
        messages.error(request, f'Error al actualizar el libro: {str(e)}')
        return redirect('adminBook')


@login_required
@user_passes_test(es_Empleado)
def deleteBook(id):
    libro = MaterialBibliografico.objects.get(id=id)
    libro.delete()
    return redirect('admin_book')


def viewBook(request, id):
    book = MaterialBibliografico.objects.get(id=id)
    book.sinopsis = book.sinopsis.replace('\n', '<br/>')
    return render(request, 'viewBook.html', {'book': book})


@login_required
@user_passes_test(es_Empleado)
def getBook(request, id):
    try:
        libro = MaterialBibliografico.objects.get(id=id)
        data = {
            'id':
            libro.id,
            'titulo':
            libro.titulo,
            'sinopsis':
            libro.sinopsis,
            'paginas':
            libro.paginas,
            'autor':
            libro.autor,
            'editorial':
            libro.editorial,
            'tipo':
            libro.tipo,
            'isbn':
            libro.isbn,
            'anno_publicacion':
            libro.anno_publicacion.strftime('%Y-%m-%d')
            if libro.anno_publicacion else None,
            'disponibilidad':
            libro.disponibilidad,
        }
        return JsonResponse(data)
    except MaterialBibliografico.DoesNotExist:
        return JsonResponse({'error': 'Libro no encontrado'}, status=404)


@login_required
def prestamos(request):
    prestamos = PrestamoMaterialBibliografico.objects.all()
    libros = MaterialBibliografico.objects.all()
    return render(request, 'prestamos.html', {
        'prestamos': prestamos,
        'libros': libros
    })


@login_required
@user_passes_test(es_Empleado)
def addPrestamo(request):
    if request.method == 'POST':
        solicitante_email = request.POST.get('solicitante')
        libros_isbn = request.POST.getlist(
            'libros')  # Obtener lista de ISBNs seleccionados
        fecha_devolucion = request.POST.get('fecha_devolucion')
        estado = request.POST.get('estado')

        # Obtener el solicitante y el bibliotecario
        solicitante = User.objects.get(email=solicitante_email)
        bibliotecario = request.user

        # Crear el préstamo
        prestamo = PrestamoMaterialBibliografico.objects.create(
            solicitante=solicitante,
            bibliotecario=bibliotecario,
            fecha_devolucion=fecha_devolucion,
            estado=estado)

        # Asociar los libros al préstamo
        for isbn in libros_isbn:
            libro = MaterialBibliografico.objects.get(isbn=isbn)
            prestamo.libros.add(libro)

        return redirect('prestamos')


@login_required
@user_passes_test(es_Empleado)
def editPrestamo(request):
    if request.method == 'POST':
        prestamo_id = request.POST.get('id')
        libros_isbn = request.POST.getlist(
            'libros')  # Obtener lista de ISBNs seleccionados
        fecha_devolucion = request.POST.get('fecha_devolucion')
        estado = request.POST.get('estado')

        # Obtener el préstamo
        prestamo = PrestamoMaterialBibliografico.objects.get(id=prestamo_id)

        # Actualizar los campos del préstamo
        prestamo.fecha_devolucion = fecha_devolucion
        prestamo.estado = estado
        prestamo.save()

        # Limpiar y asociar los nuevos libros al préstamo
        prestamo.libros.clear()
        for isbn in libros_isbn:
            libro = MaterialBibliografico.objects.get(isbn=isbn)
            prestamo.libros.add(libro)

        return redirect('prestamos')


def contri(request, user_id):
    books = MaterialBibliografico.objects.filter(autor_id=user_id)
    return render(request, 'contri.html', {'books': books})


def test(request):
    return render(request, 'test.html')


def tour_virtual(request):
    return render(request, 'tour_virtual.html')


def prestamo_salas(request):
    return render(request, 'prestamo_salas.html')


