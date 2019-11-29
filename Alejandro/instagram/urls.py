from django.contrib import admin
from django.urls import path
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.home, name='home'),
    path('registro', app_views.registro, name='registro'),
    path('noticias', app_views.noticias, name='noticias'),
    path('logout', app_views.logout, name='logout'),
    path('perfil', app_views.perfil, name='perfil'),
    
    path('agregar_publicacion', app_views.agregar_publicacion, name='agregar_publicacion'),
    path('borrar_publicacion', app_views.borrar_publicacion, name='borrar_publicacion'),
    path('editar_perfil', app_views.editar_perfil, name='editar_perfil'),
    path('seguir_perfil', app_views.seguir_perfil, name='seguir_perfil'),
    
    path('comentar', app_views.comentar, name='comentar'),
    path('borrar_comentario', app_views.borrar_comentario, name='borrar_comentario'),
    path('me_gusta', app_views.me_gusta, name='me_gusta'),
]