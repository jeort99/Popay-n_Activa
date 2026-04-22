from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('denuncias/', views.lista_denuncias, name='lista_denuncias'),
    path('denuncias/nueva/', views.registrar_denuncia, name='registrar_denuncia'),
    path('denuncias/mis/', views.mis_denuncias, name='mis_denuncias'),
    path('denuncias/<int:denuncia_id>/editar-estado/', views.editar_estado, name='editar_estado'),
    path('denuncias/<int:denuncia_id>/', views.detalle_denuncia, name='detalle_denuncia'),
]
