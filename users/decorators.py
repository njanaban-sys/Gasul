from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Allow only staff/superusers. Others are redirected with an error."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('products:home')
        return view_func(request, *args, **kwargs)
    return wrapper


def regular_user_required(view_func):
    """Block staff/superusers from user-only views (cart, checkout, wishlist)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user.is_staff or request.user.is_superuser:
            messages.info(request, 'Admins manage orders from the dashboard.')
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return wrapper
