import sqlite3

# 1. Configura a nova "gaveta" de alunos
def configurar_banco_alunos():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            serie TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

# 2. Cadastra o aluno e a série
def cadastrar_aluno(nome, serie):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO alunos (nome, serie) VALUES (?, ?)", (nome, serie))
    conexao.commit()
    conexao.close()

# 3. Lista todos os alunos
def listar_alunos():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, serie FROM alunos")
    resultados = cursor.fetchall()
    conexao.close()
    
    lista = []
    for linha in resultados:
        lista.append({"id": linha[0], "nome": linha[1], "serie": linha[2]})
        
    return lista

# Roda a configuração para criar a tabela no banco
configurar_banco_alunos()