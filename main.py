import livros
import emprestimos  # Trazendo o novo módulo para trabalhar!

while True:
    print("\n=== SISTEMA DE BIBLIOTECA COMPLETO ===")
    print("1. Cadastrar Livro")
    print("2. Ver Todos os Livros")
    print("3. Pesquisar um Livro")
    print("4. Editar um Livro")
    print("5. Excluir um Livro")
    print("--- SETOR DE EMPRÉSTIMOS ---")
    print("6. Emprestar um Livro")
    print("7. Devolver um Livro")
    print("8. Ver Livros Emprestados")
    print("9. Sair")
    
    opcao = input("Escolha uma opção: ").strip()
    
    if opcao == "1":
        nome = input("Nome do livro: ").strip()
        escritor = input("Autor: ").strip()
        if nome == "" or escritor == "":
            print("❌ ERRO: O título e o autor não podem ficar em branco!")
        else:
            livros.cadastrar_livro(nome, escritor)
            print("✅ Sucesso! Livro salvo.")
            
    elif opcao == "2":
        print("\n--- Todos os Livros ---")
        lista = livros.listar_livros() 
        if len(lista) == 0:
            print("A biblioteca está vazia.")
        else:
            for livro in lista:
                print(f"ID: {livro['id']} | Livro: {livro['titulo']} - Autor: {livro['autor']}")
                
    elif opcao == "3":
        pesquisa = input("\nDigite parte do título OU o nome do autor: ").strip()
        if pesquisa == "":
            print("❌ ERRO: Digite algo para pesquisar!")
        else:
            resultados = livros.pesquisar_livro(pesquisa)
            if len(resultados) == 0:
                print("Nenhum livro encontrado.")
            else:
                for livro in resultados:
                    print(f"ID: {livro['id']} | Livro: {livro['titulo']} - Autor: {livro['autor']}")
                
    elif opcao == "4":
        id_editar = input("\nDigite o ID numérico do livro: ").strip()
        if not id_editar.isdigit():
            print("❌ ERRO: O ID precisa ser um número!")
        else:
            novo_nome = input("Novo título: ").strip()
            novo_escritor = input("Novo autor: ").strip()
            if novo_nome == "" or novo_escritor == "":
                print("❌ ERRO: Não pode ficar em branco!")
            else:
                livros.editar_livro(id_editar, novo_nome, novo_escritor)
                print("✅ Atualizado com sucesso.")

    elif opcao == "5":
        id_excluir = input("\nDigite o ID numérico do livro para APAGAR: ").strip()
        if not id_excluir.isdigit():
            print("❌ ERRO: O ID precisa ser um número!")
        else:
            livros.excluir_livro(id_excluir)
            print("✅ Livro apagado.")
            
    # ==========================================
    # NOVAS OPÇÕES DO CAIXA (EMPRÉSTIMOS)
    # ==========================================
    elif opcao == "6":
        id_livro = input("\nDigite o ID do livro que será emprestado: ").strip()
        if not id_livro.isdigit():
            print("❌ ERRO: O ID precisa ser um número!")
        else:
            nome_aluno = input("Nome do aluno que vai pegar o livro: ").strip()
            if nome_aluno == "":
                print("❌ ERRO: O nome do aluno é obrigatório!")
            else:
                emprestimos.realizar_emprestimo(id_livro, nome_aluno)
                print(f"✅ Livro emprestado com sucesso para {nome_aluno}.")
                
    elif opcao == "7":
        id_devolucao = input("\nDigite o ID do livro que está sendo devolvido: ").strip()
        if not id_devolucao.isdigit():
            print("❌ ERRO: O ID precisa ser um número!")
        else:
            emprestimos.devolver_livro(id_devolucao)
            print("✅ Livro devolvido à biblioteca!")
            
    elif opcao == "8":
        print("\n--- Lista de Livros Emprestados ---")
        emprestados = emprestimos.listar_emprestados()
        if len(emprestados) == 0:
            print("Nenhum livro emprestado no momento.")
        else:
            for item in emprestados:
                # Agora imprimimos em duas linhas para ficar visualmente organizado!
                print(f"ID: {item['id_livro']} | Título: {item['titulo']} | Aluno: {item['aluno']}")
                print(f"   📅 Saída: {item['data_saida']} -> ⏳ Entrega: {item['data_entrega']}")
                
    elif opcao == "9":
        print("Fechando o sistema. Até logo!")
        break
        
    else:
        print("❌ Opção inválida! Tente novamente.")
