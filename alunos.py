import os
import psycopg2
from dotenv import load_dotenv

# 1. Abre o cofre e pega a URL da nuvem
load_dotenv()
url_do_banco = os.getenv("DATABASE_URL")

# Função auxiliar para não termos que digitar a conexão toda hora
def conectar():
    return psycopg2.connect(url_do_banco)

def configurar_banco_alunos():
    conexao = conectar()
    cursor = conexao.cursor()
    # MUDANÇA NO SOTAQUE: Usamos SERIAL no lugar de AUTOINCREMENT
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            serie TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

def cadastrar_aluno(nome, serie):
    conexao = conectar()
    cursor = conexao.cursor()
    # MUDANÇA NO SOTAQUE: Trocamos o '?' por '%s'
    cursor.execute("INSERT INTO alunos (nome, serie) VALUES (%s, %s)", (nome, serie))
    conexao.commit()
    conexao.close()

def listar_alunos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, serie FROM alunos ORDER BY id")
    resultados = cursor.fetchall()
    conexao.close()
    
    lista = []
    for linha in resultados:
        lista.append({"id": linha[0], "nome": linha[1], "serie": linha[2]})
        
    return lista

# Roda a configuração toda vez que o arquivo é chamado
configurar_banco_alunos()