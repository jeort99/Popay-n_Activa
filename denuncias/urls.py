from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('denuncias/', views.lista_denuncias, name='lista_denuncias'),
    path('denuncias/nueva/', views.registrar_denuncia, name='registrar_denuncia'),
    path('denuncias/mis/', views.mis_denuncias, name='mis_denuncias'),
    path('denuncias/<int:denuncia_id>/', views.detalle_denuncia, name='detalle_denuncia'),
]
