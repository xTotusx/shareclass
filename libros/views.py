from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Libro

# Helper para verificar admin (mismo criterio que en accounts)
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
        # Si solo hay uno, vamos directo al detalle
        if libros.count() == 1:
            return redirect('libro_detalle', libro_id=libros.first().id)
    else:
        libros = Libro.objects.all().order_by('-id') # Los más nuevos primero

    context = {
        'libros': libros, 
        'query': query if query else "",
        'is_admin': is_admin(request.user) # Pasamos el booleano al template
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
    # Protección de ruta
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
    # Protección de ruta
    if not is_admin(request.user):
        return redirect('libros_home')
        
    libro = get_object_or_404(Libro, id=libro_id)
    libro.delete()
    messages.success(request, "Libro eliminado del inventario.")
    return redirect('libros_home')