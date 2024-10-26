# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=255)
    email = forms.EmailField()
    carrera = forms.CharField(max_length=255)
    sede = forms.CharField(max_length=255)
    licencia_conducir = forms.CharField(max_length=20, required=False)
    vehiculo = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'carrera', 'sede', 'password1', 'password2', 'licencia_conducir', 'vehiculo']