import streamlit as st
import livros
import emprestimos

st.set_page_config(page_title="Minha Biblioteca", page_icon="📚")

# ==========================================
# MENU LATERAL (SIDEBAR)
# ==========================================
st.sidebar.title("Navegação")
# Cria uma caixa de seleção no menu lateral
menu = st.sidebar.selectbox("Escolha uma opção:", ["Ver Livros", "Cadastrar Livro"])

# ==========================================
# TELA 1: VER LIVROS
# ==========================================
if menu == "Ver Livros":
    st.title("📚 Todos os Livros")
    lista = livros.listar_livros()
    
    if len(lista) == 0:
        st.warning("A biblioteca ainda está vazia.")
    else:
        st.table(lista)

# ==========================================
# TELA 2: CADASTRAR LIVRO
# ==========================================
elif menu == "Cadastrar Livro":
    st.title("➕ Cadastrar Novo Livro")
    
    # Substitui os antigos 'inputs' da tela preta
    nome = st.text_input("Título do Livro:")
    escritor = st.text_input("Autor do Livro:")
    
    # Cria o botão e verifica se ele foi clicado
    if st.button("Salvar Livro no Banco de Dados"):
        
        # A nossa velha trava de segurança continua aqui!
        if nome == "" or escritor == "":
            st.error("❌ O título e o autor não podem ficar em branco!")
        else:
            livros.cadastrar_livro(nome, escritor)
            st.success(f"✅ O livro '{nome}' foi salvo com sucesso!")