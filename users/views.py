from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def _role_redirect(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('dashboard:home')
    return redirect('products:home')


def register_view(request):
    if request.user.is_authenticated:
        return _role_redirect(request)
    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password  = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif password != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, f'Welcome, {username}! Account created.')
            return redirect('products:home')
    return render(request, 'users/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return _role_redirect(request)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('dashboard:home')
            return redirect(request.GET.get('next', 'products:home'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('users:login')
