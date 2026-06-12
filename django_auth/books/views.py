from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Livro, Estante, Avaliacao, Resenha, Comentario, Amizade, Autor, Editora
from accounts.models import Usuario
from .forms import LivroForm, EstanteForm, AvaliacaoForm, ResenhaForm, ComentarioForm, PerfilForm


@login_required
def lista_livros(request):
    query = request.GET.get('q', '')
    livros = Livro.objects.all()
    if query:
        livros = livros.filter(
            Q(titulo__icontains=query) |
            Q(isbn__icontains=query) |
            Q(autores__nome__icontains=query) |
            Q(editora__nome__icontains=query)
        ).distinct()
    return render(request, 'books/lista_livros.html', {'livros': livros, 'query': query})


@login_required
def criar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save()
            messages.success(request, f'Livro "{livro.titulo}" cadastrado com sucesso!')
            return redirect('books:detalhe_livro', livro_id=livro.id_livro)
    else:
        # Pre-create default publishers and authors if none exist
        if not Editora.objects.exists():
            Editora.objects.create(nome="Companhia das Letras")
            Editora.objects.create(nome="Rocco")
            Editora.objects.create(nome="Intrínseca")
        if not Autor.objects.exists():
            Autor.objects.create(nome="Machado de Assis", biografia="Um dos maiores escritores brasileiros.")
            Autor.objects.create(nome="J.K. Rowling", biografia="Autora de Harry Potter.")
            Autor.objects.create(nome="George Orwell", biografia="Autor de 1984.")
        form = LivroForm()
    return render(request, 'books/criar_livro.html', {'form': form})


@login_required
def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    estante_entry = Estante.objects.filter(usuario=request.user, livro=livro).first()
    avaliacao_entry = Avaliacao.objects.filter(usuario=request.user, livro=livro).first()
    resenha_entry = Resenha.objects.filter(usuario=request.user, livro=livro).first()
    
    resenhas = Resenha.objects.filter(livro=livro).order_by('-data_resenha')
    media_nota = Avaliacao.objects.filter(livro=livro).aggregate(Avg('nota'))['nota__avg']
    
    # Forms
    estante_form = EstanteForm(instance=estante_entry)
    avaliacao_form = AvaliacaoForm(instance=avaliacao_entry)
    resenha_form = ResenhaForm(instance=resenha_entry)
    
    context = {
        'livro': livro,
        'estante_entry': estante_entry,
        'avaliacao_entry': avaliacao_entry,
        'resenha_entry': resenha_entry,
        'resenhas': resenhas,
        'media_nota': media_nota,
        'estante_form': estante_form,
        'avaliacao_form': avaliacao_form,
        'resenha_form': resenha_form,
    }
    return render(request, 'books/detalhe_livro.html', context)


