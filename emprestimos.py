import os
import psycopg2
from dotenv import load_dotenv
from datetime import date, timedelta

import psycopg2
import streamlit as st


def conectar():
  url_do_banco = (
      "postgresql://postgres.oiumgsgudkhlltwupflv:Craibas123%40@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"
  )
  return psycopg2.connect(url_do_banco)

load_dotenv()
url_do_banco = os.getenv("DATABASE_URL")

def conectar():
  # URL direta do seu banco no Supabase como garantia absoluta
  url_do_banco = (
      "postgresql://postgres.oiumgsgudkhlltwupflv:Craibas123%40@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"
  )
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

def main():
  st.subheader("🔄 Gerenciamento de Empréstimos")
  st.write("Visualize todos os empréstimos ativos e realize devoluções.")

  try:
    conexao = conectar()
    cursor = conexao.cursor()
    # Busca empréstimos que ainda não foram devolvidos
    cursor.execute("""
            SELECT e.id, l.titulo, a.nome, a.serie, e.data_emprestimo 
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            JOIN alunos a ON e.aluno_id = a.id
            WHERE e.data_devolucao IS NULL
            ORDER BY e.data_emprestimo DESC
        """)
    emprestimos_ativos = cursor.fetchall()
    cursor.close()
    conexao.close()

    if emprestimos_ativos:
      import pandas as pd

      df_emp = pd.DataFrame(
          emprestimos_ativos,
          columns=[
              "ID Empréstimo",
              "Livro",
              "Aluno",
              "Turma",
              "Data do Empréstimo",
          ],
      )
      st.dataframe(df_emp, use_container_width=True)

      st.divider()
      st.write("### 📥 Registrar Devolução de Livro")

      id_emp_dev = st.text_input(
          "Digite o ID do Empréstimo para dar baixa/devolução:",
          key="input_dev_id",
      )
      if st.button("Confirmar Devolução"):
        if id_emp_dev.isdigit():
          try:
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE emprestimos SET data_devolucao = CURRENT_TIMESTAMP"
                " WHERE id = %s",
                (id_emp_dev,),
            )
            conexao.commit()
            cursor.close()
            conexao.close()
            st.success("✅ Devolução registrada com sucesso!")
            st.rerun()
          except Exception as e:
            st.error(f"Erro ao registrar devolução: {e}")
        else:
          st.error("❌ Digite um ID numérico válido.")
    else:
      st.info("Nenhum empréstimo ativo no momento.")
  except Exception as e:
    st.info(
        "Tabela de empréstimos em configuração ou sem registros por enquanto."
    )