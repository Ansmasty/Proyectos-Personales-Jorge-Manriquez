from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required 
from .models import Usuario, Viaje
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from django.contrib import messages

#Función que permite el inicio de sesión de un usuario, obteniendo el token de la sesión
def InicioDeSesion(request):
    if request.method == 'POST':
        tipo_usuario = request.POST.get('tipo_usuario')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if tipo_usuario == 'Conductor':
                return redirect(homeConductor)
            elif tipo_usuario == 'Pasajero':
                return redirect(homePasajero)
            else:
                return render(request, 'index.html', {'error': 'Tipo de usuario incorrecto'})
        else:
            return render(request, 'index.html', {'error': 'Credenciales de usuario incorrectas'})
    else:
        csrf_token = get_token(request)
        return render(request, 'index.html', {'csrf_token': csrf_token})


#Función que permite registrar un viaje obteniendo el token de la sesión y validando los datos ingresados
@login_required
def RegistrarViaje(request):
    if request.method == 'POST':
        origen = request.POST.get('origen')
        destino = request.POST.get('destino')
        hora = request.POST.get('hora')
        cupos = request.POST.get('cupos')

        conductor_id = request.user.id

        if not conductor_id:
            return render(request, 'VistaConductor.html', {'error': 'Conductor no identificado'})

        try:
            conductor = Usuario.objects.get(id=conductor_id)
        except Usuario.DoesNotExist:
            return render(request, 'VistaConductor.html', {'error': 'Conductor no encontrado'})
        
        if int(cupos) < 1 or int(cupos) > 8:
            return render(request, 'VistaConductor.html', {'error': 'El número de cupos debe estar entre 1 y 8'})  

        try:
            viaje = Viaje.objects.create(origen=origen, destino=destino, hora=str(hora), cupos=cupos, conductor_id=conductor.id)

            return redirect(vista_destinos)
        except IntegrityError as e:
            print(f"Error al registrar el viaje: {e}")
            return render(request, 'VistaConductor.html', {'error': 'Error al registrar el viaje'})

    return render(request, 'VistaConductor.html')

#Función que permite el registro de un usuario en el sistema
def RegistrarUsuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nombre_completo = request.POST.get('nombre_completo')
        email = request.POST.get('email')
        carrera = request.POST.get('carrera')
        sede = request.POST.get('sede')
        password = request.POST.get('password')
        confirmar_password = request.POST.get('password2')

        if not email.endswith('@inacapmail.cl'):
            return render(request, 'VistaRegistro.html', {'error': 'El tipo correo electronico debe ser de INACAP'})

        if Usuario.objects.filter(email=email).exists():
            return render(request, 'VistaRegistro.html', {'error': 'El correo electrónico ya está registrado'})
        
        if password != confirmar_password:
            return render(request, 'VistaRegistro.html', {'error': 'Las contraseñas no coinciden'})

        if Usuario.objects.filter(username=username).exists():
            return render(request, 'VistaRegistro.html', {'error': 'El nombre de usuario ya está registrado'})

        user = Usuario.objects.create_user(username=username, nombre_completo=nombre_completo, email=email, password=password, carrera=carrera, sede=sede)
        return redirect('login')

    return render(request, 'VistaRegistro.html')

def CerrarSesion(request):
    if request.method == 'POST':
        logout(request)
        return redirect('VistaInicioDeSesion')
    else:
        csrf_token = get_token(request)
        return render(request, 'VistaPerfilUsuarioConductor.html', {'csrf_token': csrf_token})
    
