from django.contrib import admin
from .models import Usuario, Categoria, Denuncia, Geolocalizacion, Seguimiento, ClasificacionIA


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'email', 'rol', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email', 'rol')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'usuario', 'categoria', 'estado', 'fecha_registro')
    list_filter = ('estado', 'categoria')
    search_fields = ('titulo', 'descripcion', 'usuario__email', 'usuario__nombre')


@admin.register(Geolocalizacion)
class GeolocalizacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'denuncia', 'direccion', 'latitud', 'longitud')


@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'denuncia', 'funcionario', 'estado', 'fecha')
    search_fields = ('denuncia__titulo', 'funcionario__nombre', 'funcionario__email')


@admin.register(ClasificacionIA)
class ClasificacionIAAdmin(admin.ModelAdmin):
    list_display = ('id', 'denuncia', 'categoria_predicha', 'confianza', 'fecha')
    search_fields = ('denuncia__titulo', 'categoria_predicha')
