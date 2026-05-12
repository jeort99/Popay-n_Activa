from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import (
    ESTADO_EN_PROCESO,
    ESTADO_PENDIENTE,
    ESTADO_RESUELTA,
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
    list_filter = ("rol", "fecha_registro")
    ordering = ("-fecha_registro",)
    readonly_fields = ("fecha_registro", "password_hash")
    list_per_page = 20


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre",)
    ordering = ("nombre",)
    list_per_page = 20


class GeolocalizacionInline(admin.StackedInline):
    model = Geolocalizacion
    extra = 0
    max_num = 1
    fields = ("direccion", "latitud", "longitud", "ver_mapa")
    readonly_fields = ("ver_mapa",)

    @admin.display(description="Mapa")
    def ver_mapa(self, obj):
        if not obj or obj.latitud is None or obj.longitud is None:
            return "Sin ubicacion registrada"

        url = f"https://www.openstreetmap.org/?mlat={obj.latitud}&mlon={obj.longitud}#map=18/{obj.latitud}/{obj.longitud}"
        return format_html('<a href="{}" target="_blank" rel="noopener">Ver en OpenStreetMap</a>', url)


class SeguimientoInline(admin.TabularInline):
    model = Seguimiento
    extra = 1
    fields = ("funcionario", "estado", "comentario", "fecha")
    readonly_fields = ("fecha",)
    autocomplete_fields = ("funcionario",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "funcionario":
            kwargs["queryset"] = Usuario.objects.exclude(rol="Ciudadano").order_by("nombre", "apellido")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ClasificacionIAInline(admin.TabularInline):
    model = ClasificacionIA
    extra = 0
    can_delete = False
    fields = ("categoria_predicha", "confianza", "validez", "motivo", "fecha")
    readonly_fields = ("categoria_predicha", "confianza", "validez", "motivo", "fecha")


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "titulo",
        "ciudadano",
        "categoria",
        "estado",
        "fecha_registro",
        "ubicacion",
        "tiene_foto",
        "validacion_ia",
    )
    list_filter = ("estado", "categoria", "fecha_registro")
    search_fields = (
        "titulo",
        "descripcion",
        "usuario__nombre",
        "usuario__apellido",
        "usuario__email",
    )
    ordering = ("-fecha_registro",)
    list_editable = ("estado",)
    readonly_fields = ("fecha_registro", "datos_ciudadano", "vista_previa_imagen", "enlace_mapa")
    fieldsets = (
        ("Denuncia", {"fields": ("titulo", "descripcion", "categoria", "estado", "fecha_registro")}),
        ("Evidencia fotografica", {"fields": ("imagen", "vista_previa_imagen")}),
        ("Ciudadano", {"fields": ("usuario", "datos_ciudadano")}),
        ("Ubicacion", {"fields": ("enlace_mapa",)}),
    )
    inlines = (ClasificacionIAInline, GeolocalizacionInline, SeguimientoInline)
    actions = ("marcar_pendiente", "marcar_en_proceso", "marcar_resuelta")
    date_hierarchy = "fecha_registro"
    autocomplete_fields = ("usuario", "categoria")
    list_per_page = 20

    @admin.display(description="Ciudadano", ordering="usuario__email")
    def ciudadano(self, obj):
        return obj.usuario

    @admin.display(description="Datos del ciudadano")
    def datos_ciudadano(self, obj):
        return format_html(
            "<strong>{} {}</strong><br>{}",
            obj.usuario.nombre,
            obj.usuario.apellido,
            obj.usuario.email,
        )

    @admin.display(description="Ubicacion")
    def ubicacion(self, obj):
        if hasattr(obj, "geolocalizacion"):
            return "Registrada"
        return "Sin ubicacion"

    @admin.display(description="Foto")
    def tiene_foto(self, obj):
        if obj.imagen:
            return "Registrada"
        return "Sin foto"

    @admin.display(description="Vista previa")
    def vista_previa_imagen(self, obj):
        if not obj or not obj.imagen:
            return "Sin foto registrada"
        return format_html(
            '<img src="{}" style="max-width: 360px; height: auto; border-radius: 8px;" alt="Foto de la denuncia">',
            obj.imagen.url,
        )

    @admin.display(description="IA")
    def validacion_ia(self, obj):
        clasificacion = obj.clasificacionia_set.order_by("-fecha").first()
        if not clasificacion:
            return "Sin clasificacion"
        return f"{clasificacion.validez} ({clasificacion.confianza:.0%})"

    @admin.display(description="Mapa")
    def enlace_mapa(self, obj):
        if not obj or not hasattr(obj, "geolocalizacion"):
            return "Sin ubicacion registrada"

        geo = obj.geolocalizacion
        url = f"https://www.openstreetmap.org/?mlat={geo.latitud}&mlon={geo.longitud}#map=18/{geo.latitud}/{geo.longitud}"
        return format_html('<a href="{}" target="_blank" rel="noopener">Ver ubicacion en mapa</a>', url)

    @admin.action(description="Marcar seleccionadas como pendientes")
    def marcar_pendiente(self, request, queryset):
        queryset.update(estado=ESTADO_PENDIENTE)

    @admin.action(description="Marcar seleccionadas en proceso")
    def marcar_en_proceso(self, request, queryset):
        queryset.update(estado=ESTADO_EN_PROCESO)

    @admin.action(description="Marcar seleccionadas como resueltas")
    def marcar_resuelta(self, request, queryset):
        queryset.update(estado=ESTADO_RESUELTA)


@admin.register(Geolocalizacion)
class GeolocalizacionAdmin(admin.ModelAdmin):
    list_display = ("id", "denuncia", "direccion", "latitud", "longitud", "ver_mapa")
    search_fields = ("direccion", "denuncia__titulo")
    autocomplete_fields = ("denuncia",)
    list_per_page = 20

    @admin.display(description="Mapa")
    def ver_mapa(self, obj):
        url = f"https://www.openstreetmap.org/?mlat={obj.latitud}&mlon={obj.longitud}#map=18/{obj.latitud}/{obj.longitud}"
        return format_html('<a href="{}" target="_blank" rel="noopener">Abrir mapa</a>', url)


@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ("id", "denuncia", "funcionario", "estado", "fecha")
    list_filter = ("estado", "fecha")
    search_fields = ("denuncia__titulo", "funcionario__email", "funcionario__nombre", "comentario")
    ordering = ("-fecha",)
    readonly_fields = ("fecha",)
    autocomplete_fields = ("denuncia", "funcionario")
    date_hierarchy = "fecha"
    list_per_page = 20


@admin.register(ClasificacionIA)
class ClasificacionIAAdmin(admin.ModelAdmin):
    list_display = ("id", "denuncia", "categoria_predicha", "confianza", "validez", "fecha")
    list_filter = ("validez", "categoria_predicha", "fecha")
    search_fields = ("denuncia__titulo", "categoria_predicha", "validez", "motivo")
    readonly_fields = ("fecha",)
    autocomplete_fields = ("denuncia",)
    ordering = ("-fecha",)
    list_per_page = 20