#Función que permite eliminar una cuenta
@login_required
def EliminarCuenta(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST['password']

        if not check_password(password, user.password):
            return JsonResponse({'success': False, 'message': 'Contraseña incorrecta'})

        user.delete()
        logout(request)
        return JsonResponse({'success': True, 'message': 'Cuenta eliminada exitosamente'})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

#Función que permite editar un usuario
@login_required
def editar_usuario_conductor(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        carrera = request.POST.get('carrera')
        sede = request.POST.get('sede')
        patente = request.POST.get('patente')
        vehiculo = request.POST.get('vehiculo')
        telefono = request.POST.get('telefono')

        if username:
            user.username = username
        if carrera:
            user.carrera = carrera
        if sede:
            user.sede = sede
        if patente:
            user.patente = patente
        if vehiculo:
            user.vehiculo = vehiculo
        if telefono:
            user.telefono = telefono

        user.save()
        return redirect('perfilUsuarioConductor')
    return render(request, 'VistaPerfilUsuarioConductor.html')

#Función que permite editar un usuario pasajero
@login_required
def editar_usuario_pasajero(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        carrera = request.POST.get('carrera')
        sede = request.POST.get('sede')
        telefono = request.POST.get('telefono')

        if username:
            user.username = username
        if carrera:
            user.carrera = carrera
        if sede:
            user.sede = sede
        if telefono:
            user.telefono = telefono
        user.save()
        return redirect('perfilUsuarioPasajero')
    return render(request, 'VistaPerfilUsuarioPasajero.html')

#Función que permite cambiar la contraseña del usuario
@login_required
def CambiarContraseña(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST['password']
        new_password = request.POST['password_nueva']
        confirm_password = request.POST['confirmar_password']

        if not check_password(password, user.password):
            return JsonResponse({'success': False, 'message': 'Contraseña incorrecta'})

        if new_password != confirm_password:
            return JsonResponse({'success': False, 'message': 'Las contraseñas no coinciden'})

        user.set_password(new_password)
        user.save()
        return JsonResponse({'success': True, 'message': 'Contraseña cambiada exitosamente'})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

#Función que permite a un pasajero reservar viajes
@login_required
def reservar_viaje(request, viaje_id):
    viaje = get_object_or_404(Viaje, id=viaje_id)
    if viaje.cupos > 0 and not Viaje.objects.filter(pasajeros=request.user).exists():
        viaje.pasajeros.add(request.user)
        viaje.cupos -= 1
        viaje.save()
    return redirect('homePasajero')

#Función que permite a un pasajero cancelar una reserva de un viaje
@login_required
def cancelar_reserva(request, viaje_id):
    viaje = get_object_or_404(Viaje, id=viaje_id)
    if request.user in viaje.pasajeros.all():
        viaje.pasajeros.remove(request.user)
        viaje.cupos += 1
        viaje.save()
    return redirect('homePasajero')

#Función que permite al conductor eliminar un viaje
@login_required
def eliminar_viaje(request, viaje_id):
    viaje = get_object_or_404(Viaje, id=viaje_id, conductor=request.user)
    viaje.delete()
    return redirect('destinoConductor')

#Función que permite al conductor modificar un viaje
@login_required
def modificar_viaje(request, viaje_id):
    viaje = get_object_or_404(Viaje, id=viaje_id, conductor=request.user)
    if request.method == 'POST':
        viaje.origen = request.POST.get('origen', viaje.origen)
        viaje.destino = request.POST.get('destino', viaje.destino)
        viaje.hora = request.POST.get('hora', viaje.hora)
        viaje.cupos = request.POST.get('cupos', viaje.cupos)
        viaje.save()
        return redirect('destinoConductor')
    return render(request, 'VistaModificarViaje.html', {'viaje': viaje})

#Path que renderiza la vista de registro
def registro(request):
    return render(request, 'VistaRegistro.html')

#Path que renderiza la vista de inicio de sesión
def vista_login(request):
    return render(request, 'index.html')

#Path que renderiza la vista del home conductor
@login_required
def homeConductor(request):
    return render(request, 'VistaConductor.html')

#Path que renderiza la vista del home pasajero, además de funcionar como buscador de viajes
@login_required
def homePasajero(request):
    query = request.GET.get('q')
    error = None
    nohayviajes = None
    if query:
        viajes = Viaje.objects.filter(Q(destino__icontains=query) | Q(origen__icontains=query), activo=True)
        if not viajes:
            error = 'No se encontraron viajes'
    else:
        viajes = Viaje.objects.filter(activo=True)
        if not viajes:
            nohayviajes = 'Estamos a la espera de nuevos viajes'
    return render(request, 'VistaPasajero.html', {'viajes': viajes, 'error': error, 'nohayviajes': nohayviajes, 'usuarios': Usuario.objects.all()})

#Path que renderiza la vista de perfil de usuario conductor
@login_required
def perfil_usuario_conductor(request):
    usuario = request.user
    return render(request, 'VistaPerfilUsuarioConductor.html', {'usuario': usuario})

#Path que renderiza la vista de perfil de usuario pasajero
@login_required
def perfil_usuario_pasajero(request):
    usuario = request.user
    return render(request, 'VistaPerfilUsuarioPasajero.html', {'usuario': usuario})

#Path que renderiza la vista de perfil de vehículo
@login_required
def perfil_vehiculo(request):
    return render(request, 'VistaPerfilVehiculo.html')

#Path que renderiza la vista de destinos, además de obtener los viajes asociados a los conductores y mostrarlos
@login_required
def vista_destinos(request):
    conductor = request.user
    viajes = Viaje.objects.filter(conductor=conductor)
    nohayviajes = None  # Inicializa la variable error
    error = None
    if not viajes:
        nohayviajes = 'En este momento no tienes ningún viaje registrado'
        
    return render(request, 'VistaDestinosConductor.html', {'viajes': viajes, 'nohayviajes': nohayviajes})

#Función que permite la activación de un viaje
@csrf_exempt
@require_POST
@login_required
def activar_viaje(request, viaje_id):
    try:
        viaje = Viaje.objects.get(id=viaje_id, conductor=request.user)
        data = json.loads(request.body)
        viaje.activo = data['activo']
        viaje.save()
        return JsonResponse({'status': 'success'})
    except Viaje.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Viaje no encontrado'}, status=404)