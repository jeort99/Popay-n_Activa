from decimal import Decimal

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import DenunciaForm, RegistroCiudadanoForm
from .models import Denuncia, ESTADO_EN_PROCESO, ESTADO_PENDIENTE, ESTADO_RESUELTA


def home(request):
    stats = {
        "total": Denuncia.objects.count(),
        "pendientes": Denuncia.objects.filter(estado=ESTADO_PENDIENTE).count(),
        "proceso": Denuncia.objects.filter(estado=ESTADO_EN_PROCESO).count(),
        "resueltas": Denuncia.objects.filter(estado=ESTADO_RESUELTA).count(),
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

    categorias_servicio = [
        {
            "nombre": "Infraestructura",
            "entidad": "Secretaria de Infraestructura Municipal",
            "descripcion": "Atiende reportes sobre vias, andenes, puentes, parques, huecos y deterioro del espacio publico.",
        },
        {
            "nombre": "Servicios Publicos",
            "entidad": "Empresas prestadoras y oficina de servicios publicos",
            "descripcion": "Gestiona fallas relacionadas con agua, energia, alumbrado, residuos y alcantarillado.",
        },
        {
            "nombre": "Seguridad",
            "entidad": "Secretaria de Gobierno, Policia Nacional y organismos de convivencia",
            "descripcion": "Recibe alertas sobre inseguridad, vandalismo, conflictos ciudadanos y situaciones de riesgo.",
        },
        {
            "nombre": "Medio Ambiente",
            "entidad": "Autoridad ambiental y dependencia municipal de ambiente",
            "descripcion": "Orienta casos de contaminacion, ruido, escombros, manejo de arbolado y afectaciones ambientales.",
        },
        {
            "nombre": "Transporte",
            "entidad": "Secretaria de Transito y Transporte",
            "descripcion": "Atiende problemas de movilidad, rutas, paraderos, senalizacion vial y congestion vehicular.",
        },
        {
            "nombre": "Salud",
            "entidad": "Secretaria de Salud Municipal",
            "descripcion": "Gestiona reportes sanitarios, plagas, riesgos de salud publica y acceso a servicios de atencion.",
        },
    ]

    return render(
        request,
        "home.html",
        {
            "stats": stats,
            "features": features,
            "categorias": categorias_servicio,
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
        form = DenunciaForm(request.POST, request.FILES)

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
    next_url = request.POST.get("next") or request.GET.get("next") or "mis_denuncias"

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect("mis_denuncias")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form, "next": next_url})


def cerrar_sesion(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def detalle_denuncia(request, denuncia_id):
    denuncia = get_object_or_404(Denuncia, pk=denuncia_id)

    geolocalizacion = None
    mapa_url = None

    try:
        geolocalizacion = denuncia.geolocalizacion
        margen = Decimal("0.004")
        latitud = geolocalizacion.latitud
        longitud = geolocalizacion.longitud
        mapa_url = (
            "https://www.openstreetmap.org/export/embed.html"
            f"?bbox={longitud - margen},{latitud - margen},{longitud + margen},{latitud + margen}"
            f"&layer=mapnik&marker={latitud},{longitud}"
        )
    except Exception:
        geolocalizacion = None

    seguimientos = denuncia.seguimiento_set.order_by("-fecha")

    return render(
        request,
        "detalle_denuncia.html",
        {
            "denuncia": denuncia,
            "geolocalizacion": geolocalizacion,
            "mapa_url": mapa_url,
            "seguimientos": seguimientos,
        },
    )
