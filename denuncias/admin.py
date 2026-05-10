from django.contrib import admin
from .models import (
    Usuario, Categoria, Denuncia,
    Geolocalizacion, Seguimiento, ClasificacionIA
)

# USUARIOS
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'email', 'rol', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('rol',)
    ordering = ('-fecha_registro',)
    list_per_page = 20


# CATEGORÍAS
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)
    list_per_page = 20


# DENUNCIAS
@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'usuario', 'categoria', 'estado', 'fecha_registro')
    list_filter = ('estado', 'categoria')
    search_fields = ('titulo', 'descripcion', 'usuario__email')
    ordering = ('-fecha_registro',)
    list_editable = ('estado',)
    date_hierarchy = 'fecha_registro'
    list_per_page = 20


# GEOLOCALIZACIÓN
@admin.register(Geolocalizacion)
class GeolocalizacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'denuncia', 'direccion', 'latitud', 'longitud')
    search_fields = ('direccion',)
    list_per_page = 20


# SEGUIMIENTO
@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'denuncia', 'funcionario', 'estado', 'fecha')
    list_filter = ('estado',)
    search_fields = ('denuncia__titulo', 'funcionario__email')
    ordering = ('-fecha',)
    date_hierarchy = 'fecha'
    list_per_page = 20


# IA
@admin.register(ClasificacionIA)
class ClasificacionIAAdmin(admin.ModelAdmin):
    list_display = ('id', 'denuncia', 'categoria_predicha', 'confianza', 'fecha')
    search_fields = ('denuncia__titulo', 'categoria_predicha')
    ordering = ('-fecha',)
    list_per_page = 20