@login_required
def adicionar_estante(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    estante_entry = Estante.objects.filter(usuario=request.user, livro=livro).first()
    
    if request.method == 'POST':
        confirmado = request.POST.get('confirmado') == '1'
        if estante_entry and not confirmado:
            # Render a confirmation page asking if user wants to change status
            new_status = request.POST.get('status')
            new_page = request.POST.get('pagina_atual', 0)
            return render(request, 'books/confirmar_estante.html', {
                'livro': livro,
                'status_atual': estante_entry.status,
                'status_novo': new_status,
                'pagina_atual': new_page,
            })
            
        form = EstanteForm(request.POST, instance=estante_entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.usuario = request.user
            entry.livro = livro
            entry.save()
            messages.success(request, f'Estante atualizada para "{livro.titulo}"!')
            return redirect('books:detalhe_livro', livro_id=livro.id_livro)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo {field}: {error}")
    return redirect('books:detalhe_livro', livro_id=livro_id)


@login_required
def atualizar_progresso(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    estante_entry = get_object_or_404(Estante, usuario=request.user, livro=livro)
    
    if request.method == 'POST':
        pagina_atual = int(request.POST.get('pagina_atual', 0))
        if pagina_atual > livro.num_paginas:
            messages.error(request, f'Erro: a página atual não pode ser maior que o total do livro ({livro.num_paginas}).')
        else:
            estante_entry.pagina_atual = pagina_atual
            # Auto-update status to "lido" if page reaches total pages
            if pagina_atual == livro.num_paginas:
                estante_entry.status = 'lido'
            elif estante_entry.status == 'quero ler' and pagina_atual > 0:
                estante_entry.status = 'lendo'
            estante_entry.save()
            messages.success(request, 'Progresso de leitura atualizado!')
    return redirect('books:detalhe_livro', livro_id=livro.id_livro)


@login_required
def avaliar_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    
    # Rating requires the book to be in the shelf
    estante_entry = Estante.objects.filter(usuario=request.user, livro=livro).first()
    if not estante_entry:
        messages.error(request, 'Você deve adicionar o livro à sua estante antes de avaliá-lo.')
        return redirect('books:detalhe_livro', livro_id=livro_id)
        
    avaliacao_entry = Avaliacao.objects.filter(usuario=request.user, livro=livro).first()
    
    if request.method == 'POST':
        confirmado = request.POST.get('confirmado') == '1'
        nova_nota = request.POST.get('nota')
        
        if avaliacao_entry and not confirmado:
            return render(request, 'books/confirmar_avaliacao.html', {
                'livro': livro,
                'nota_atual': avaliacao_entry.nota,
                'nota_nova': nova_nota,
            })
            
        form = AvaliacaoForm(request.POST, instance=avaliacao_entry)
        if form.is_valid():
            val = form.save(commit=False)
            val.usuario = request.user
            val.livro = livro
            val.save()
            messages.success(request, 'Avaliação registrada com sucesso!')
            return redirect('books:detalhe_livro', livro_id=livro.id_livro)
            
    return redirect('books:detalhe_livro', livro_id=livro_id)


@login_required
def escrever_resenha(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    resenha_entry = Resenha.objects.filter(usuario=request.user, livro=livro).first()
    
    if request.method == 'POST':
        confirmado = request.POST.get('confirmado') == '1'
        texto = request.POST.get('texto')
        spoiler = request.POST.get('spoiler') == 'on'
        
        if not texto.strip():
            messages.error(request, 'A resenha não pode estar vazia.')
            return redirect('books:detalhe_livro', livro_id=livro_id)
            
        if resenha_entry and not confirmado:
            return render(request, 'books/confirmar_resenha.html', {
                'livro': livro,
                'texto_novo': texto,
                'spoiler_novo': spoiler,
            })
            
        form = ResenhaForm(request.POST, instance=resenha_entry)
        if form.is_valid():
            res = form.save(commit=False)
            res.usuario = request.user
            res.livro = livro
            res.save()
            messages.success(request, 'Resenha publicada com sucesso!')
            return redirect('books:detalhe_livro', livro_id=livro.id_livro)
            
    return redirect('books:detalhe_livro', livro_id=livro_id)


@login_required
def comentar_resenha(request, resenha_id):
    resenha = get_object_or_404(Resenha, pk=resenha_id)
    
    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()
        confirmado = request.POST.get('confirmado') == '1'
        
        if not texto:
            messages.error(request, 'O comentário não pode ser vazio.')
            return redirect('books:detalhe_livro', livro_id=resenha.livro.id_livro)
            
        # Check for duplicate comment in sequence
        ultimo_comentario = Comentario.objects.filter(resenha=resenha, usuario=request.user).order_by('-data_comentario').first()
        if ultimo_comentario and ultimo_comentario.texto == texto and not confirmado:
            return render(request, 'books/confirmar_comentario.html', {
                'resenha': resenha,
                'texto': texto,
            })
            
        Comentario.objects.create(
            resenha=resenha,
            usuario=request.user,
            texto=texto
        )
        messages.success(request, 'Comentário publicado!')
    return redirect('books:detalhe_livro', livro_id=resenha.livro.id_livro)


@login_required
def perfil_usuario(request, usuario_id):
    perfil = get_object_or_404(Usuario, pk=usuario_id)
    estante_itens = Estante.objects.filter(usuario=perfil).select_related('livro')
    
    # Filter shelf categories
    lendo = estante_itens.filter(status='lendo')
    lido = estante_itens.filter(status='lido')
    quero_ler = estante_itens.filter(status='quero ler')
    abandonado = estante_itens.filter(status='abandonado')
    
    # Friendship status
    solicitacao_pendente = None
    sao_amigos = False
    
    if perfil != request.user:
        amizade_sol = Amizade.objects.filter(solicitante=request.user, destinatario=perfil).first()
        amizade_dest = Amizade.objects.filter(solicitante=perfil, destinatario=request.user).first()
        
        if amizade_sol:
            if amizade_sol.status == 'aceita':
                sao_amigos = True
            else:
                solicitacao_pendente = 'enviada'
        elif amizade_dest:
            if amizade_dest.status == 'aceita':
                sao_amigos = True
            else:
                solicitacao_pendente = 'recebida'
                
    # Get friends list
    amizades_sol = Amizade.objects.filter(solicitante=perfil, status='aceita').values_list('destinatario_id', flat=True)
    amizades_dest = Amizade.objects.filter(destinatario=perfil, status='aceita').values_list('solicitante_id', flat=True)
    amigos = Usuario.objects.filter(id__in=list(amizades_sol) + list(amizades_dest))
    
    context = {
        'perfil': perfil,
        'lendo': lendo,
        'lido': lido,
        'quero_ler': quero_ler,
        'abandonado': abandonado,
        'solicitacao_pendente': solicitacao_pendente,
        'sao_amigos': sao_amigos,
        'amigos': amigos,
    }
    return render(request, 'books/perfil.html', context)


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('books:perfil_usuario', usuario_id=request.user.id)
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'books/editar_perfil.html', {'form': form})


@login_required
def solicitar_amizade(request, usuario_id):
    destinatario = get_object_or_404(Usuario, pk=usuario_id)
    
    if request.user == destinatario:
        messages.error(request, 'Você não pode enviar uma solicitação de amizade para si mesmo.')
        return redirect('books:perfil_usuario', usuario_id=usuario_id)
        
    # Check if exists
    amizade_existente = Amizade.objects.filter(
        Q(solicitante=request.user, destinatario=destinatario) |
        Q(solicitante=destinatario, destinatario=request.user)
    ).first()
    
    if amizade_existente:
        messages.info(request, 'Já existe uma solicitação ou amizade registrada.')
    else:
        Amizade.objects.create(solicitante=request.user, destinatario=destinatario, status='aguardando')
        messages.success(request, 'Convite de amizade enviado!')
        
    return redirect('books:perfil_usuario', usuario_id=usuario_id)


@login_required
def aceitar_amizade(request, amizade_id):
    amizade = get_object_or_404(Amizade, pk=amizade_id, destinatario=request.user)
    amizade.status = 'aceita'
    amizade.save()
    messages.success(request, f'Você aceitou a amizade de {amizade.solicitante.nome}!')
    return redirect('books:lista_amigos')


@login_required
def recusar_amizade(request, amizade_id):
    amizade = get_object_or_404(Amizade, pk=amizade_id, destinatario=request.user)
    amizade.status = 'recusado'
    amizade.save()
    messages.info(request, f'Você recusou a amizade de {amizade.solicitante.nome}.')
    return redirect('books:lista_amigos')


@login_required
def lista_amigos(request):
    # List accepted friends
    amizades_sol = Amizade.objects.filter(solicitante=request.user, status='aceita').values_list('destinatario_id', flat=True)
    amizades_dest = Amizade.objects.filter(destinatario=request.user, status='aceita').values_list('solicitante_id', flat=True)
    amigos = Usuario.objects.filter(id__in=list(amizades_sol) + list(amizades_dest))
    
    # List pending requests received
    solicitacoes_recebidas = Amizade.objects.filter(destinatario=request.user, status='aguardando')
    
    # List search for other users to add
    search_query = request.GET.get('search_user', '')
    outros_usuarios = []
    if search_query:
        outros_usuarios = Usuario.objects.filter(
            Q(nome__icontains=search_query) | Q(email__icontains=search_query)
        ).exclude(id=request.user.id).distinct()
        
    context = {
        'amigos': amigos,
        'solicitacoes_recebidas': solicitacoes_recebidas,
        'outros_usuarios': outros_usuarios,
        'search_query': search_query,
    }
    return render(request, 'books/amigos.html', context)
