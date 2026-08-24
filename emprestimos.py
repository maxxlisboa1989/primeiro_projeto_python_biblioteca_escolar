import os
import psycopg2
from dotenv import load_dotenv
from datetime import date, timedelta

load_dotenv()
url_do_banco = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(url_do_banco)

def configurar_banco_emprestimos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id SERIAL PRIMARY KEY,
            id_livro INTEGER NOT NULL,
            id_aluno INTEGER NOT NULL,
            data_saida TEXT NOT NULL,
            data_entrega TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

def realizar_emprestimo(id_livro, id_aluno):
    conexao = conectar()
    cursor = conexao.cursor()
    hoje = date.today()
    prazo = hoje + timedelta(days=7)
    
    # MUDANÇA: Substituímos os 4 '?' por '%s'
    cursor.execute('''
        INSERT INTO emprestimos (id_livro, id_aluno, data_saida, data_entrega) 
        VALUES (%s, %s, %s, %s)
    ''', (id_livro, id_aluno, hoje.strftime("%d/%m/%Y"), prazo.strftime("%d/%m/%Y")))
    
    conexao.commit()
    conexao.close()

def devolver_livro(id_livro):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM emprestimos WHERE id_livro = %s", (id_livro,))
    conexao.commit()
    conexao.close()

def livro_esta_emprestado(id_livro):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM emprestimos WHERE id_livro = %s", (id_livro,))
    resultado = cursor.fetchone() 
    conexao.close()
    return resultado is not None

def listar_emprestados():
    conexao = conectar()
    cursor = conexao.cursor()
    
    # Olha a mágica: O JOIN complexo funciona perfeitamente na nuvem!
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
            "serie": linha[3], 
            "data_saida": linha[4],
            "data_entrega": linha[5] 
        })
        
    return lista_formatada

# Cria a tabela de empréstimos na nuvem
configurar_banco_emprestimos()