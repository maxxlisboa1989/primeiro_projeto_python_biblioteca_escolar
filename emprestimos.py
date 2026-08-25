import psycopg2
import streamlit as st


def conectar():
  url_do_banco = (
      "postgresql://postgres.oiumgsgudkhlltwupflv:Craibas123%40@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"
  )
  return psycopg2.connect(url_do_banco)


def configurar_banco_emprestimos():
  try:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS emprestimos (
                id SERIAL PRIMARY KEY,
                livro_id INTEGER NOT NULL,
                aluno_id INTEGER NOT NULL,
                data_emprestimo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_devolucao TIMESTAMP
            )
        """)
    conexao.commit()
    cursor.close()
    conexao.close()
  except Exception:
    pass


# Inicializa a tabela automaticamente
configurar_banco_emprestimos()


def livro_esta_emprestado(livro_id):
  conexao = conectar()
  cursor = conexao.cursor()
  # Usa livro_id corretamente conforme a tabela do banco
  cursor.execute(
      "SELECT id FROM emprestimos WHERE livro_id = %s AND data_devolucao IS"
      " NULL",
      (livro_id,),
  )
  resultado = cursor.fetchone()
  cursor.close()
  conexao.close()
  return resultado is not None


def realizar_emprestimo(livro_id, aluno_id):
  conexao = conectar()
  cursor = conexao.cursor()
  # Usa livro_id e aluno_id corretamente
  cursor.execute(
      "INSERT INTO emprestimos (livro_id, aluno_id) VALUES (%s, %s)",
      (livro_id, aluno_id),
  )
  conexao.commit()
  cursor.close()
  conexao.close()


# ==========================================
# FUNÇÃO PRINCIPAL VISUAL (CHAMADA PELO APP.PY)
# ==========================================
def main():
  st.subheader("🔄 Gerenciamento de Empréstimos")
  st.write("Visualize todos os empréstimos ativos e realize devoluções.")

  try:
    conexao = conectar()
    cursor = conexao.cursor()
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
    st.info(f"Painel de empréstimos em configuração: {e}")