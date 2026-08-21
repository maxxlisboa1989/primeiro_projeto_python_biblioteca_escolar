import streamlit as st
import livros
import emprestimos

st.set_page_config(page_title="Minha Biblioteca", page_icon="📚")

# ==========================================
# MENU LATERAL (SIDEBAR)
# ==========================================
st.sidebar.title("Navegação")

# ATUALIZADO: Menu 100% completo!
opcoes_menu = [
    "Ver Livros", 
    "Pesquisar Livro",
    "Cadastrar Livro", 
    "Editar Livro",
    "Excluir Livro",
    "Emprestar Livro", 
    "Devolver Livro", 
    "Livros Emprestados"
]
menu = st.sidebar.selectbox("Escolha uma opção:", opcoes_menu)

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
# TELA 2: PESQUISAR LIVRO (NOVO)
# ==========================================
elif menu == "Pesquisar Livro":
    st.title("🔍 Pesquisar Livro")
    st.write("Busque por parte do título ou nome do autor.")
    
    termo = st.text_input("Digite sua pesquisa:")
    
    if st.button("Buscar"):
        if termo == "":
            st.error("❌ Digite algo para pesquisar!")
        else:
            resultados = livros.pesquisar_livro(termo)
            if len(resultados) == 0:
                st.warning("Nenhum livro encontrado.")
            else:
                st.table(resultados)

# ==========================================
# TELA 3: CADASTRAR LIVRO
# ==========================================
elif menu == "Cadastrar Livro":
    st.title("➕ Cadastrar Novo Livro")
    nome = st.text_input("Título do Livro:")
    escritor = st.text_input("Autor do Livro:")
    
    if st.button("Salvar Livro no Banco de Dados"):
        if nome == "" or escritor == "":
            st.error("❌ O título e o autor não podem ficar em branco!")
        else:
            livros.cadastrar_livro(nome, escritor)
            st.success(f"✅ O livro '{nome}' foi salvo com sucesso!")

# ==========================================
# TELA 4: EDITAR LIVRO (NOVO)
# ==========================================
elif menu == "Editar Livro":
    st.title("✏️ Editar Livro")
    st.write("Use a tela 'Ver Livros' para descobrir o ID numérico do livro.")
    
    id_editar = st.text_input("ID numérico do livro:")
    novo_nome = st.text_input("Novo título correto:")
    novo_escritor = st.text_input("Novo autor correto:")
    
    if st.button("Atualizar Informações"):
        if not id_editar.isdigit():
            st.error("❌ O ID precisa ser um número!")
        elif novo_nome == "" or novo_escritor == "":
            st.error("❌ O título e o autor não podem ficar em branco!")
        else:
            livros.editar_livro(id_editar, novo_nome, novo_escritor)
            st.success("✅ As informações foram atualizadas com sucesso!")

# ==========================================
# TELA 5: EXCLUIR LIVRO (NOVO)
# ==========================================
elif menu == "Excluir Livro":
    st.title("🗑️ Excluir Livro")
    st.error("⚠️ Atenção: Esta ação apagará o livro para sempre do banco de dados!")
    
    id_excluir = st.text_input("ID numérico do livro para excluir:")
    
    if st.button("Excluir Definitivamente"):
        if not id_excluir.isdigit():
            st.error("❌ O ID precisa ser um número!")
        else:
            livros.excluir_livro(id_excluir)
            st.success("✅ O livro foi apagado com sucesso!")

# ==========================================
# TELA 6: EMPRESTAR LIVRO
# ==========================================
elif menu == "Emprestar Livro":
    st.title("🤝 Emprestar Livro")
    id_livro = st.text_input("ID numérico do livro:")
    nome_aluno = st.text_input("Nome do aluno:")
    
    if st.button("Registrar Empréstimo"):
        if id_livro == "" or nome_aluno == "":
            st.error("❌ Preencha todos os campos!")
        elif not id_livro.isdigit():
            st.error("❌ O ID precisa ser um número!")
        else:
            if emprestimos.livro_esta_emprestado(id_livro) == True:
                st.error("❌ Operação bloqueada! Este livro já está emprestado.")
            else:
                emprestimos.realizar_emprestimo(id_livro, nome_aluno)
                st.success(f"✅ Livro emprestado com sucesso para {nome_aluno}.")

# ==========================================
# TELA 7: DEVOLVER LIVRO
# ==========================================
elif menu == "Devolver Livro":
    st.title("📥 Devolver Livro")
    id_devolucao = st.text_input("ID numérico do livro:")
    
    if st.button("Registrar Devolução"):
        if not id_devolucao.isdigit():
            st.error("❌ O ID precisa ser um número!")
        else:
            emprestimos.devolver_livro(id_devolucao)
            st.success("✅ Livro devolvido e liberado na biblioteca!")

# ==========================================
# TELA 8: LIVROS EMPRESTADOS
# ==========================================
elif menu == "Livros Emprestados":
    st.title("⏳ Livros Emprestados e Prazos")
    emprestados = emprestimos.listar_emprestados()
    
    if len(emprestados) == 0:
        st.info("Nenhum livro emprestado no momento. Tudo no acervo!")
    else:
        st.table(emprestados)