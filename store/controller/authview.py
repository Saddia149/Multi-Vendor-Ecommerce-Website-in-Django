from django.shortcuts import redirect, render
from django.contrib import messages
from store.forms import CustomUserForm
from django.contrib.auth import authenticate, login, logout
from store.models import CustomUser 
from django.contrib.auth import get_user_model


def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']  # Capture role (buyer/seller)
            user.save()
            messages.success(request, "Registered Successfully! Login to Continue....")
            return redirect('/login')
    context = {'form': form}
    return render(request, "store/auth/register.html", context)



def loginpage(request): 
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_superuser:  # ✅ Prevent superuser login on website
                messages.error(request, "Admin users cannot log in here!")
                return redirect('loginpage')

            login(request, user)
            messages.success(request, "Logged in Successfully")

            return redirect('/seller-dashboard/' if user.role == 'seller' else '/')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect("loginpage")

    return render(request, "store/auth/login.html")



def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect("/")
