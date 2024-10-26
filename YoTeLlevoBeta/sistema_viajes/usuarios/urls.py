from django.urls import path
from . import views

urlpatterns = [
    # Templates
    path('registro/', views.registro, name='registro'),
    path('homeConductor/', views.homeConductor, name='homeConductor'),
    path('perfilUsuarioConductor/', views.perfil_usuario_conductor, name='perfilUsuarioConductor'),
    path('perfilUsuarioPasajero/', views.perfil_usuario_pasajero, name='perfilUsuarioPasajero'),
    path('homePasajero/', views.homePasajero, name='homePasajero'),
    path('', views.vista_login, name='VistaInicioDeSesion'),
    path('destinoConductor/', views.vista_destinos, name='destinoConductor'),

    # Funciones
    
    path('login/', views.InicioDeSesion, name='login'),
    path('RegistrarUsuario/', views.RegistrarUsuario, name='RegistrarUsuario'),
    path('registrarViaje/', views.RegistrarViaje, name='RegistrarViaje'),
    path('activar_viaje/<int:viaje_id>/', views.activar_viaje, name='activar_viaje'),
    path('reservar_viaje/<int:viaje_id>/', views.reservar_viaje, name='reservar_viaje'),
    path('cancelar_reserva/<int:viaje_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('editar_usuario_conductor/', views.editar_usuario_conductor, name='editar_usuario_conductor'),
    path('CambiarContraseña/', views.CambiarContraseña, name='CambiarContraseña'),
    path('editar_usuario_pasajero/', views.editar_usuario_pasajero, name='editar_usuario_pasajero'),
    path('EliminarCuenta/', views.EliminarCuenta, name='EliminarCuenta'),
    path('CerrarSesion/', views.CerrarSesion, name='CerrarSesion'),
    path('eliminar_viaje/<int:viaje_id>/', views.eliminar_viaje, name='eliminar_viaje'),
    path('modificar_viaje/<int:viaje_id>/', views.modificar_viaje, name='modificar_viaje'),
]    