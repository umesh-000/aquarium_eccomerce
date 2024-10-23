from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils import timezone
from accounts import models


# Create your views here.
def index(request):
    return redirect('site_home')

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

def customer_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        # Check if user already exists
        if models.User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('customer_register')

        # Create User as Customer
        user = models.User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            user_type="customer"
        )

        # Create Customer Profile
        models.Customer.objects.create(
            user=user,
            phone_number=phone_number,
            status=1,
            create_at=timezone.now(),
            update_at=timezone.now()
        )

        messages.success(request, "Registration successful!")
        return redirect('login')

    return render(request, 'accounts/customer_register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.user_type == 'admin':
                request.session['admin_id'] = user.id
                messages.success(request, "Login Successful!")
                return redirect('admin_dashboard')
            elif user.user_type == 'customer':
                messages.success(request, "Login Successful!")
                return redirect('site_home')
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('login')

    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request) 
    request.session.flush()
    return redirect('login')