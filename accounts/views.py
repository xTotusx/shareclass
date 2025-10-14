from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile

# Home
@login_required
def home(request):
    return render(request, 'accounts/home.html')

# Perfil
@login_required
def perfil(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        selected_image = request.POST.get("profile_image")
        if selected_image:
            profile.profile_image = selected_image
            profile.save()
        return redirect("perfil")

    # Recuperamos la foto guardada
    profile_image = profile.profile_image
    return render(request, "accounts/perfil.html", {"profile_image": profile_image})

# Login y Registro juntos (auth.html)
def auth_view(request):
    error = None
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
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
                return redirect('home')
    return render(request, 'accounts/auth.html', {'error': error})

# Página pública (antes del login)
def landing(request):
    # Si el usuario ya está logueado, mándalo directo al home
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'accounts/landing.html')



# Logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('auth')


