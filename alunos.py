import os
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def conectar():
  url_do_banco = (
      "postgresql://postgres.oiumgsgudkhlltwupflv:Craibas123%40@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"
  )
  return psycopg2.connect(url_do_banco)


def listar_alunos():
  conexao = conectar()
  cursor = conexao.cursor()
  cursor.execute("SELECT id, nome, serie FROM alunos ORDER BY id DESC")
  resultados = cursor.fetchall()
  cursor.close()
  conexao.close()

  lista = []
  for linha in resultados:
    lista.append({"id": linha[0], "nome": linha[1], "serie": linha[2]})
  return lista