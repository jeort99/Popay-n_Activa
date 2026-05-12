from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Categoria, Denuncia, Usuario


class RegistroCiudadanoForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        label="Nombre",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre"}),
    )
    last_name = forms.CharField(
        max_length=100,
        label="Apellido",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu apellido"}),
    )
    email = forms.EmailField(
        label="Correo electronico",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ejemplo@correo.com"}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este correo.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_staff = False
        user.is_superuser = False

        if commit:
            user.save()
            Usuario.objects.get_or_create(
                email=user.email,
                defaults={
                    "nombre": user.first_name,
                    "apellido": user.last_name,
                    "password_hash": "django-auth",
                    "rol": "Ciudadano",
                },
            )

        return user


class DenunciaForm(forms.Form):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all().order_by("nombre"),
        required=False,
        empty_label="Sin categoria",
        label="Categoria",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    titulo = forms.CharField(
        max_length=200,
        label="Titulo de la denuncia",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Breve titulo"}),
    )
    descripcion = forms.CharField(
        label="Descripcion",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Describe lo que sucedio con el mayor detalle posible.",
            }
        ),
    )

    def save(self, user):
        datos = self.cleaned_data
        usuario, _ = Usuario.objects.get_or_create(
            email=user.email,
            defaults={
                "nombre": user.first_name,
                "apellido": user.last_name,
                "password_hash": "django-auth",
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
