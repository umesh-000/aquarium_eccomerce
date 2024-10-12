from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from accounts import models


# Create your views here.
def index(request):
    return redirect('login')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user already exists
        if models.User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        # Create User
        user = models.User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            user_type="admin"
        )
        # Create Admins entry
        models.Admins.objects.create(user=user)
        messages.success(request, "Registration successful!")
        return redirect('login')

    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['admin_id'] = user.id
            if user.user_type == 'admin':
                messages.success(request, "Login Successful!")
                return redirect('admin_dashboard')
            # elif user.user_type == 'customer':
            #     return redirect('customer_dashboard')
            # elif user.user_type == 'vendor':
            #     return redirect('vendor_dashboard')
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('login')

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request) 
    request.session.flush()
    return redirect('login')