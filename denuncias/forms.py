from django import forms
from .models import Categoria, Denuncia, Usuario

class DenunciaForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre"}),
    )
    apellido = forms.CharField(
        max_length=100,
        label="Apellido",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu apellido"}),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ejemplo@correo.com"}),
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all().order_by("nombre"),
        required=False,
        empty_label="Sin categoría",
        label="Categoría",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    titulo = forms.CharField(
        max_length=200,
        label="Título de la denuncia",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Breve título"}),
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Describe lo que sucedió con el mayor detalle posible."}),
    )

    def save(self):
        datos = self.cleaned_data
        usuario, _ = Usuario.objects.get_or_create(
            email=datos["email"],
            defaults={
                "nombre": datos["nombre"],
                "apellido": datos["apellido"],
                "password_hash": "anonimo",
                "rol": "Ciudadano",
            },
        )
        denuncia = Denuncia.objects.create(
            usuario=usuario,
            categoria=datos["categoria"],
            titulo=datos["titulo"],
            descripcion=datos["descripcion"],
            estado="Pendiente",
        )
        return denuncia
