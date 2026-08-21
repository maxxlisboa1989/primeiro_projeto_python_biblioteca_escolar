import sqlite3

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

def cadastrar_livro(titulo, autor):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO livros (titulo, autor) VALUES (?, ?)", (titulo, autor))
    conexao.commit()
    conexao.close()

def listar_livros():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    
    # ATENÇÃO: Agora pedimos o 'id' junto com o titulo e o autor
    cursor.execute("SELECT id, titulo, autor FROM livros")
    livros_encontrados = cursor.fetchall() 
    conexao.close()
    
    lista_formatada = []
    for livro in livros_encontrados:
        # livro[0] agora é o id, livro[1] é o titulo, livro[2] é o autor
        lista_formatada.append({"id": livro[0], "titulo": livro[1], "autor": livro[2]})
        
    return lista_formatada

# 4. Pesquisar um livro específico (Por Título OU Autor)
def pesquisar_livro(termo_pesquisa):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    
    # Colocamos o % antes e depois para achar a palavra em qualquer parte do texto
    busca = '%' + termo_pesquisa + '%'
    
    # Usamos o OR para buscar nas duas colunas. 
    # Como temos dois '?', precisamos passar a 'busca' duas vezes no final!
    cursor.execute("SELECT id, titulo, autor FROM livros WHERE titulo LIKE ? OR autor LIKE ?", (busca, busca))
    
    livros_encontrados = cursor.fetchall()
    conexao.close()
    
    lista_formatada = []
    for livro in livros_encontrados:
        lista_formatada.append({"id": livro[0], "titulo": livro[1], "autor": livro[2]})
        
    return lista_formatada
    
    lista_formatada = []
    for livro in livros_encontrados:
        lista_formatada.append({"id": livro[0], "titulo": livro[1], "autor": livro[2]})
        
    return lista_formatada

# ==========================================
# AS DUAS NOVAS RECEITAS DA COZINHA (UPDATE E DELETE)
# ==========================================

# 5. Editar (Update)
def editar_livro(id_livro, novo_titulo, novo_autor):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE livros SET titulo = ?, autor = ? WHERE id = ?", (novo_titulo, novo_autor, id_livro))
    conexao.commit()
    conexao.close()

# 6. Excluir (Delete)
def excluir_livro(id_livro):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM livros WHERE id = ?", (id_livro,))
    conexao.commit()
    conexao.close()

configurar_banco()