import livros

while True:
    print("\n=== SISTEMA DE BIBLIOTECA COMPLETO ===")
    print("1. Cadastrar Livro")
    print("2. Ver Todos os Livros")
    print("3. Pesquisar um Livro")
    print("4. Editar um Livro")
    print("5. Excluir um Livro")
    print("6. Sair")
    
    # O .strip() remove espaços vazios que o usuário digitar sem querer
    opcao = input("Escolha uma opção: ").strip()
    
    if opcao == "1":
        nome = input("Nome do livro: ").strip()
        escritor = input("Autor: ").strip()
        
        # TRATAMENTO DE ERRO: Impede cadastro em branco
        if nome == "" or escritor == "":
            print("❌ ERRO: O título e o autor não podem ficar em branco!")
        else:
            livros.cadastrar_livro(nome, escritor)
            print("✅ Sucesso! Livro salvo no banco de dados.")
            
    elif opcao == "2":
        print("\n--- Todos os Livros ---")
        lista = livros.listar_livros() 
        
        if len(lista) == 0:
            print("A sua biblioteca ainda está vazia.")
        else:
            for livro in lista:
                print(f"ID: {livro['id']} | Livro: {livro['titulo']} - Autor: {livro['autor']}")
                
    elif opcao == "3":
        # Mudamos a frase para avisar o usuário do novo superpoder da busca
        pesquisa = input("\nDigite parte do título OU o nome do autor: ").strip()
        
        # TRATAMENTO DE ERRO: Impede pesquisa em branco
        if pesquisa == "":
            print("❌ ERRO: Você precisa digitar algo para pesquisar!")
        else:
            resultados = livros.pesquisar_livro(pesquisa)
            if len(resultados) == 0:
                print("Nenhum livro encontrado com esse termo.")
            else:
                print("\n--- Resultados da Pesquisa ---")
                for livro in resultados:
0                    print(f"ID: {livro['id']} | Livro: {livro['titulo']} - Autor: {livro['autor']}")
                
    elif opcao == "4":
        nome_autor_editar = input("\nDigite o nome ou autor do livro que deseja editar: ").strip()
        
        # TRATAMENTO DE ERRO: Garante que o usuário digitou um número
        if not nome_autor_editar.strip():
            print("❌ ERRO: O Nome ou Autor precisa ser texto!")
        else:
            novo_nome = input("Digite o novo título: ").strip()
            novo_escritor = input("Digite o novo autor: ").strip()
            
            if novo_nome == "" or novo_escritor == "":
                print("❌ ERRO: O título e o autor não podem ficar em branco!")
            else:
                livros.editar_livro(novo_nome, novo_escritor)
                print("✅ Sucesso! As informações foram atualizadas.")

    elif opcao == "5":
        id_excluir = input("\nDigite o ID numérico do livro que deseja APAGAR: ").strip()
        
        if not id_excluir.isdigit():
            print("❌ ERRO: O ID precisa ser um número!")
        else:
            livros.excluir_livro(id_excluir)
            print("✅ Sucesso! O livro foi apagado.")
                
    elif opcao == "6":
        print("Fechando o sistema. Até logo!")
        break
        
    else:
        print("❌ Opção inválida! Tente novamente.")