import os
import pandas as pd
import psycopg2
import streamlit as st


def conectar():
  url_do_banco = (
      "postgresql://postgres.oiumgsgudkhlltwupflv:Craibas123%40@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"
  )
  return psycopg2.connect(url_do_banco)


def configurar_banco_visitas():
  try:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitas (
                id SERIAL PRIMARY KEY,
                aluno_id INTEGER NOT NULL,
                data_visita TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conexao.commit()
    cursor.close()
    conexao.close()
  except Exception as e:
    pass


# Inicializa a tabela de visitas automaticamente
configurar_banco_visitas()


def registrar_visita(aluno_id):
  conexao = conectar()
  cursor = conexao.cursor()
  try:
    cursor.execute("INSERT INTO visitas (aluno_id) VALUES (%s)", (aluno_id,))
    conexao.commit()
    sucesso = True
  except Exception:
    sucesso = False
  finally:
    cursor.close()
    conexao.close()
  return sucesso


def relatorio_visitas_geral():
  conexao = conectar()
  cursor = conexao.cursor()
  try:
    cursor.execute("""
            SELECT v.id, a.nome, a.serie, v.data_visita 
            FROM visitas v
            JOIN alunos a ON v.aluno_id = a.id
            ORDER BY v.data_visita DESC
        """)
    resultados = cursor.fetchall()
  except Exception:
    resultados = []
  cursor.close()
  conexao.close()
  return resultados


# ==========================================
# FUNÇÃO PRINCIPAL VISUAL (CHAMADA PELO APP.PY)
# ==========================================
def main():
  st.subheader("📊 Relatório de Presença e Uso da Biblioteca")
  st.write(
      "Acompanhe o fluxo diário e mensal de alunos que utilizaram o espaço."
  )

  try:
    visitas = relatorio_visitas_geral()

    if visitas:
      df_visitas = pd.DataFrame(
          visitas, columns=["ID", "Nome do Aluno", "Turma", "Data e Hora"]
      )
      st.metric("Total de Registros de Acesso", len(df_visitas))
      st.dataframe(df_visitas, use_container_width=True)
    else:
      st.info(
          "Nenhum registro de presença ou uso da biblioteca encontrado até o"
          " momento."
      )
  except Exception as e:
    st.info("Tabela de visitas em configuração ou sem registros.")