from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Dispositivo

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