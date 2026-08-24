import streamlit as st
import psycopg2
from datetime import datetime

def conectar():
    url_do_banco = st.secrets["DATABASE_URL"]
    return psycopg2.connect(url_do_banco)

def registrar_entrada(aluno_nome, matricula, motivo):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO acessos_biblioteca (aluno_nome, matricula, motivo) VALUES (%s, %s, %s)",
        (aluno_nome, matricula, motivo)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

def carregar_acessos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT aluno_nome, matricula, data_hora, motivo FROM acessos_biblioteca ORDER BY data_hora DESC")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados

def exibir_pagina_acessos():
    st.header("🚪 Controle de Fluxo e Frequência na Biblioteca")
    
    st.subheader("Registrar Entrada de Aluno")
    with st.form("form_acesso"):
        aluno_nome = st.text_input("Nome do Aluno")
        matricula = st.text_input("Matrícula (Opcional)")
        motivo = st.selectbox("Motivo da Visita", ["Leitura Local", "Estudo para Provas", "Pesquisa Escolar", "Uso de Computadores/Outros"])
        
        enviar = st.form_submit_button("Registrar Entrada")
        if enviar:
            if aluno_nome.strip() != "":
                registrar_entrada(aluno_nome, matricula, motivo)
                st.success(f"Entrada registrada com sucesso para {aluno_nome}!")
            else:
                st.warning("Por favor, digite o nome do aluno.")

    st.divider()
    
    st.subheader("📊 Relatórios e Logs de Acesso")
    dados = carregar_acessos()
    
    if dados:
        import pandas as pd
        df = pd.DataFrame(dados, columns=["Nome", "Matrícula", "Data/Hora", "Motivo"])
        
        # Métricas rápidas
        total_geral = len(df)
        st.metric(label="Total de Registros de Acesso", value=total_geral)
        
        # Exibir tabela completa de logs
        st.dataframe(df, use_container_width=True)
    else:
        st.info("N nenhum acesso registrado até o momento.")