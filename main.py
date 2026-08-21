import livros

while True:
    print("\n=== SISTEMA DE BIBLIOTECA COMPLETO ===")
    print("1. Cadastrar Livro")
    print("2. Ver Todos os Livros")
    print("3. Pesquisar um Livro")
    print("4. Editar um Livro")
    print("5. Excluir um Livro")
    print("6. Sair")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        nome = input("Nome do livro: ")
        escritor = input("Autor: ")
        livros.cadastrar_livro(nome, escritor)
        print("Sucesso! Livro salvo no banco de dados.")
        
    elif opcao == "2":
        print("\n--- Todos os Livros ---")
        lista = livros.listar_livros() 
        
        if len(lista) == 0:
            print("A sua biblioteca ainda está vazia.")
        else:
            for livro in lista:
                # Mudança: Adicionamos o ID na tela para o usuário ver
                print(f"ID: {livro['id']} | Livro: {livro['titulo']} - Autor: {livro['autor']}")
                
    elif opcao == "3":
        pesquisa = input("\nDigite o nome do livro para pesquisar: ")
        resultados = livros.pesquisar_livro(pesquisa)
        
        if len(resultados) == 0:
            print("Nenhum livro encontrado com esse nome.")
        else:
            print("\n--- Resultados da Pesquisa ---")
            for livro in resultados:
                # Mudança: Adicionamos o ID na tela
                print(f"ID: {livro['id']} | Livro: {livro['titulo']} - Autor: {livro['autor']}")
                
    # ==========================
    # AS NOVAS OPÇÕES DO MENU
    # ==========================
    elif opcao == "4":
        id_editar = input("\nDigite o ID numérico do livro que deseja editar: ")
        novo_nome = input("Digite o novo título correto: ")
        novo_escritor = input("Digite o novo autor correto: ")
        # Entrega as três caixinhas para o cozinheiro
        livros.editar_livro(id_editar, novo_nome, novo_escritor)
        print("Sucesso! As informações foram atualizadas.")

    elif opcao == "5":
        id_excluir = input("\nDigite o ID numérico do livro que deseja APAGAR: ")
        # Entrega a caixinha do ID para o cozinheiro
        livros.excluir_livro(id_excluir)
        print("Sucesso! O livro foi apagado para sempre do banco de dados.")
                
    elif opcao == "6":
        print("Fechando o sistema. Até logo!")
        break
        
    else:
        print("Opção inválida! Tente novamente.")