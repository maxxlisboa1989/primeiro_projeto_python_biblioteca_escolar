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

def pesquisar_livro(titulo_pesquisa):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    # Também pedimos o 'id' aqui
    cursor.execute("SELECT id, titulo, autor FROM livros WHERE titulo LIKE ?", ('%' + titulo_pesquisa + '%',))
    livros_encontrados = cursor.fetchall()
    conexao.close()
    
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