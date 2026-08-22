import streamlit as st
import livros
import emprestimos
import alunos # Trazendo a secretaria para a nossa tela!

st.set_page_config(page_title="Minha Biblioteca", page_icon="📚")

st.sidebar.title("Navegação")

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


if menu == "Ver Livros":
    st.title("📚 Todos os Livros")
    lista = livros.listar_livros()
    if len(lista) == 0:
        st.warning("A biblioteca ainda está vazia.")
    else:
        st.table(lista)


elif menu == "Pesquisar Livro":
    st.title("🔍 Pesquisar Livro")
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


elif menu == "Cadastrar Livro":
    st.title("➕ Cadastrar Novo Livro")
    nome = st.text_input("Título do Livro:")
    escritor = st.text_input("Autor do Livro:")
    if st.button("Salvar Livro"):
        if nome == "" or escritor == "":
            st.error("❌ O título e o autor não podem ficar em branco!")
        else:
            livros.cadastrar_livro(nome, escritor)
            st.success(f"✅ O livro '{nome}' foi salvo com sucesso!")


elif menu == "Editar Livro":
    st.title("✏️ Editar Livro")
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
            st.success("✅ As informações foram atualizadas!")


elif menu == "Excluir Livro":
    st.title("🗑️ Excluir Livro")
    id_excluir = st.text_input("ID numérico do livro para excluir:")
    if st.button("Excluir Definitivamente"):
        if not id_excluir.isdigit():
            st.error("❌ O ID precisa ser um número!")
        else:
            livros.excluir_livro(id_excluir)
            st.success("✅ O livro foi apagado com sucesso!")


# ==========================================
# O NOVO SISTEMA DE EMPRÉSTIMO COM DROPDOWN
# ==========================================
elif menu == "Emprestar Livro":
    st.title("🤝 Emprestar Livro")
    
    # 1. Pede a lista de todos os alunos para a secretaria
    lista_alunos = alunos.listar_alunos()
    
    # 2. Prepara uma lista visual para o site. Ex: "1 - Maxuel (8º Ano)"
    opcoes_alunos = []
    for aluno in lista_alunos:
        opcoes_alunos.append(f"{aluno['id']} - {aluno['nome']} ({aluno['serie']})")
        
    id_livro = st.text_input("ID numérico do livro:")
    
    # 3. Cria a caixa de seleção suspensa!
    aluno_selecionado = st.selectbox("Selecione o aluno na lista:", opcoes_alunos)
    
    if st.button("Registrar Empréstimo"):
        if id_livro == "":
            st.error("❌ Preencha o ID do Livro!")
        elif not id_livro.isdigit():
            st.error("❌ O ID do livro precisa ser um número!")
        else:
            if emprestimos.livro_esta_emprestado(id_livro) == True:
                st.error("❌ Operação bloqueada! Este livro já está emprestado.")
            else:
                # 4. Magia do Python: O split corta a frase no " - " e pega apenas o número do ID (a posição 0)
                id_aluno_extraido = aluno_selecionado.split(" - ")[0]
                
                emprestimos.realizar_emprestimo(id_livro, id_aluno_extraido)
                st.success("✅ Livro emprestado com sucesso!")


elif menu == "Devolver Livro":
    st.title("📥 Devolver Livro")
    id_devolucao = st.text_input("ID numérico do livro:")
    if st.button("Registrar Devolução"):
        if not id_devolucao.isdigit():
            st.error("❌ O ID precisa ser um número!")
        else:
            emprestimos.devolver_livro(id_devolucao)
            st.success("✅ Livro devolvido e liberado!")


elif menu == "Livros Emprestados":
    st.title("⏳ Livros Emprestados e Prazos")
    emprestados = emprestimos.listar_emprestados()
    if len(emprestados) == 0:
        st.info("Nenhum livro emprestado no momento. Tudo no acervo!")
    else:
        # A tabela agora vai mostrar a Série automaticamente!
        st.table(emprestados)