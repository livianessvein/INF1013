from django.contrib import admin
from .models import Autor, Editora, Livro, Estante, Avaliacao, Resenha, Comentario, Amizade


@admin.register(Editora)
class EditoraAdmin(admin.ModelAdmin):
    list_display = ('id_editora', 'nome')
    search_fields = ('nome',)


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('id_autor', 'nome')
    search_fields = ('nome',)


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('id_livro', 'titulo', 'isbn', 'ano_publicacao', 'num_paginas', 'editora')
    search_fields = ('titulo', 'isbn')
    list_filter = ('editora', 'ano_publicacao')
    filter_horizontal = ('autores',)


@admin.register(Estante)
class EstanteAdmin(admin.ModelAdmin):
    list_display = ('id_estante', 'usuario', 'livro', 'status', 'pagina_atual', 'percentual_lido', 'data_adicao')
    list_filter = ('status', 'data_adicao')
    search_fields = ('usuario__nome', 'usuario__email', 'livro__titulo')


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('id_avaliacao', 'usuario', 'livro', 'nota', 'data_adicao')
    list_filter = ('nota', 'data_adicao')
    search_fields = ('usuario__nome', 'livro__titulo')


@admin.register(Resenha)
class ResenhaAdmin(admin.ModelAdmin):
    list_display = ('id_resenha', 'usuario', 'livro', 'spoiler', 'data_resenha')
    list_filter = ('spoiler', 'data_resenha')
    search_fields = ('usuario__nome', 'livro__titulo', 'texto')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id_comentario', 'resenha', 'usuario', 'data_comentario')
    list_filter = ('data_comentario',)
    search_fields = ('usuario__nome', 'texto')


@admin.register(Amizade)
class AmizadeAdmin(admin.ModelAdmin):
    list_display = ('id_amizade', 'solicitante', 'destinatario', 'status', 'data_inicio')
    list_filter = ('status', 'data_inicio')
    search_fields = ('solicitante__nome', 'destinatario__nome')
