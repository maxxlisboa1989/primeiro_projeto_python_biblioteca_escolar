import os
import psycopg2
import hashlib # A biblioteca de criptografia embutida no Python
from dotenv import load_dotenv

load_dotenv()
url_do_banco = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(url_do_banco)

def gerar_hash(senha):
    # Pega a senha real, bate no liquidificador (SHA-256) e devolve o texto embaralhado
    return hashlib.sha256(senha.encode()).hexdigest()

def configurar_banco_funcionarios():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

def cadastrar_funcionario(nome, login, senha):
    conexao = conectar()
    cursor = conexao.cursor()
    
    # 1. Criptografa a senha ANTES de chegar perto do banco de dados
    senha_criptografada = gerar_hash(senha)
    
    try:
        cursor.execute("INSERT INTO funcionarios (nome, login, senha) VALUES (%s, %s, %s)", 
                       (nome, login, senha_criptografada))
        conexao.commit()
        print(f"✅ Sucesso! O funcionário '{nome}' foi cadastrado.")
    except psycopg2.errors.UniqueViolation:
        print(f"❌ Erro: O login '{login}' já está sendo usado por outra pessoa!")
    finally:
        conexao.close()

def verificar_login(login, senha):
    conexao = conectar()
    cursor = conexao.cursor()
    
    # 1. O usuário digita a senha normal, nós criptografamos e comparamos com o lixo criptografado do banco
    senha_criptografada = gerar_hash(senha)
    
    cursor.execute("SELECT id, nome FROM funcionarios WHERE login = %s AND senha = %s", 
                   (login, senha_criptografada))
    
    usuario = cursor.fetchone()
    conexao.close()
    
    # Se achou o usuário, devolve os dados dele. Se não achou (ou errou a senha), devolve Nada (None)
    if usuario:
        return {"id": usuario[0], "nome": usuario[1]}
    else:
        return None

# Configura a gaveta na nuvem ao executar
configurar_banco_funcionarios()

def listar_funcionarios():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, login FROM funcionarios ORDER BY id")
    resultados = cursor.fetchall()
    conexao.close()
    
    lista = []
    for linha in resultados:
        lista.append({"id": linha[0], "nome": linha[1], "login": linha[2]})
    return lista

def criar_admin_padrao():
    # Verifica se já existe algum funcionário cadastrado. Se não houver, cria o admin automaticamente!
    equipe = listar_funcionarios()
    if len(equipe) == 0:
        cadastrar_funcionario("Administrador", "admin", "12345")
        print("🔐 Conta padrão 'admin' (senha: 12345) criada com sucesso na nuvem!")

# Roda a verificação toda vez que o módulo for importado
criar_admin_padrao()