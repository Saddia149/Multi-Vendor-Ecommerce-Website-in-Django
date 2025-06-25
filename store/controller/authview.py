from django.shortcuts import render, redirect
from django.contrib import messages
from store.forms import CustomUserForm
from django.contrib.auth import authenticate, login, logout
from store.models import CustomUser


def register(request):
    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            messages.success(request, "Registered Successfully! Login to Continue.")
            return redirect('loginpage')

    return render(request, "store/auth/register.html", {'form': form})


def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_superuser:
                messages.error(request, "Admin users cannot log in here!")
                return redirect('loginpage')

            login(request, user)
            messages.success(request, "Logged in Successfully!")

            if user.role == "seller":
                return redirect("seller_home")
            elif user.role == "buyer":
                return redirect("home")
            elif user.role == "admin":
                return redirect("admin_dashboard")
            else:
                return redirect("/")
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect("loginpage")

    return render(request, "store/auth/login.html")


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully!")
    return redirect("home")
