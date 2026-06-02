from django import forms
from django.contrib.auth import authenticate
from .models import Usuario


class CadastroForm(forms.ModelForm):
    senha = forms.CharField(
        label='Senha',
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 6 caracteres'}),
    )
    confirmar_senha = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha'}),
    )

    class Meta:
        model = Usuario
        fields = ['nome', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
            'email': forms.EmailInput(attrs={'placeholder': 'seu@email.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar = cleaned_data.get('confirmar_senha')
        if senha and confirmar and senha != confirmar:
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['senha'])
        if commit:
            usuario.save()
        return usuario


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com'}),
    )
    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Sua senha'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '').lower()
        senha = cleaned_data.get('senha')
        if email and senha:
            self.usuario = authenticate(username=email, password=senha)
            if self.usuario is None:
                raise forms.ValidationError('E-mail ou senha incorretos.')
            if not self.usuario.is_active:
                raise forms.ValidationError('Esta conta está desativada.')
        return cleaned_data

    def get_usuario(self):
        return getattr(self, 'usuario', None)
