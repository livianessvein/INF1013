from django.core.management.base import BaseCommand
from books.models import Autor, Editora, Livro


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados fictícios (Editoras, Autores e Livros) para testes.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Semeando dados fictícios...")

        # 1. Editoras
        editoras_data = [
            {"nome": "Editora Intrínseca"},
            {"nome": "Editora Rocco"},
            {"nome": "Companhia das Letras"},
            {"nome": "HarperCollins Brasil"},
            {"nome": "Grupo Editorial Record"}
        ]
        
        editoras = {}
        for ed in editoras_data:
            obj, created = Editora.objects.get_or_create(nome=ed["nome"])
            editoras[ed["nome"]] = obj
            if created:
                self.stdout.write(f"Editora criada: {ed['nome']}")

        # 2. Autores
        autores_data = [
            {"nome": "Rick Riordan"},
            {"nome": "J.K. Rowling"},
            {"nome": "J.R.R. Tolkien"},
            {"nome": "George R.R. Martin"},
            {"nome": "Machado de Assis"},
            {"nome": "Clarice Lispector"}
        ]

        autores = {}
        for aut in autores_data:
            obj, created = Autor.objects.get_or_create(nome=aut["nome"])
            autores[aut["nome"]] = obj
            if created:
                self.stdout.write(f"Autor criado: {aut['nome']}")

        # 3. Livros
        livros_data = [
            {
                "titulo": "Percy Jackson e o Ladrão de Raios",
                "isbn": "9788598078397",
                "sinopse": "Um garoto de doze anos descobre que seu pai é Poseidon, o deus do mar, e é acusado de ter roubado o raio mestre de Zeus.",
                "ano_publicacao": 2005,
                "num_paginas": 400,
                "editora": editoras["Editora Intrínseca"],
                "autores": [autores["Rick Riordan"]]
            },
            {
                "titulo": "Harry Potter e a Pedra Filosofal",
                "isbn": "9788532511010",
                "sinopse": "Harry Potter é um garoto órfão que vive infeliz com seus tios. Em seu aniversário de 11 anos, ele descobre que é um bruxo e é convidado para estudar na Escola de Magia e Bruxaria de Hogwarts.",
                "ano_publicacao": 1997,
                "num_paginas": 223,
                "editora": editoras["Editora Rocco"],
                "autores": [autores["J.K. Rowling"]]
            },
            {
                "titulo": "A Guerra dos Tronos",
                "isbn": "9788580442625",
                "sinopse": "Primeiro livro da aclamada série de fantasia Crônicas de Gelo e Fogo. Onde verões duram décadas e o inverno pode durar uma vida inteira, a luta pelo Trono de Ferro começou.",
                "ano_publicacao": 1996,
                "num_paginas": 592,
                "editora": editoras["Companhia das Letras"],
                "autores": [autores["George R.R. Martin"]]
            },
            {
                "titulo": "O Senhor dos Anéis: A Sociedade do Anel",
                "isbn": "9788595086357",
                "sinopse": "Frodo Bolseiro herda o Um Anel e precisa iniciar uma jornada perigosa para destruí-lo nas profundezas da Montanha da Perdição, evitando que caia nas mãos do Senhor Sombrio Sauron.",
                "ano_publicacao": 1954,
                "num_paginas": 424,
                "editora": editoras["HarperCollins Brasil"],
                "autores": [autores["J.R.R. Tolkien"]]
            },
            {
                "titulo": "Dom Casmurro",
                "isbn": "9788572322300",
                "sinopse": "A obra-prima de Machado de Assis conta a história de Bento Santiago (Bentinho) e seu amor de infância por Capitu, levantando a eterna dúvida da literatura brasileira: houve ou não traição?",
                "ano_publicacao": 1899,
                "num_paginas": 256,
                "editora": editoras["Companhia das Letras"],
                "autores": [autores["Machado de Assis"]]
            },
            {
                "titulo": "O Hobbit",
                "isbn": "9788595084742",
                "sinopse": "Bilbo Bolseiro é um hobbit pacato que é arrastado para uma aventura inesperada pelo mago Gandalf e um grupo de anões para recuperar um tesouro guardado pelo dragão Smaug.",
                "ano_publicacao": 1937,
                "num_paginas": 320,
                "editora": editoras["HarperCollins Brasil"],
                "autores": [autores["J.R.R. Tolkien"]]
            },
            {
                "titulo": "A Hora da Estrela",
                "isbn": "9788532512628",
                "sinopse": "O último livro escrito por Clarice Lispector apresenta a história da jovem alagoana Macabéa, uma datilógrafa órfã que vive no Rio de Janeiro e tem uma existência apagada e silenciosa.",
                "ano_publicacao": 1977,
                "num_paginas": 88,
                "editora": editoras["Grupo Editorial Record"],
                "autores": [autores["Clarice Lispector"]]
            }
        ]

        for book_info in list(livros_data):
            livro, created = Livro.objects.get_or_create(
                isbn=book_info["isbn"],
                defaults={
                    "titulo": book_info["titulo"],
                    "sinopse": book_info["sinopse"],
                    "ano_publicacao": book_info["ano_publicacao"],
                    "num_paginas": book_info["num_paginas"],
                    "editora": book_info["editora"]
                }
            )
            
            # Associe os autores
            for autor in book_info["autores"]:
                livro.autores.add(autor)
                
            if created:
                self.stdout.write(f"Livro cadastrado: {livro.titulo}")
            else:
                self.stdout.write(f"Livro já existente: {livro.titulo}")

        self.stdout.write(self.style.SUCCESS("Banco de dados populado com sucesso!"))
