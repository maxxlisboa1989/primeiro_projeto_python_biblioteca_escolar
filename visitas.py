import os
import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def conectar():
  # URL direta do seu banco no Supabase como garantia absoluta
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
    st.error(f"Erro ao configurar tabela de visitas: {e}")


# Inicializa a tabela isolada
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


# Função visual chamada de forma independente na Área Restrita
def main():
  st.subheader("📊 Histórico de Presença e Uso da Biblioteca")
  st.write(
      "Acompanhe o fluxo diário e mensal de alunos que utilizaram o espaço."
  )

  visitas = relatorio_visitas_geral()

  if visitas:
    df_visitas = pd.DataFrame(
        visitas, columns=["ID", "Nome do Aluno", "Turma", "Data e Hora"]
    )
    st.metric("Total de Registros de Acesso", len(df_visitas))
    st.dataframe(df_visitas, use_container_width=True)
  else:
    st.info("Nenhum registro de presença encontrado até o momento.")

def main():
  st.subheader("👥 Gerenciamento de Funcionários")
  st.write("Cadastre novos operadores ou visualize a equipe autorizada.")

  # Formulário para cadastrar funcionário
  with st.form("form_cadastrar_func"):
    nome = st.text_input("Nome do Funcionário")
    login = st.text_input("Login de Acesso")
    senha = st.text_input("Senha", type="password")
    botao_cadastrar = st.form_submit_button("Cadastrar Funcionário")

    if botao_cadastrar:
      if nome.strip() and login.strip() and senha.strip():
        try:
          conexao = conectar()
          cursor = conexao.cursor()
          cursor.execute(
              "INSERT INTO funcionarios (nome, login, senha) VALUES (%s, %s,"
              " %s)",
              (nome, login, senha),
          )
          conexao.commit()
          cursor.close()
          conexao.close()
          st.success(f"✅ Funcionário '{nome}' cadastrado com sucesso!")
          st.rerun()
        except Exception as e:
          st.error(f"Erro ao cadastrar funcionário: {e}")
      else:
        st.warning("⚠️ Preencha todos os campos.")

  st.divider()

  # Listagem de funcionários cadastrados
  st.write("### 📋 Equipe Cadastrada")
  try:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, login FROM funcionarios ORDER BY id DESC")
    funcs = cursor.fetchall()
    cursor.close()
    conexao.close()

    if funcs:
      for f in funcs:
        f_id, f_nome, f_login = f
        col1, col2 = st.columns([3, 1])
        with col1:
          st.write(f"👤 **{f_nome}** (Login: `{f_login}`)")
        with col2:
          if st.button("🗑️ Excluir", key=f"del_func_{f_id}"):
            try:
              conexao = conectar()
              cursor = conexao.cursor()
              cursor.execute(
                  "DELETE FROM funcionarios WHERE id = %s", (f_id,)
              )
              conexao.commit()
              cursor.close()
              conexao.close()
              st.success("Funcionário removido com sucesso!")
              st.rerun()
            except Exception as e:
              st.error(f"Erro ao excluir: {e}")
        st.divider()
    else:
      st.info("Nenhum funcionário cadastrado.")
  except Exception:
    st.info("Tabela de funcionários em configuração.")    