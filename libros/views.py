from django.shortcuts import render, redirect
from .models import Libro

def libros_home(request):
    # ===== AGREGAR LIBRO =====
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        autor = request.POST.get("autor")
        imagen = request.FILES.get("imagen")  # Opcional

        if titulo and autor:
            libro = Libro(titulo=titulo, autor=autor)
            if imagen:
                libro.imagen = imagen
            libro.save()
            return redirect('libros_home')  # Evita reenvío de formulario

    # ===== BÚSQUEDA =====
    query = request.GET.get('q')
    if query:
        libros = Libro.objects.filter(titulo__icontains=query) | Libro.objects.filter(autor__icontains=query)
    else:
        libros = Libro.objects.all()

    context = {
        'libros': libros,
        'query': query if query else ""
    }
    return render(request, 'libros/libros_home.html', context)
