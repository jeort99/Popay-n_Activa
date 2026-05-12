from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import (
    Categoria,
    ClasificacionIA,
    Denuncia,
    Geolocalizacion,
    Seguimiento,
    Usuario,
)


admin.site.unregister(User)


@admin.register(User)
class AdministradorUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        if not change:
            obj.is_superuser = False
        super().save_model(request, obj, form, change)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellido", "email", "rol", "fecha_registro")
    search_fields = ("nombre", "apellido", "email")
    list_filter = ("rol",)
    ordering = ("-fecha_registro",)
    list_per_page = 20


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre",)
    ordering = ("nombre",)
    list_per_page = 20


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "usuario", "categoria", "estado", "fecha_registro")
    list_filter = ("estado", "categoria")
    search_fields = ("titulo", "descripcion", "usuario__email")
    ordering = ("-fecha_registro",)
    list_editable = ("estado",)
    date_hierarchy = "fecha_registro"
    list_per_page = 20


@admin.register(Geolocalizacion)
class GeolocalizacionAdmin(admin.ModelAdmin):
    list_display = ("id", "denuncia", "direccion", "latitud", "longitud")
    search_fields = ("direccion",)
    list_per_page = 20


@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ("id", "denuncia", "funcionario", "estado", "fecha")
    list_filter = ("estado",)
    search_fields = ("denuncia__titulo", "funcionario__email")
    ordering = ("-fecha",)
    date_hierarchy = "fecha"
    list_per_page = 20


@admin.register(ClasificacionIA)
class ClasificacionIAAdmin(admin.ModelAdmin):
    list_display = ("id", "denuncia", "categoria_predicha", "confianza", "fecha")
    search_fields = ("denuncia__titulo", "categoria_predicha")
    ordering = ("-fecha",)
    list_per_page = 20
