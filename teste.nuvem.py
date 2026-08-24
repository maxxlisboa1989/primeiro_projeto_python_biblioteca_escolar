import os
import psycopg2
from dotenv import load_dotenv

# 1. Abre o cofre secreto (.env)
load_dotenv()

# 2. Pega a URL que guardamos lá dentro
url_do_banco = os.getenv("DATABASE_URL")

print("⏳ Ligando os motores e tentando conectar ao Supabase...")

try:
    # 3. Tenta fazer a conexão com a nuvem
    conexao = psycopg2.connect(url_do_banco)
    print("✅ SUCESSO ABSOLUTO! O seu Python acabou de dar um aperto de mão na Nuvem!")
    
    # Fecha a conexão
    conexao.close()
    
except Exception as erro:
    print("❌ Ops! Algo deu errado. Verifique se a senha ou a URL estão corretas no .env.")
    print(f"Detalhe do erro: {erro}")