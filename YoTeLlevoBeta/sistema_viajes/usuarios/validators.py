from django.core.exceptions import ValidationError

#Función que valida los cupos
def validar_cupos(value):
    if value < 1 or value > 8:
        raise ValidationError('El número de cupos debe estar entre 1 y 8.')