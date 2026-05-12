from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from ia.classificador import analizar_denuncia

from .models import Categoria, ClasificacionIA, Denuncia, Geolocalizacion, Usuario


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
    latitud = forms.DecimalField(
        max_digits=9,
        decimal_places=6,
        min_value=-90,
        max_value=90,
        required=False,
        widget=forms.HiddenInput(),
    )
    longitud = forms.DecimalField(
        max_digits=9,
        decimal_places=6,
        min_value=-180,
        max_value=180,
        required=False,
        widget=forms.HiddenInput(),
    )
    direccion = forms.CharField(
        max_length=255,
        required=False,
        label="Direccion o referencia",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ejemplo: carrera, barrio o punto de referencia",
            }
        ),
    )

    def clean(self):
        datos = super().clean()
        latitud = datos.get("latitud")
        longitud = datos.get("longitud")

        if (latitud is None) != (longitud is None):
            raise forms.ValidationError("Captura la ubicacion completa antes de enviar la denuncia.")

        return datos

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

        if datos.get("latitud") is not None and datos.get("longitud") is not None:
            Geolocalizacion.objects.create(
                denuncia=denuncia,
                latitud=datos["latitud"],
                longitud=datos["longitud"],
                direccion=datos.get("direccion") or "Ubicacion capturada desde el navegador",
            )

        resultado_ia = analizar_denuncia(datos["titulo"], datos["descripcion"])
        ClasificacionIA.objects.create(
            denuncia=denuncia,
            categoria_predicha=resultado_ia["categoria_predicha"],
            confianza=resultado_ia["confianza"],
            validez=resultado_ia["validez"],
            motivo=resultado_ia["motivo"],
        )

        return denuncia
