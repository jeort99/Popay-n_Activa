from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DenunciaForm, RegistroCiudadanoForm
from .models import Denuncia


def home(request):
    stats = {
        "total": Denuncia.objects.count(),
        "pendientes": Denuncia.objects.filter(estado="Pendiente").count(),
        "proceso": Denuncia.objects.filter(estado="En proceso").count(),
        "resueltas": Denuncia.objects.filter(estado="Resuelta").count(),
    }

    features = [
        {
            "icon": "bi-geo-alt-fill",
            "title": "Geolocalizacion Precisa",
            "description": "Ubica tu denuncia en el mapa exacto donde ocurre la problematica.",
        },
        {
            "icon": "bi-cpu-fill",
            "title": "Clasificacion Inteligente",
            "description": "Nuestro sistema clasifica automaticamente los reportes.",
        },
        {
            "icon": "bi-clock-history",
            "title": "Seguimiento en Tiempo Real",
            "description": "Consulta el estado de tus denuncias en cualquier momento.",
        },
        {
            "icon": "bi-shield-check",
            "title": "Transparencia Total",
            "description": "Visualiza todas las denuncias y su gestion.",
        },
    ]

    categorias = [
        "Infraestructura",
        "Servicios Publicos",
        "Seguridad",
        "Medio Ambiente",
        "Transporte",
        "Salud",
    ]

    return render(
        request,
        "home.html",
        {
            "stats": stats,
            "features": features,
            "categorias": categorias,
        },
    )


def lista_denuncias(request):
    denuncias = Denuncia.objects.all()
    return render(request, "lista.html", {"denuncias": denuncias})


@login_required(login_url="login")
def mis_denuncias(request):
    estado = request.GET.get("estado", "").strip()

    denuncias = Denuncia.objects.filter(usuario__email__iexact=request.user.email)

    if estado:
        denuncias = denuncias.filter(estado__iexact=estado)

    estados = (
        Denuncia.objects.filter(usuario__email__iexact=request.user.email)
        .order_by()
        .values_list("estado", flat=True)
        .distinct()
    )

    return render(
        request,
        "mis_denuncias.html",
        {
            "denuncias": denuncias,
            "estado": estado,
            "estados": estados,
        },
    )


@login_required(login_url="login")
def registrar_denuncia(request):
    if request.method == "POST":
        form = DenunciaForm(request.POST)

        if form.is_valid():
            form.save(request.user)
            return redirect("mis_denuncias")
    else:
        form = DenunciaForm()

    return render(request, "registrar_denuncia.html", {"form": form})


def registro(request):
    if request.method == "POST":
        form = RegistroCiudadanoForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("mis_denuncias")
    else:
        form = RegistroCiudadanoForm()

    return render(request, "registro.html", {"form": form})


def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("mis_denuncias")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def cerrar_sesion(request):
    logout(request)
    return redirect("home")


def detalle_denuncia(request, denuncia_id):
    denuncia = get_object_or_404(Denuncia, pk=denuncia_id)

    geolocalizacion = None

    try:
        geolocalizacion = denuncia.geolocalizacion
    except Exception:
        geolocalizacion = None

    seguimientos = denuncia.seguimiento_set.order_by("-fecha")

    return render(
        request,
        "detalle_denuncia.html",
        {
            "denuncia": denuncia,
            "geolocalizacion": geolocalizacion,
            "seguimientos": seguimientos,
        },
    )
