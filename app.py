import streamlit as st
import livros
import emprestimos
import alunos
import funcionarios

st.set_page_config(page_title="Biblioteca Escolar", page_icon="📚", layout="centered")

# ==========================================
# GERENCIAMENTO DE SESSÃO (MEMÓRIA)
# ==========================================
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

# ==========================================
# CABEÇALHO E MODO DE ACESSO
# ==========================================
st.title("📚 Sistema de Biblioteca Escolar")

if st.session_state["usuario_logado"] is not None:
    st.sidebar.success(f"👤 Logado como: **{st.session_state['usuario_logado']['nome']}**")
    if st.sidebar.button("🚪 Sair (Logout)"):
        st.session_state["usuario_logado"] = None
        st.rerun()

# Criando as duas portas de entrada via Abas
aba_aluno, aba_funcionario = st.tabs(["🎒 Terminal do Aluno (Autoatendimento)", "🔐 Área Restrita (Funcionário)"])

# ==========================================
# ==========================================
# ABA 1: TERMINAL DO ALUNO
# ==========================================
with aba_aluno:
    st.header("🎒 Autoatendimento do Estudante")
    st.info("Digite seu Nome ou seu ID (Matrícula) para se identificar.")

    # Campo único de busca que aceita texto (nome) ou números (ID)
    entrada_busca = st.text_input("Digite seu Nome ou ID:", key="input_busca_aluno")
    aluno_selecionado = None

    if entrada_busca:
        todos_alunos = alunos.listar_alunos()
        
        # Se o usuário digitou apenas números, filtramos diretamente pelo ID exato!
        if entrada_busca.isdigit():
            alunos_compatíveis = [a for a in todos_alunos if str(a["id"]) == entrada_busca]
        else:
            # Caso contrário, filtramos por parte do nome (ignorando maiúsculas/minúsculas)
            alunos_compatíveis = [
                a for a in todos_alunos if entrada_busca.strip().lower() in a["nome"].strip().lower()
            ]

        if len(alunos_compatíveis) == 0:
            st.warning("❌ Nenhum aluno encontrado. Verifique se digitou o nome ou ID corretamente.")
        elif len(alunos_compatíveis) == 1:
            # Se achou exatamente 1 aluno (por ID exato ou nome único), já seleciona direto
            aluno_selecionado = alunos_compatíveis[0]
        else:
            # Se achou vários nomes parecidos (ex: vários "João"), exibe a lista para ele escolher
            opcoes_formatadas = []
            mapa_alunos = {}
            
            for a in alunos_compatíveis:
                texto_opcao = f"ID: {a['id']} - {a['nome']} ({a['serie']})"
                opcoes_formatadas.append(texto_opcao)
                mapa_alunos[texto_opcao] = a

            escolha_usuario = st.selectbox("Encontramos estes registros. Selecione o seu nome:", opcoes_formatadas)
            
            if escolha_usuario:
                aluno_selecionado = mapa_alunos[escolha_usuario]

    st.divider()

    # SÓ MOSTRA A IDENTIFICAÇÃO E OS BOTÕES APÓS A ESCOLHA DEFINITIVA
    if aluno_selecionado is not None:
        st.success(f"✅ Identificado(a): **{aluno_selecionado['nome']}** | Matrícula: `{aluno_selecionado['id']}` | Turma: `{aluno_selecionado['serie']}`")
        
        opcao_aluno = st.radio("O que você deseja fazer?", ["Pesquisar Livro", "Registrar Meu Empréstimo"], key="rad_aluno")
        
        if opcao_aluno == "Pesquisar Livro":
            termo = st.text_input("Buscar livro por título ou autor:", key="busca_aluno")
            if st.button("Buscar Livro"):
                res = livros.pesquisar_livro(termo)
                if len(res) == 0:
                    st.warning("Nenhum livro encontrado.")
                else:
                    st.table(res)

        elif opcao_aluno == "Registrar Meu Empréstimo":
            id_livro_emp = st.text_input("Digite o ID numérico do Livro que está pegando:", key="emp_livro_id")
            if st.button("Confirmar Empréstimo"):
                if not id_livro_emp.isdigit():
                    st.error("❌ Digite um ID numérico válido para o livro.")
                else:
                    if emprestimos.livro_esta_emprestado(id_livro_emp):
                        st.error("❌ Este livro já está emprestado no momento!")
                    else:
                        emprestimos.realizar_emprestimo(id_livro_emp, aluno_selecionado["id"])
                        st.balloons()
                        st.success(f"🎉 Empréstimo registrado com sucesso para {aluno_selecionado['nome']}!")
