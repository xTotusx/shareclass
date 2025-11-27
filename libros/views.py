from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone # Importante para la fecha de devolución
from .models import Libro, Prestamo # Agregamos Prestamo

# Helper para verificar admin
def is_admin(user):
    try:
        if user.is_superuser: return True
        return user.profile.role == 'admin'
    except:
        return False

@login_required(login_url='auth')
def libros_home(request):
    # ===== AGREGAR LIBRO (SOLO ADMIN) =====
    if request.method == "POST":
        if not is_admin(request.user):
            return HttpResponseForbidden("No tienes permisos para agregar libros.")

        titulo = request.POST.get("titulo")
        autor = request.POST.get("autor")
        descripcion = request.POST.get("descripcion")
        stock = request.POST.get("stock", 0)
        imagen = request.FILES.get("imagen")

        if titulo and autor:
            libro = Libro(titulo=titulo, autor=autor, descripcion=descripcion, stock=stock)
            if imagen:
                libro.imagen = imagen
            libro.save()
            messages.success(request, "Libro agregado al inventario.")
            return redirect('libros_home')

    # ===== BÚSQUEDA =====
    query = request.GET.get('q')
    if query:
        libros = Libro.objects.filter(titulo__icontains=query) | Libro.objects.filter(autor__icontains=query)
        if libros.count() == 1:
            return redirect('libro_detalle', libro_id=libros.first().id)
    else:
        libros = Libro.objects.all().order_by('-id')

    context = {
        'libros': libros, 
        'query': query if query else "",
        'is_admin': is_admin(request.user)
    }
    return render(request, 'libros/libros_home.html', context)


@login_required(login_url='auth')
def libro_detalle(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    return render(request, 'libros/libro_detalle.html', {
        'libro': libro,
        'is_admin': is_admin(request.user)
    })


@login_required(login_url='auth')
def libro_editar(request, libro_id):
    if not is_admin(request.user):
        return redirect('libros_home')

    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == "POST":
        libro.titulo = request.POST.get("titulo")
        libro.autor = request.POST.get("autor")
        libro.descripcion = request.POST.get("descripcion")
        libro.stock = request.POST.get("stock", 0)

        if request.FILES.get("imagen"):
            libro.imagen = request.FILES["imagen"]

        libro.save()
        messages.success(request, "Libro actualizado correctamente.")
        return redirect('libro_detalle', libro_id=libro.id)

    context = {'libro': libro}
    return render(request, 'libros/libro_editar.html', context)


@login_required(login_url='auth')
def libro_eliminar(request, libro_id):
    if not is_admin(request.user):
        return redirect('libros_home')
        
    libro = get_object_or_404(Libro, id=libro_id)
    libro.delete()
    messages.success(request, "Libro eliminado del inventario.")
    return redirect('libros_home')


# ==========================================
# NUEVAS VISTAS DE PRÉSTAMOS
# ==========================================

@login_required(login_url='auth')
def prestar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    # 1. Verificar si hay stock
    if libro.stock > 0:
        # 2. Crear registro de préstamo
        Prestamo.objects.create(libro=libro, usuario=request.user)
        
        # 3. Restar del inventario
        libro.stock -= 1
        libro.save()
        
        messages.success(request, f"Has tomado prestado '{libro.titulo}'.")
    else:
        messages.error(request, "Lo sentimos, este libro está agotado temporalmente.")
        
    return redirect('libro_detalle', libro_id=libro.id)


@login_required(login_url='auth')
def devolver_libro(request, prestamo_id):
    # Buscamos el préstamo específico que NO ha sido devuelto aún
    prestamo = get_object_or_404(Prestamo, id=prestamo_id, devuelto=False)
    
    # Seguridad: Solo el dueño o un admin pueden devolverlo
    if prestamo.usuario != request.user and not is_admin(request.user):
        messages.error(request, "No puedes devolver un libro que no tienes.")
        return redirect('libro_detalle', libro_id=prestamo.libro.id)

    # 1. Marcar como devuelto
    prestamo.devuelto = True
    prestamo.fecha_devolucion = timezone.now()
    prestamo.save()
    
    # 2. Sumar al inventario
    libro = prestamo.libro
    libro.stock += 1
    libro.save()
    
    messages.success(request, f"Has devuelto '{libro.titulo}'. ¡Gracias!")
    return redirect('libro_detalle', libro_id=libro.id)