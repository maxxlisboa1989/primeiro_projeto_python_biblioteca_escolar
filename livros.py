import os
import psycopg2
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def conectar():
    url_do_banco = "postgresql://postgres.oiumgsgudkhlltwupflv:Craibas123%40@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"
    return psycopg2.connect(url_do_banco)

def configurar_banco_livros():
    conexao = conectar()
    cursor = conexao.cursor()
    # Cria a tabela garantindo que a coluna categoria exista para suportar o painel
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            categoria TEXT
        )
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()

# Inicializa e atualiza a tabela automaticamente ao carregar o módulo
configurar_banco_livros()

def cadastrar_livro(titulo, autor, categoria="Geral"):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO livros (titulo, autor, categoria) VALUES (%s, %s, %s)", (titulo, autor, categoria))
    conexao.commit()
    cursor.close()
    conexao.close()

def listar_livros():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, titulo, autor, categoria FROM livros ORDER BY id")
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    lista = []
    for linha in resultados:
        lista.append({"id": linha[0], "titulo": linha[1], "autor": linha[2], "categoria": linha[3]})
    return lista

def pesquisar_livro(termo):
    conexao = conectar()
    cursor = conexao.cursor()
    termo_busca = f"%{termo}%"
    # O ILIKE ignora maiúsculas/minúsculas no Postgres
    cursor.execute("SELECT id, titulo, autor, categoria FROM livros WHERE titulo ILIKE %s OR autor ILIKE %s", (termo_busca, termo_busca))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    lista = []
    for linha in resultados:
        lista.append({"id": linha[0], "titulo": linha[1], "autor": linha[2], "categoria": linha[3]})
    return lista

def editar_livro(id_livro, novo_titulo, novo_autor, nova_categoria):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE livros SET titulo = %s, autor = %s, categoria = %s WHERE id = %s", (novo_titulo, novo_autor, nova_categoria, id_livro))
    conexao.commit()
    cursor.close()
    conexao.close()

def excluir_livro(id_livro):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM livros WHERE id = %s", (id_livro,))
    conexao.commit()
    cursor.close()
    conexao.close()

# ==========================================
# FUNÇÃO PRINCIPAL VISUAL (CHAMADA PELO APP.PY)
# ==========================================
def main():
    st.subheader("📚 Gerenciamento de Acervo (Livros)")
    st.write("Cadastre novos livros na biblioteca ou visualize o acervo atual.")

    # Formulário para cadastrar novo livro
    with st.form("form_cadastrar_livro"):
        titulo = st.text_input("Título do Livro")
        autor = st.text_input("Autor")
        categoria = st.text_input("Categoria / Gênero")
        botao_cadastrar = st.form_submit_button("Cadastrar Livro")

        if botao_cadastrar:
            if titulo.strip() and autor.strip():
                try:
                    cadastrar_livro(titulo, autor, categoria if categoria.strip() else "Geral")
                    st.success(f"✅ Livro '{titulo}' cadastrado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao cadastrar livro: {e}")
            else:
                st.warning("⚠️ Preencha pelo menos o Título e o Autor.")

    st.divider()

    # Listagem e exclusão de livros
    st.write("### 📖 Livros Cadastrados")
    try:
        livros_cadastrados = listar_livros()

        if livros_cadastrados:
            for l in livros_cadastrados:
                l_id = l["id"]
                l_titulo = l["titulo"]
                l_autor = l["autor"]
                l_cat = l["categoria"]
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"📖 **{l_titulo}** — *{l_autor}* (Categoria: {l_cat or 'Geral'}) [ID: `{l_id}`]")
                with col2:
                    if st.button("🗑️ Excluir", key=f"del_livro_{l_id}"):
                        try:
                            excluir_livro(l_id)
                            st.success("Livro removido com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao excluir livro: {e}")
                st.divider()
        else:
            st.info("Nenhum livro cadastrado no acervo até o momento.")
    except Exception as e:
        st.info(f"Tabela de livros em configuração ou vazia: {e}")