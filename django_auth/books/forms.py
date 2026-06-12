from django import forms
from .models import Livro, Estante, Avaliacao, Resenha, Comentario, Editora, Autor
from accounts.models import Usuario


class LivroForm(forms.ModelForm):
    # Enable adding new authors or publishers easily
    class Meta:
        model = Livro
        fields = ['titulo', 'isbn', 'sinopse', 'ano_publicacao', 'num_paginas', 'capa', 'editora', 'autores']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título do livro'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'ISBN-10 ou ISBN-13'}),
            'sinopse': forms.Textarea(attrs={'placeholder': 'Resumo do livro...', 'rows': 4}),
            'ano_publicacao': forms.NumberInput(attrs={'placeholder': 'Ex: 2023'}),
            'num_paginas': forms.NumberInput(attrs={'placeholder': 'Total de páginas', 'min': 1}),
            'capa': forms.FileInput(attrs={'accept': 'image/*'}),
            'editora': forms.Select(attrs={'class': 'select-input'}),
            'autores': forms.SelectMultiple(attrs={'class': 'select-multiple-input'}),
        }


class EstanteForm(forms.ModelForm):
    class Meta:
        model = Estante
        fields = ['status', 'pagina_atual']
        widgets = {
            'status': forms.Select(attrs={'class': 'select-input'}),
            'pagina_atual': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Página atual'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pagina_atual'].required = False

    def clean_pagina_atual(self):
        pagina = self.cleaned_data.get('pagina_atual')
        return pagina if pagina is not None else 0



class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota']
        widgets = {
            'nota': forms.Select(choices=[(i, str(i)) for i in range(6)], attrs={'class': 'select-input'}),
        }


class ResenhaForm(forms.ModelForm):
    class Meta:
        model = Resenha
        fields = ['texto', 'spoiler']
        widgets = {
            'texto': forms.Textarea(attrs={'placeholder': 'Escreva sua resenha sobre o livro...', 'rows': 5}),
            'spoiler': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'placeholder': 'Escreva um comentário...', 'rows': 2}),
        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'foto_perfil', 'bio']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Seu nome'}),
            'foto_perfil': forms.FileInput(attrs={'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Fale um pouco sobre você...', 'rows': 3}),
        }
