from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('livros/', views.lista_livros, name='lista_livros'),
    path('livros/novo/', views.criar_livro, name='criar_livro'),
    path('livros/<int:livro_id>/', views.detalhe_livro, name='detalhe_livro'),
    path('livros/<int:livro_id>/estante/', views.adicionar_estante, name='adicionar_estante'),
    path('livros/<int:livro_id>/atualizar-progresso/', views.atualizar_progresso, name='atualizar_progresso'),
    path('livros/<int:livro_id>/avaliar/', views.avaliar_livro, name='avaliar_livro'),
    path('livros/<int:livro_id>/resenha/', views.escrever_resenha, name='escrever_resenha'),
    path('resenhas/<int:resenha_id>/comentar/', views.comentar_resenha, name='comentar_resenha'),
    path('perfil/<int:usuario_id>/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('amizade/solicitar/<int:usuario_id>/', views.solicitar_amizade, name='solicitar_amizade'),
    path('amizade/aceitar/<int:amizade_id>/', views.aceitar_amizade, name='aceitar_amizade'),
    path('amizade/recusar/<int:amizade_id>/', views.recusar_amizade, name='recusar_amizade'),
    path('amigos/', views.lista_amigos, name='lista_amigos'),
]
