from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Editora(models.Model):
    id_editora = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150, verbose_name="Nome da Editora")

    class Meta:
        verbose_name = "Editora"
        verbose_name_plural = "Editoras"
        db_table = "editoras"

    def __str__(self):
        return self.nome


class Autor(models.Model):
    id_autor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150, verbose_name="Nome do Autor")
    biografia = models.TextField(blank=True, null=True, verbose_name="Biografia")

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        db_table = "autores"

    def __str__(self):
        return self.nome


class Livro(models.Model):
    id_livro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255, verbose_name="Título")
    isbn = models.CharField(max_length=20, unique=True, verbose_name="ISBN")
    sinopse = models.TextField(verbose_name="Sinopse")
    ano_publicacao = models.IntegerField(verbose_name="Ano de Publicação")
    num_paginas = models.PositiveIntegerField(verbose_name="Número de Páginas")
    capa = models.ImageField(upload_to="capas/", null=True, blank=True, verbose_name="Capa do Livro")
    editora = models.ForeignKey(
        Editora, on_delete=models.PROTECT, related_name="livros", verbose_name="Editora"
    )
    autores = models.ManyToManyField(
        Autor, related_name="livros", verbose_name="Autores"
    )

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"
        db_table = "livros"

    @property
    def media_nota(self):
        avg = self.avaliacoes.aggregate(models.Avg('nota'))['nota__avg']
        return round(avg, 1) if avg is not None else None

    def __str__(self):
        return self.titulo


class Estante(models.Model):
    STATUS_CHOICES = [
        ("lendo", "Lendo"),
        ("lido", "Lido"),
        ("quero ler", "Quero Ler"),
        ("abandonado", "Abandonado"),
    ]

    id_estante = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="estantes",
        verbose_name="Usuário",
    )
    livro = models.ForeignKey(
        Livro, on_delete=models.CASCADE, related_name="estantes", verbose_name="Livro"
    )
    data_adicao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Adição")
    pagina_atual = models.PositiveIntegerField(default=0, verbose_name="Página Atual")
    percentual_lido = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00, verbose_name="Percentual Lido"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="quero ler", verbose_name="Status de Leitura"
    )

    class Meta:
        verbose_name = "Estante"
        verbose_name_plural = "Estantes"
        db_table = "estantes"
        unique_together = ("usuario", "livro")

    def clean(self):
        if self.pagina_atual > self.livro.num_paginas:
            raise ValidationError(
                {"pagina_atual": f"A página atual não pode ser maior que o total de páginas do livro ({self.livro.num_paginas})."}
            )

    def save(self, *args, **kwargs):
        self.clean()
        if self.status == "lido":
            self.pagina_atual = self.livro.num_paginas
        elif self.status == "quero ler":
            self.pagina_atual = 0
        
        if self.livro.num_paginas > 0:
            self.percentual_lido = round((self.pagina_atual / self.livro.num_paginas) * 100, 2)
        else:
            self.percentual_lido = 0.00
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.nome} - {self.livro.titulo} ({self.status})"


class Avaliacao(models.Model):
    id_avaliacao = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="avaliacoes",
        verbose_name="Usuário",
    )
    livro = models.ForeignKey(
        Livro, on_delete=models.CASCADE, related_name="avaliacoes", verbose_name="Livro"
    )
    data_adicao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Adição")
    nota = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Nota (0 a 5)"
    )

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        db_table = "avaliacoes"
        unique_together = ("usuario", "livro")

    def __str__(self):
        return f"{self.usuario.nome} avaliou {self.livro.titulo} com {self.nota}"


class Resenha(models.Model):
    id_resenha = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resenhas",
        verbose_name="Usuário",
    )
    livro = models.ForeignKey(
        Livro, on_delete=models.CASCADE, related_name="resenhas", verbose_name="Livro"
    )
    texto = models.TextField(verbose_name="Texto da Resenha")
    data_resenha = models.DateTimeField(auto_now_add=True, verbose_name="Data da Resenha")
    spoiler = models.BooleanField(default=False, verbose_name="Contém Spoiler")

    class Meta:
        verbose_name = "Resenha"
        verbose_name_plural = "Resenhas"
        db_table = "resenhas"
        unique_together = ("usuario", "livro")

    def __str__(self):
        return f"Resenha de {self.usuario.nome} para {self.livro.titulo}"


class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True)
    resenha = models.ForeignKey(
        Resenha, on_delete=models.CASCADE, related_name="comentarios", verbose_name="Resenha"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comentarios",
        verbose_name="Usuário",
    )
    texto = models.TextField(verbose_name="Texto do Comentário")
    data_comentario = models.DateTimeField(auto_now_add=True, verbose_name="Data do Comentário")

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        db_table = "comentarios"

    def __str__(self):
        return f"Comentário de {self.usuario.nome} na resenha {self.resenha.id_resenha}"


class Amizade(models.Model):
    STATUS_CHOICES = [
        ("aguardando", "Aguardando"),
        ("aceita", "Aceita"),
        ("recusado", "Recusado"),
    ]

    id_amizade = models.AutoField(primary_key=True)
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="solicitacoes_enviadas",
        verbose_name="Solicitante",
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="solicitacoes_recebidas",
        verbose_name="Destinatário",
    )
    data_inicio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Solicitação")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="aguardando", verbose_name="Status"
    )

    class Meta:
        verbose_name = "Amizade"
        verbose_name_plural = "Amizades"
        db_table = "amizades"
        unique_together = ("solicitante", "destinatario")

    def clean(self):
        if self.solicitante == self.destinatario:
            raise ValidationError("Você não pode enviar uma solicitação de amizade para si mesmo.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.solicitante.nome} -> {self.destinatario.nome} ({self.status})"
