from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone # Importante para fechas
from .models import Dispositivo, PrestamoDispositivo # Importamos el nuevo modelo

# Helper para admin
def is_admin(user):
    try:
        if user.is_superuser: return True
        return user.profile.role == 'admin'
    except:
        return False

@login_required(login_url='auth')
def dispositivos_home(request):
    # ===== AGREGAR DISPOSITIVO (SOLO ADMIN) =====
    if request.method == "POST":
        if not is_admin(request.user):
            return HttpResponseForbidden("No tienes permisos.")

        nombre = request.POST.get("nombre")
        marca = request.POST.get("marca")
        descripcion = request.POST.get("descripcion")
        stock = request.POST.get("stock", 0)
        imagen = request.FILES.get("imagen")

        if nombre and marca:
            disp = Dispositivo(nombre=nombre, marca=marca, descripcion=descripcion, stock=stock)
            if imagen:
                disp.imagen = imagen
            disp.save()
            messages.success(request, "Dispositivo agregado.")
            return redirect('dispositivos_home')

    # ===== BÚSQUEDA =====
    query = request.GET.get('q')
    if query:
        dispositivos = Dispositivo.objects.filter(nombre__icontains=query) | Dispositivo.objects.filter(marca__icontains=query)
        if dispositivos.count() == 1:
            return redirect('dispositivo_detalle', dispositivo_id=dispositivos.first().id)
    else:
        dispositivos = Dispositivo.objects.all().order_by('-id')

    context = {
        'dispositivos': dispositivos,
        'query': query if query else "",
        'is_admin': is_admin(request.user)
    }
    return render(request, 'dispositivos/dispositivos_home.html', context)


@login_required(login_url='auth')
def dispositivo_detalle(request, dispositivo_id):
    dispositivo = get_object_or_404(Dispositivo, id=dispositivo_id)
    return render(request, 'dispositivos/dispositivo_detalle.html', {
        'dispositivo': dispositivo,
        'is_admin': is_admin(request.user)
    })


@login_required(login_url='auth')
def dispositivo_editar(request, dispositivo_id):
    if not is_admin(request.user):
        return redirect('dispositivos_home')

    dispositivo = get_object_or_404(Dispositivo, id=dispositivo_id)

    if request.method == "POST":
        dispositivo.nombre = request.POST.get("nombre")
        dispositivo.marca = request.POST.get("marca")
        dispositivo.descripcion = request.POST.get("descripcion")
        dispositivo.stock = request.POST.get("stock", 0)

        if request.FILES.get("imagen"):
            dispositivo.imagen = request.FILES["imagen"]

        dispositivo.save()
        messages.success(request, "Dispositivo actualizado.")
        return redirect('dispositivo_detalle', dispositivo_id=dispositivo.id)

    context = {'dispositivo': dispositivo}
    return render(request, 'dispositivos/dispositivo_editar.html', context)


@login_required(login_url='auth')
def dispositivo_eliminar(request, dispositivo_id):
    if not is_admin(request.user):
        return redirect('dispositivos_home')
        
    dispositivo = get_object_or_404(Dispositivo, id=dispositivo_id)
    dispositivo.delete()
    messages.success(request, "Dispositivo eliminado.")
    return redirect('dispositivos_home')


# ==========================================
# NUEVAS VISTAS: PRÉSTAMOS DE EQUIPOS
# ==========================================

@login_required(login_url='auth')
def prestar_dispositivo(request, dispositivo_id):
    equipo = get_object_or_404(Dispositivo, id=dispositivo_id)
    
    if equipo.stock > 0:
        # Crear préstamo
        PrestamoDispositivo.objects.create(dispositivo=equipo, usuario=request.user)
        
        # Actualizar stock
        equipo.stock -= 1
        equipo.save()
        
        messages.success(request, f"Has tomado el equipo '{equipo.nombre}'.")
    else:
        messages.error(request, "Equipo no disponible por el momento.")
        
    return redirect('dispositivo_detalle', dispositivo_id=equipo.id)


@login_required(login_url='auth')
def devolver_dispositivo(request, prestamo_id):
    # Buscar el préstamo activo
    prestamo = get_object_or_404(PrestamoDispositivo, id=prestamo_id, devuelto=False)
    
    # Validar que sea el dueño o un admin
    if prestamo.usuario != request.user and not is_admin(request.user):
        messages.error(request, "Acción no permitida.")
        return redirect('dispositivo_detalle', dispositivo_id=prestamo.dispositivo.id)

    # Devolver
    prestamo.devuelto = True
    prestamo.fecha_devolucion = timezone.now()
    prestamo.save()
    
    # Reponer stock
    equipo = prestamo.dispositivo
    equipo.stock += 1
    equipo.save()
    
    messages.success(request, f"Equipo '{equipo.nombre}' devuelto correctamente.")
    return redirect('dispositivo_detalle', dispositivo_id=equipo.id)