import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
url_do_banco = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(url_do_banco)

def configurar_banco_livros():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

def cadastrar_livro(titulo, autor):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO livros (titulo, autor) VALUES (%s, %s)", (titulo, autor))
    conexao.commit()
    conexao.close()

def listar_livros():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, titulo, autor FROM livros ORDER BY id")
    resultados = cursor.fetchall()
    conexao.close()
    
    lista = []
    for linha in resultados:
        lista.append({"id": linha[0], "titulo": linha[1], "autor": linha[2]})
    return lista

def pesquisar_livro(termo):
    conexao = conectar()
    cursor = conexao.cursor()
    termo_busca = f"%{termo}%"
    # O ILIKE é o segredo do Postgres para ignorar maiúsculas/minúsculas!
    cursor.execute("SELECT id, titulo, autor FROM livros WHERE titulo ILIKE %s OR autor ILIKE %s", (termo_busca, termo_busca))
    resultados = cursor.fetchall()
    conexao.close()
    
    lista = []
    for linha in resultados:
        lista.append({"id": linha[0], "titulo": linha[1], "autor": linha[2]})
    return lista

def editar_livro(id_livro, novo_titulo, novo_autor):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE livros SET titulo = %s, autor = %s WHERE id = %s", (novo_titulo, novo_autor, id_livro))
    conexao.commit()
    conexao.close()

def excluir_livro(id_livro):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM livros WHERE id = %s", (id_livro,))
    conexao.commit()
    conexao.close()

configurar_banco_livros()