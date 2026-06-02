from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CadastroForm, LoginForm


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.get_usuario()
        login(request, usuario)
        messages.success(request, f'Bem-vindo(a), {usuario.nome}!')
        return redirect('dashboard')

    return render(request, 'auth/login.html', {'form': form})


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = CadastroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        login(request, usuario)
        messages.success(request, f'Conta criada com sucesso! Bem-vindo(a), {usuario.nome}!')
        return redirect('dashboard')

    return render(request, 'auth/cadastro.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('login')


@login_required
def dashboard_view(request):
    return render(request, 'auth/dashboard.html', {'usuario': request.user})
