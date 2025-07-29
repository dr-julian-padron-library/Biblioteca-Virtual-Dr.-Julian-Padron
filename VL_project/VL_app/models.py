from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
class MaterialBibliografico(models.Model):

    TIPO_CHOICES = [
        ('libro', 'Libro'),
        ('revista', 'Revista'),
        ('referencia', 'Referencia'),
    ]

    titulo = models.CharField(max_length=80)
    sinopsis = models.TextField(max_length=2000)
    paginas = models.CharField(max_length=80)
    pdf = models.FileField(upload_to='pdfs/')
    autor = models.CharField(max_length=80)
    editorial = models.CharField(max_length=80)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    anno_publicacion = models.DateField(blank=True, null=True)
    disponibilidad = models.BooleanField(default=True)
    isbn = models.CharField(max_length=13, unique=True)

    #genero
    #categoria
    def __str__(self):
        return f"{self.titulo}"


class PrestamoMaterialBibliografico(models.Model):
    ESTADO_CHOICES = [
        ('solicitado', 'Solicitado'),
        ('retirado', 'Retirado'),
        ('devuelto', 'Devuelto'),
        ('atrasado', 'Atrasado'),
        ('no_entregado', 'No entregado'),
    ]

    fecha_prestamo = models.DateField(auto_now_add=True)  # Fecha automática al crear el préstamo
    fecha_devolucion = models.DateField()  # Fecha límite de devolución
    solicitante = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="prestamos_solicitados")  # Usuario que solicita
    bibliotecario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="prestamos_gestionados")  # Bibliotecario que gestiona
    estado = models.CharField(max_length=20,
                              choices=ESTADO_CHOICES,
                              default='solicitado')  # Estado del préstamo
    libros = models.ManyToManyField('MaterialBibliografico', related_name='prestamos')  # Relación muchos a muchos con MaterialBibliografico

    def __str__(self):
        return f"Préstamo de {self.solicitante} - Estado: {self.estado}"


class PrestamoSala(models.Model):
    fecha_prestamo = models.DateField(
        auto_now_add=True)  # Se asigna automáticamente al crear el préstamo
    fecha_devolucion = models.DateField(
    )  # Fecha en que se debe devolver el uso de la sala
    nombre_actividad = models.CharField(
        max_length=255)  # Nombre de la actividad a realizar
    descripcion = models.TextField()  # Descripción detallada del evento
    nombre_organizacion = models.CharField(
        max_length=255)  # Nombre de la organización que solicita la sala
    numero_contacto = models.CharField(
        max_length=15)  # Teléfono de contacto de la organización
    correo = models.EmailField()  # Correo electrónico de la organización
    # Datos del representante
    nombre_representante = models.CharField(
        max_length=255)  # Nombre completo del representante
    ci_representante = models.CharField(
        max_length=20, unique=True)  # Cédula de identidad del representante
    numero_contacto_representante = models.CharField(
        max_length=15)  # Teléfono del representante
    correo_representante = models.EmailField()  # Correo del representante
    numero_participantes = models.PositiveIntegerField(
    )  # Cantidad de personas que asistirán

    def __str__(self):
        return f"{self.nombre_actividad} - {self.nombre_organizacion}"


def obtener_ultimo_prestamo():
    return PrestamoMaterialBibliografico.objects.last().id


class Multa(models.Model):
    fecha_inicio = models.DateField(
        auto_now_add=True)  # Fecha en que se genera la multa
    fecha_cierre = models.DateField(
        null=True, blank=True)  # Fecha en que se paga o se elimina la multa
    # prestamo = models.ForeignKey(
    #     'PrestamoMaterialBibliografico',
    #     on_delete=models.CASCADE,
    #     related_name="multas",
    #     default=obtener_ultimo_prestamo())  # Relación con el préstamo asociado

    def __str__(self):
        return f"Multa {self.id} - {self.prestamo.solicitante}"


class SalaTematica(models.Model):
    codigo_tema = models.CharField(
        max_length=50, unique=True)  # Código único para identificar el tema
    nombre_tema = models.CharField(
        max_length=255)  # Nombre del tema tratado en la sala
    nombre_sala = models.CharField(
        max_length=255)  # Nombre de la sala temática

    def __str__(self):
        return f"{self.codigo_tema} - {self.nombre_sala} - {self.nombre_tema}"
