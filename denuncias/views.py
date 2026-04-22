from django.shortcuts import get_object_or_404, render, redirect
from .models import Denuncia
from .forms import DenunciaForm


def home(request):
    return render(request, "home.html")


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

    estados = Denuncia.objects.order_by().values_list("estado", flat=True).distinct()

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

    return render(request, "registrar_denuncia.html", {"form": form})


def editar_estado(request, denuncia_id):
    denuncia = get_object_or_404(Denuncia, pk=denuncia_id)
    estados = ["Pendiente", "En Proceso", "Resuelta"]

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        if nuevo_estado in estados:
            denuncia.estado = nuevo_estado
            denuncia.save()
            return redirect("lista_denuncias")

    return render(
        request,
        "editar_estado.html",
        {"denuncia": denuncia, "estados": estados},
    )


def detalle_denuncia(request, denuncia_id):
    denuncia = get_object_or_404(Denuncia, pk=denuncia_id)
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
