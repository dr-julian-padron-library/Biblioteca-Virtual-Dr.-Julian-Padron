from django import forms
from .models import MaterialBibliografico, Multa, PrestamoMaterialBibliografico, PrestamoSala, SalaTematica
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class MaterialBibliograficoForm(forms.ModelForm):

    class Meta:
        model = MaterialBibliografico
        fields = '__all__'

    # categoria_CHOICES = [
    #     ('Educacion', 'Educación'),
    #     ('Ficcion', 'Ficción'),
    #     ('Ciencia', 'Ciencia'),
    #     # Add more categories as needed
    # ]

    # categoria = forms.ChoiceField(choices=categoria_CHOICES)

    # def __init__(self, *args, **kwargs):
    #     super(MaterialBibliograficoForm, self).__init__(*args, **kwargs)
    #     self.fields['titulo'].widget.attrs.update({
    #         'class':
    #         'form-control',
    #         'placeholder':
    #         'Introducir Titulo...'
    #     })
    #     self.fields['sinopsis'].widget.attrs.update({
    #         'class':
    #         'form-control',
    #         'placeholder':
    #         'Introducir Descripción...'
    #     })
    #     self.fields['paginas'].widget.attrs.update({
    #         'class':
    #         'form-control',
    #         'placeholder':
    #         'Numero de Paginas...'
    #     })
    #     self.fields['pdf'].widget.attrs.update({
    #         'class':
    #         'form-control',
    #         'placeholder':
    #         'Introducir PDF...'
    #     })
    #     self.fields['categoria'].widget.attrs.update({
    #         'class':
    #         'form-control',
    #         'placeholder':
    #         'Selecionar Categoria...'
    #     })

    #     # Make all fields required
    #     for field_name, field in self.fields.items():
    #         field.required = True


class MultaForm(forms.ModelForm):

    class Meta:
        model = Multa
        fields = ['fecha_cierre']  # , 'prestamo'

    def __init__(self, *args, **kwargs):
        self.fields['fecha_cierre'].widget.attrs.update({
            'class':
            'form-control',
            'placeholder':
            'Introducir Fecha de Cierre de multa...'
        })
        # self.fields['prestamo'].widget.attrs.update({
        #     'class':
        #     'form-control',
        #     'placeholder':
        #     'Introducir Codigo de prestamo...'
        # })


class PerfilForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label="Contraseña Actual")
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label="Nueva Contraseña")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label="Confirmar Nueva Contraseña")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        current_password = cleaned_data.get("current_password")

        # Si se proporciona una nueva contraseña, se requiere la actual
        if new_password or confirm_password:
            if not current_password:
                raise forms.ValidationError(
                    "Debes ingresar tu contraseña actual para cambiarla.")

            # Verificar que la nueva contraseña coincide
            if new_password != confirm_password:
                raise forms.ValidationError(
                    "Las nuevas contraseñas no coinciden.")

        return cleaned_data
