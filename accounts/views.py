from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseServerError
from .models import Profile

# ====== HOME ======
@login_required
def home(request):
    try:
        # HAPPY PATH: usuario autenticado y carga correcta
        return render(request, 'accounts/home.html')
    except Exception as e:
        # UNHAPPY PATH: error inesperado
        print(f"Error en home: {e}")
        return render(request, 'accounts/error.html', {'message': 'Ocurrió un problema al cargar el inicio.'})


# ====== PERFIL ======
@login_required
def perfil(request):
    try:
        profile = Profile.objects.get(user=request.user)  # Happy path

        if request.method == "POST":
            selected_image = request.POST.get("profile_image")
            if selected_image:
                profile.profile_image = selected_image
                profile.save()
            return redirect("perfil")

        profile_image = profile.profile_image
        return render(request, "accounts/perfil.html", {"profile_image": profile_image})

    except Profile.DoesNotExist:
        # Unhappy Path: no existe el perfil
        return render(request, "accounts/error.html", {
            "message": "No se encontró tu perfil. Por favor, contacta al administrador."
        })
    except Exception as e:
        print(f"Error en perfil: {e}")
        return render(request, "accounts/error.html", {"message": "Error al cargar el perfil."})


# ====== LOGIN Y REGISTRO ======
def auth_view(request):
    error = None
    success = None  # Indicador de Happy Path

    try:
        if request.method == 'POST':
            if 'login' in request.POST:
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)

                if user:
                    login(request, user)
                    success = f"¡Bienvenido {user.username}!"
                    return redirect('home')
                else:
                    error = 'Usuario o contraseña incorrectos'

            elif 'register' in request.POST:
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password']

                if User.objects.filter(username=username).exists():
                    error = 'El usuario ya existe'
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    login(request, user)
                    success = "Registro exitoso"
                    return redirect('home')

    except Exception as e:
        print(f"Error en auth_view: {e}")
        error = 'Ocurrió un error inesperado, por favor intenta nuevamente.'

    return render(request, 'accounts/auth.html', {'error': error, 'success': success})


# ====== LANDING (PÚBLICA) ======
def landing(request):
    try:
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'accounts/landing.html')
    except Exception as e:
        print(f"Error en landing: {e}")
        return render(request, 'accounts/error.html', {'message': 'No se pudo cargar la página principal.'})


# ====== LOGOUT ======
@login_required
def logout_view(request):
    try:
        logout(request)
        return redirect('auth')
    except Exception as e:
        print(f"Error en logout: {e}")
        return render(request, 'accounts/error.html', {'message': 'Error al cerrar sesión.'})


# ====== MANEJO DE ERRORES ======
def error_404(request, exception):
    return render(request, 'accounts/error.html', {'message': 'Página no encontrada (404).'}, status=404)

def error_500(request):
    return render(request, 'accounts/error.html', {'message': 'Error interno del servidor (500).'}, status=500)
