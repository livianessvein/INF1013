from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('id', 'nome', 'email', 'data_cadastro', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'data_cadastro')
    search_fields = ('nome', 'email')
    ordering = ('-data_cadastro',)
    readonly_fields = ('data_cadastro',)

    fieldsets = (
        ('Dados pessoais', {'fields': ('nome', 'email', 'password')}),
        ('Informações', {'fields': ('data_cadastro',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nome', 'email', 'password1', 'password2'),
        }),
    )
