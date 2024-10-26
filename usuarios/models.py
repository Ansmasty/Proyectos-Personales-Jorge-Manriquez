from django.db import models
from django.contrib.auth.models import AbstractUser


#Modelos que funcionan como tablas en la base de datos	

#Modelo Usuario que hereda de AbstractUser, clase de Django que contiene los campos de un usuario
class Usuario(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    nombre_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    carrera = models.CharField(max_length=255)
    sede = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    patente = models.CharField(max_length=255, null=True, blank=True)
    vehiculo = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

#Modelo Viaje que contiene los campos de un viaje
class Viaje(models.Model):
    origen = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    hora = models.TimeField()
    cupos = models.IntegerField()
    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='viajes_conducidos')
    pasajeros = models.ManyToManyField(Usuario, related_name='viajes_como_pasajero', null=True, blank=True)
    activo = models.BooleanField(default=True)