from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Libro

def libros_home(request):
    # ===== AGREGAR LIBRO =====
    if request.method == "POST":
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
            messages.success(request, "Libro agregado correctamente.")
            return redirect('libros_home')

    # ===== BÚSQUEDA =====
    query = request.GET.get('q')
    if query:
        libros = Libro.objects.filter(titulo__icontains=query) | Libro.objects.filter(autor__icontains=query)

        # ✅ Si solo hay un resultado, redirige directo al detalle
        if libros.count() == 1:
            return redirect('libro_detalle', libro_id=libros.first().id)
    else:
        libros = Libro.objects.all()

    context = {'libros': libros, 'query': query if query else ""}
    return render(request, 'libros/libros_home.html', context)


def libro_detalle(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    return render(request, 'libros/libro_detalle.html', {'libro': libro})


def libro_editar(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == "POST":
        libro.titulo = request.POST.get("titulo")
        libro.autor = request.POST.get("autor")
        libro.descripcion = request.POST.get("descripcion")
        libro.stock = request.POST.get("stock", 0)

        if request.FILES.get("imagen"):
            libro.imagen = request.FILES["imagen"]

        libro.save()
        messages.success(request, "El libro fue actualizado correctamente.")
        return redirect('libro_detalle', libro_id=libro.id)

    context = {'libro': libro}
    return render(request, 'libros/libro_editar.html', context)
