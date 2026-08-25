import alunos
import emprestimos
import funcionarios
import livros
import streamlit as st
import visitas  # Módulo isolado de registro e relatório de presença

# Configuração da página deve ser sempre a primeira chamada do Streamlit
st.set_page_config(
    page_title="Biblioteca Escolar", page_icon="📚", layout="centered"
)

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
  st.sidebar.success(
      f"👤 Logado como: **{st.session_state['usuario_logado']['nome']}**"
  )
  if st.sidebar.button("🚪 Sair (Logout)"):
    st.session_state["usuario_logado"] = None
    st.rerun()

# Criando as duas portas de entrada principais via Abas
aba_aluno, aba_funcionario = st.tabs([
    "🎒 Terminal do Aluno (Autoatendimento)",
    "🔐 Área Restrita (Funcionário)",
])

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
      alunos_compatíveis = [
          a for a in todos_alunos if str(a["id"]) == entrada_busca
      ]
    else:
      # Caso contrário, filtramos por parte do nome (ignorando maiúsculas/minúsculas)
      alunos_compatíveis = [
          a
          for a in todos_alunos
          if entrada_busca.strip().lower() in a["nome"].strip().lower()
      ]

    if len(alunos_compatíveis) == 0:
      st.warning(
          "❌ Nenhum aluno encontrado. Verifique se digitou o nome ou ID"
          " corretamente."
      )
    elif len(alunos_compatíveis) == 1:
      # Se achou exatamente 1 aluno, já seleciona direto
      aluno_selecionado = alunos_compatíveis[0]
    else:
      # Se achou vários nomes parecidos, exibe a lista para ele escolher
      opcoes_formatadas = []
      mapa_alunos = {}

      for a in alunos_compatíveis:
        texto_opcao = f"ID: {a['id']} - {a['nome']} ({a['serie']})"
        opcoes_formatadas.append(texto_opcao)
        mapa_alunos[texto_opcao] = a

      escolha_usuario = st.selectbox(
          "Encontramos estes registros. Selecione o seu nome:",
          opcoes_formatadas,
      )

      if escolha_usuario:
        aluno_selecionado = mapa_alunos[escolha_usuario]

  st.divider()

  # SÓ MOSTRA A IDENTIFICAÇÃO E OS BOTÕES APÓS A ESCOLHA DEFINITIVA
  if aluno_selecionado is not None:
    st.success(
        f"✅ Identificado(a): **{aluno_selecionado['nome']}** | Matrícula:"
        f" `{aluno_selecionado['id']}` | Turma: `{aluno_selecionado['serie']}`"
    )

    # Opções do Aluno (incluindo pesquisa, empréstimo e presença)
    opcao_aluno = st.radio(
        "O que você deseja fazer?",
        [
            "Pesquisar Livro",
            "Registrar Meu Empréstimo",
            "Registrar Presença / Uso da Biblioteca",
        ],
        key="rad_aluno",
    )

    if opcao_aluno == "Pesquisar Livro":
      termo = st.text_input("Buscar livro por título ou autor:", key="busca_aluno")
      if st.button("Buscar Livro"):
        res = livros.pesquisar_livro(termo)
        if len(res) == 0:
          st.warning("Nenhum livro encontrado.")
        else:
          st.table(res)

    elif opcao_aluno == "Registrar Meu Empréstimo":
      id_livro_emp = st.text_input(
          "Digite o ID numérico do Livro que está pegando:", key="emp_livro_id"
      )
      if st.button("Confirmar Empréstimo"):
        if not id_livro_emp.isdigit():
          st.error("❌ Digite um ID numérico válido para o livro.")
        else:
          if emprestimos.livro_esta_emprestado(id_livro_emp):
            st.error("❌ Este livro já está emprestado no momento!")
          else:
            emprestimos.realizar_emprestimo(
                id_livro_emp, aluno_selecionado["id"]
            )
            st.balloons()
            st.success(
                f"🎉 Empréstimo registrado com sucesso para"
                f" {aluno_selecionado['nome']}!"
            )

    elif opcao_aluno == "Registrar Presença / Uso da Biblioteca":
      st.write(
          "Confirme abaixo sua presença ou uso do espaço da biblioteca hoje:"
      )
      if st.button("Confirmar Minha Presença"):
        if visitas.registrar_visita(aluno_selecionado["id"]):
          st.balloons()
          st.success(
              f"✅ Presença registrada, {aluno_selecionado['nome']}! Bom estudo!"
          )
        else:
          st.error("❌ Erro ao registrar presença. Tente novamente.")

# ==========================================
# ABA 2: ÁREA RESTRITA (FUNCIONÁRIO)
# ==========================================
with aba_funcionario:
  st.header("🔐 Área Restrita (Funcionário)")

  # Verifica se o funcionário está logado
  if st.session_state["usuario_logado"] is None:
    st.warning("🔒 Por favor, faça login para acessar o painel de gestão.")

    with st.form("form_login_func"):
      login_input = st.text_input("Login")
      senha_input = st.text_input("Senha", type="password")
      botao_login = st.form_submit_button("Entrar")

      if botao_login:
        dados_funcionario = funcionarios.verificar_login(
            login_input, senha_input
        )
        if dados_funcionario:
          st.session_state["usuario_logado"] = dados_funcionario
          st.success("Login realizado com sucesso!")
          st.rerun()
        else:
          st.error("❌ Login ou senha incorretos.")
  else:
    # Sub-abas administrativas organizadas
    sub_livros, sub_emprestimos, sub_visitas, sub_funcionarios = st.tabs([
        "📚 Gerenciar Livros",
        "🔄 Gerenciar Empréstimos",
        "📊 Relatório de Presença",
        "👥 Funcionários",
    ])

    with sub_livros:
      try:
        livros.main()
      except Exception as e:
        st.error(f"Erro ao carregar livros: {e}")

    with sub_emprestimos:
      try:
        emprestimos.main()
      except Exception as e:
        st.error(f"Erro ao carregar empréstimos: {e}")

    with sub_visitas:
      try:
        visitas.main()  # Mostra corretamente o relatório de presenças
      except Exception as e:
        st.error(f"Erro ao carregar relatório de presença: {e}")

    with sub_funcionarios:
      try:
        funcionarios.main()  # Mostra corretamente o painel de funcionários
      except Exception as e:
        st.error(f"Erro ao carregar funcionários: {e}")