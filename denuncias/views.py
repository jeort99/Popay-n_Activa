from django.shortcuts import get_object_or_404, render, redirect
from .models import Denuncia
from .forms import DenunciaForm

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
            "title": "Geolocalización Precisa",
            "description": "Ubica tu denuncia en el mapa exacto donde ocurre la problemática.",
        },
        {
            "icon": "bi-cpu-fill",
            "title": "Clasificación Inteligente",
            "description": "Nuestro sistema clasifica automáticamente los reportes.",
        },
        {
            "icon": "bi-clock-history",
            "title": "Seguimiento en Tiempo Real",
            "description": "Consulta el estado de tus denuncias en cualquier momento.",
        },
        {
            "icon": "bi-shield-check",
            "title": "Transparencia Total",
            "description": "Visualiza todas las denuncias y su gestión.",
        },
    ]

    categorias = [
        "Infraestructura",
        "Servicios Públicos",
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


def mis_denuncias(request):
    email = request.GET.get("email", "").strip()
    estado = request.GET.get("estado", "").strip()

    denuncias = Denuncia.objects.all()

    if email:
        denuncias = denuncias.filter(usuario__email__iexact=email)

    if estado:
        denuncias = denuncias.filter(estado__iexact=estado)

    estados = Denuncia.objects.order_by().values_list(
        "estado",
        flat=True
    ).distinct()

    return render(
        request,
        "mis_denuncias.html",
        {
            "denuncias": denuncias,
            "email": email,
            "estado": estado,
            "estados": estados,
        },
    )


def registrar_denuncia(request):

    if request.method == "POST":

        form = DenunciaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("lista_denuncias")

    else:
        form = DenunciaForm()

    return render(
        request,
        "registrar_denuncia.html",
        {
            "form": form
        }
    )


def detalle_denuncia(request, denuncia_id):

    denuncia = get_object_or_404(
        Denuncia,
        pk=denuncia_id
    )

    geolocalizacion = None

    try:
        geolocalizacion = denuncia.geolocalizacion

    except Exception:
        geolocalizacion = None

    seguimientos = denuncia.seguimiento_set.order_by('-fecha')

    return render(
        request,
        "detalle_denuncia.html",
        {
            "denuncia": denuncia,
            "geolocalizacion": geolocalizacion,
            "seguimientos": seguimientos,
        },
    )
