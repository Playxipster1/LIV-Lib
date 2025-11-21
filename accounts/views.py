from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Добро пожаловать, {user.first_name}! Регистрация прошла успешно."
            )
            return redirect('home')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if form.is_valid():
                login(request, user)
                messages.success(request, 'Добро пожаловать, {user.first_name}!')
                next_page = request.GET.get("next", 'home')
                return redirect(next_page)
            else:
                messages.error(request, "Неверное имя пользователя или пароль")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы")
    return redirect('home')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        messages.success(request, "Профиль успешно обновлен!")
        return redirect('profile')
    return render(request, "accounts/profile_edit.html")
