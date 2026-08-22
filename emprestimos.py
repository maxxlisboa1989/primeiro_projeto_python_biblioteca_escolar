import sqlite3
from datetime import date, timedelta

def configurar_banco_emprestimos():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    
    # MÁGICA: Apaga SOMENTE a gaveta de empréstimos antiga para criar a nova!
    cursor.execute("DROP TABLE IF EXISTS emprestimos")
    
    # Cria a nova tabela usando id_aluno ao invés de nome_aluno
    cursor.execute('''
        CREATE TABLE emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER NOT NULL,
            id_aluno INTEGER NOT NULL,
            data_saida TEXT NOT NULL,
            data_entrega TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

def realizar_emprestimo(id_livro, id_aluno):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    hoje = date.today()
    prazo = hoje + timedelta(days=7)
    
    cursor.execute('''
        INSERT INTO emprestimos (id_livro, id_aluno, data_saida, data_entrega) 
        VALUES (?, ?, ?, ?)
    ''', (id_livro, id_aluno, hoje.strftime("%d/%m/%Y"), prazo.strftime("%d/%m/%Y")))
    
    conexao.commit()
    conexao.close()

def devolver_livro(id_livro):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM emprestimos WHERE id_livro = ?", (id_livro,))
    conexao.commit()
    conexao.close()

def livro_esta_emprestado(id_livro):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM emprestimos WHERE id_livro = ?", (id_livro,))
    resultado = cursor.fetchone() 
    conexao.close()
    return resultado is not None

def listar_emprestados():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    
    # O DUPLO JOIN: Junta Empréstimos + Livros + Alunos de uma vez só!
    cursor.execute('''
        SELECT emprestimos.id_livro, livros.titulo, alunos.nome, alunos.serie, 
               emprestimos.data_saida, emprestimos.data_entrega
        FROM emprestimos
        JOIN livros ON emprestimos.id_livro = livros.id
        JOIN alunos ON emprestimos.id_aluno = alunos.id
    ''')
    
    resultados = cursor.fetchall()
    conexao.close()
    
    lista_formatada = []
    for linha in resultados:
        lista_formatada.append({
            "id_livro": linha[0], 
            "titulo": linha[1], 
            "aluno": linha[2],
            "serie": linha[3], # Agora a série vem direto do banco!
            "data_saida": linha[4],
            "data_entrega": linha[5] 
        })
        
    return lista_formatada

configurar_banco_emprestimos()