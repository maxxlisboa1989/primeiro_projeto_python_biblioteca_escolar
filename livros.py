import sqlite3


# 1. Configurando o nosso "Arquivo de Aço"
def configurar_banco():
    # Cria (ou abre) o arquivo biblioteca.db na sua pasta
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()  # O cursor é o "braço" que executa nossos comandos

    # Cria a gaveta (tabela) caso ela ainda não exista
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL
        )
    ''')
    conexao.commit()  # Carimba e confirma a operação
    conexao.close()  # Fecha a conexão


# 2. A função que salva os dados lá dentro
def cadastrar_livro(titulo, autor):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    # Inserindo dados. Os '?' são escudos de segurança contra hackers!
    cursor.execute("INSERT INTO livros (titulo, autor) VALUES (?, ?)", (titulo, autor))

    conexao.commit()
    conexao.close()


# Roda a configuração assim que o módulo for chamado pelo main.py
configurar_banco()


# 4. NOVA FUNÇÃO: Pesquisar um livro específico
def pesquisar_livro(titulo_pesquisa):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    # O comando LIKE com % procura por qualquer livro que contenha aquela palavra
    cursor.execute("SELECT titulo, autor FROM livros WHERE titulo LIKE ?", ('%' + titulo_pesquisa + '%',))
    livros_encontrados = cursor.fetchall()
    conexao.close()

    lista_formatada = []
    for livro in livros_encontrados:
        lista_formatada.append({"titulo": livro[0], "autor": livro[1]})

    return lista_formatada