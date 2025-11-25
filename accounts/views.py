from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Profile

# Importamos los modelos de las otras apps para el Dashboard
# Usamos try/except por si alguna app aún no tiene migraciones, para que no rompa todo.
try:
    from libros.models import Libro
except ImportError:
    Libro = None

try:
    from dispositivos.models import Dispositivo
except ImportError:
    Dispositivo = None


# =====================================================
#  HELPER: VERIFICAR SI ES ADMIN
# =====================================================
def is_admin(user):
    """
    Devuelve True si es Superusuario (Django) o Admin (Perfil).
    """
    if not user.is_authenticated:
        return False
    
    try:
        # Si es superusuario de terminal, pase directo
        if user.is_superuser:
            return True
        # Si tiene rol 'admin' en su perfil
        return user.profile.role == "admin"
    except:
        # Si falla algo (ej. no tiene perfil), nos fiamos del superuser
        return user.is_superuser


# =====================================================
#  VISTAS PÚBLICAS Y DE NAVEGACIÓN
# =====================================================

def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'accounts/landing.html')


@login_required
def home(request):
    return render(request, 'accounts/home.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('auth')


# =====================================================
#  PERFIL DE USUARIO
# =====================================================

@login_required
def perfil(request):
    try:
        profile = request.user.profile
        
        if request.method == "POST":
            # Guardar el avatar seleccionado
            selected_image = request.POST.get("profile_image")
            if selected_image:
                profile.profile_image = selected_image
                profile.save()
            return redirect("perfil")

        return render(request, "accounts/perfil.html", {
            "profile": profile,
            # Pasamos profile_image por si se usa directo en el template antiguo
            "profile_image": profile.profile_image 
        })
    except Exception as e:
        print(f"Error en perfil: {e}")
        return redirect('home')


# =====================================================
#  AUTENTICACIÓN (LOGIN / REGISTRO)
# =====================================================

def auth_view(request):
    # Si ya está dentro, mandar al home
    if request.user.is_authenticated:
        return redirect('home')

    error = None

    if request.method == 'POST':
        
        # --- LOGIN ---
        if 'login' in request.POST:
            u = request.POST.get('username')
            p = request.POST.get('password')
            user = authenticate(request, username=u, password=p)
            
            if user:
                login(request, user)
                return redirect('home')
            else:
                error = 'Usuario o contraseña incorrectos.'

        # --- REGISTRO ---
        elif 'register' in request.POST:
            u = request.POST.get('username')
            e = request.POST.get('email')
            p = request.POST.get('password')

            # Validaciones básicas
            if not u or not p:
                error = "Usuario y contraseña son obligatorios."
            
            elif User.objects.filter(username=u).exists():
                error = 'El usuario ya existe. Prueba otro nombre.'
            
            else:
                try:
                    # 1. Crear usuario (Signal crea el perfil auto)
                    user = User.objects.create_user(username=u, email=e, password=p)
                    
                    # 2. Auto-Login inmediato
                    # Especificamos el backend para que no pida autenticar de nuevo
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    
                    return redirect('home')
                    
                except Exception as ex:
                    print(f"Error registro: {ex}")
                    error = "Ocurrió un error. Intenta de nuevo."

    return render(request, 'accounts/auth.html', {'error': error})


# =====================================================
#  PANEL DE ADMINISTRACIÓN (PROTEGIDO)
# =====================================================

@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        return redirect('home')

    # Contadores
    total_users = User.objects.count()
    total_admins = Profile.objects.filter(role='admin').count()
    
    # Stock de libros
    total_libros = Libro.objects.count() if Libro else 0
    
    # Stock de dispositivos
    total_dispositivos = Dispositivo.objects.count() if Dispositivo else 0

    context = {
        'total_users': total_users,
        'total_admins': total_admins,
        'total_libros': total_libros,
        'total_dispositivos': total_dispositivos,
    }
    return render(request, "accounts/admin_dashboard.html", context)


@login_required
def user_list(request):
    if not is_admin(request.user):
        return redirect('home')

    # Traemos usuarios + perfil optimizado
    users = User.objects.select_related('profile').all().order_by('id')

    return render(request, 'accounts/user_list.html', {
        "users": users
    })


@login_required
def change_role(request, user_id):
    if not is_admin(request.user):
        return HttpResponseForbidden("No autorizado")
    
    # Evitar quitarse admin a uno mismo
    if request.user.id == user_id:
        return redirect('user_list')

    try:
        user_obj = User.objects.get(id=user_id)
        # Toggle: si es admin -> alumno, si es alumno -> admin
        new_role = 'alumno' if user_obj.profile.role == 'admin' else 'admin'
        user_obj.profile.role = new_role
        user_obj.profile.save()
    except User.DoesNotExist:
        pass
        
    return redirect("user_list")


@login_required
def delete_user(request, user_id):
    if not is_admin(request.user):
        return HttpResponseForbidden("No autorizado")

    # Seguridad: No auto-eliminarse
    if request.user.id == user_id:
        return redirect('user_list')

    try:
        User.objects.get(id=user_id).delete()
    except:
        pass

    return redirect("user_list")