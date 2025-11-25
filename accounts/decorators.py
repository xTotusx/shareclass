from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.profile.role != "admin":
            messages.error(request, "No tienes permiso para entrar aquí.")
            return redirect("home")
            
        return view_func(request, *args, **kwargs)
    return wrapper
