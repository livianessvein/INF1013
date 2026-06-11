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
    from books.models import Amizade, Estante, Resenha
    from django.db.models import Q

    # Get friends IDs
    amizades_sol = Amizade.objects.filter(solicitante=request.user, status='aceita').values_list('destinatario_id', flat=True)
    amizades_dest = Amizade.objects.filter(destinatario=request.user, status='aceita').values_list('solicitante_id', flat=True)
    amigos_ids = list(amizades_sol) + list(amizades_dest)

    # Get recent reviews from user and their friends
    feed_resenhas = Resenha.objects.filter(
        Q(usuario=request.user) | Q(usuario_id__in=amigos_ids)
    ).select_related('usuario', 'livro').order_by('-data_resenha')[:10]

    # Get user's active reading shelf
    lendo = Estante.objects.filter(usuario=request.user, status='lendo').select_related('livro')

    # Get reading counts
    stats = {
        'lendo': Estante.objects.filter(usuario=request.user, status='lendo').count(),
        'lido': Estante.objects.filter(usuario=request.user, status='lido').count(),
        'quero_ler': Estante.objects.filter(usuario=request.user, status='quero ler').count(),
        'abandonado': Estante.objects.filter(usuario=request.user, status='abandonado').count(),
    }

    context = {
        'usuario': request.user,
        'feed_resenhas': feed_resenhas,
        'lendo': lendo,
        'stats': stats,
    }
    return render(request, 'auth/dashboard.html', context)


def run_migrations_view(request):
    from django.core.management import call_command
    from django.http import HttpResponse
    try:
        call_command('makemigrations')
        call_command('migrate')
        return HttpResponse("Migrations successfully run!")
    except Exception as e:
        return HttpResponse(f"Error running migrations: {str(e)}")


def seed_data_view(request):
    from django.core.management import call_command
    from django.http import HttpResponse
    try:
        call_command('seed_data')
        return HttpResponse("Database successfully seeded with books!")
    except Exception as e:
        return HttpResponse(f"Error seeding database: {str(e)}")

