import sqlite3

# 1. Configura o Banco
def configurar_banco():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

# 2. Salva o Livro
def cadastrar_livro(titulo, autor):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO livros (titulo, autor) VALUES (?, ?)", (titulo, autor))
    conexao.commit()
    conexao.close()

# 3. Busca os livros no Banco de Dados (A receita que estava faltando!)
def listar_livros():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT titulo, autor FROM livros")
    livros_encontrados = cursor.fetchall() 
    conexao.close()
    
    lista_formatada = []
    for livro in livros_encontrados:
        lista_formatada.append({"titulo": livro[0], "autor": livro[1]})
        
    return lista_formatada

# 4. Pesquisar um livro específico
def pesquisar_livro(titulo_pesquisa):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT titulo, autor FROM livros WHERE titulo LIKE ?", ('%' + titulo_pesquisa + '%',))
    livros_encontrados = cursor.fetchall()
    conexao.close()
    
    lista_formatada = []
    for livro in livros_encontrados:
        lista_formatada.append({"titulo": livro[0], "autor": livro[1]})
        
    return lista_formatada

# Roda a configuração
configurar_banco()