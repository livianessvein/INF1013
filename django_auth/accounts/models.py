from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, password=None):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        usuario = self.model(email=email, nome=nome)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nome, password=None):
        usuario = self.create_user(email, nome, password)
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, verbose_name='E-mail')
    nome = models.CharField(max_length=150, verbose_name='Nome completo')
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True, verbose_name='Foto de perfil')
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name='Bio')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'usuarios'

    def __str__(self):
        return f'{self.nome} <{self.email}>'
