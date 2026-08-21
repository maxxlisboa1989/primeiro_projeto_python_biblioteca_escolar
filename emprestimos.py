import sqlite3
from datetime import date, timedelta  # Ferramentas de tempo do Python!

def configurar_banco_emprestimos():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    
    # ATUALIZADO: Adicionamos as colunas de data_saida e data_entrega
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER NOT NULL,
            nome_aluno TEXT NOT NULL,
            data_saida TEXT NOT NULL,
            data_entrega TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

def realizar_emprestimo(id_livro, nome_aluno):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    
    # 1. Pega a data exata de hoje
    hoje = date.today()
    
    # 2. Calcula a data de entrega (Hoje + 7 dias)
    prazo = hoje + timedelta(days=7)
    
    # 3. Transforma a data no padrão brasileiro (DD/MM/AAAA)
    hoje_formatado = hoje.strftime("%d/%m/%Y")
    prazo_formatado = prazo.strftime("%d/%m/%Y")
    
    # Inserimos as duas datas novas no banco
    cursor.execute('''
        INSERT INTO emprestimos (id_livro, nome_aluno, data_saida, data_entrega) 
        VALUES (?, ?, ?, ?)
    ''', (id_livro, nome_aluno, hoje_formatado, prazo_formatado))
    
    conexao.commit()
    conexao.close()

def devolver_livro(id_livro):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM emprestimos WHERE id_livro = ?", (id_livro,))
    conexao.commit()
    conexao.close()

def listar_emprestados():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()
    
    # ATUALIZADO: Puxando as novas datas na busca
    cursor.execute('''
        SELECT emprestimos.id_livro, livros.titulo, emprestimos.nome_aluno, 
               emprestimos.data_saida, emprestimos.data_entrega
        FROM emprestimos
        JOIN livros ON emprestimos.id_livro = livros.id
    ''')
    
    resultados = cursor.fetchall()
    conexao.close()
    
    lista_formatada = []
    for linha in resultados:
        lista_formatada.append({
            "id_livro": linha[0], 
            "titulo": linha[1], 
            "aluno": linha[2],
            "data_saida": linha[3],  # Pegando a data de hoje do banco
            "data_entrega": linha[4] # Pegando a data do prazo do banco
        })
        
    return lista_formatada

# Roda a configuração
configurar_banco_emprestimos()