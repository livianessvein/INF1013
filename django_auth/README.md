# Sistema de Autenticação Django

Sistema web completo com login e cadastro de usuários.

## Estrutura

```
django_auth/
├── manage.py
├── settings.py
├── urls.py
├── requirements.txt
├── accounts/
│   ├── models.py      # Model Usuario customizado
│   ├── views.py       # Login, cadastro, dashboard, logout
│   ├── forms.py       # Formulários com validação
│   └── admin.py       # Painel admin configurado
├── templates/
│   ├── base.html
│   └── auth/
│       ├── login.html
│       ├── cadastro.html
│       └── dashboard.html
└── static/
    └── css/
        └── style.css
```

## Modelo de dados (tabela `usuarios`)

| Campo          | Tipo            | Detalhe                   |
|----------------|-----------------|---------------------------|
| id             | AutoField (PK)  | Chave primária automática |
| email          | EmailField      | Único (UNIQUE constraint) |
| nome           | CharField(150)  | Nome completo             |
| password       | CharField       | Hash bcrypt (Django)      |
| data_cadastro  | DateTimeField   | Preenchida automaticamente|
| is_active      | BooleanField    | Conta ativa               |
| is_staff       | BooleanField    | Acesso ao admin           |

## Como rodar

### 1. Criar e ativar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Criar as migrations e o banco de dados

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### 4. (Opcional) Criar superusuário para o admin

```bash
python manage.py createsuperuser
```

### 5. Rodar o servidor

```bash
python manage.py runserver
```

## Rotas disponíveis

| URL           | Descrição                          |
|---------------|------------------------------------|
| `/login/`     | Página de login                    |
| `/cadastro/`  | Página de cadastro de novo usuário |
| `/dashboard/` | Área logada (requer autenticação)  |
| `/logout/`    | Encerra a sessão                   |
| `/admin/`     | Painel administrativo Django       |

## Segurança

- Senhas armazenadas com **hash PBKDF2** (padrão Django)
- Proteção **CSRF** em todos os formulários
- Redirecionamento automático para login em rotas protegidas
- Validação de email único no banco de dados
- Confirmação de senha no cadastro

## Produção

Antes de colocar em produção, altere no `settings.py`:

```python
SECRET_KEY = 'sua-chave-secreta-aleatoria-aqui'
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']

# Troque SQLite por PostgreSQL:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_do_banco',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
