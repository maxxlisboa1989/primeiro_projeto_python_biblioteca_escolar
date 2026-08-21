import livros
import tkinter


while True:
    print("\n=== MENU DA BIBLIOTECA ===")
    print("1. Cadastrar Livro")
    print("2. Ver Todos os Livros")
    print("3. Pesquisar um Livro")
    print("4. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Nome do livro: ")
        escritor = input("Autor: ")
        livros.cadastrar_livro(nome, escritor)
        print("Sucesso! Livro salvo no banco de dados.")

    elif opcao == "2":
        print("\n--- Todos os Livros ---")
        lista = livros.listar_livros()   # Pede a lista para o livros.py

        if len(lista) == 0:
            print("A sua biblioteca ainda está vazia.")
        else:
            for livro in lista:
                print(f"Livro: {livro['titulo']} - Autor: {livro['autor']}")

    elif opcao == "3":
        pesquisa = input("\nDigite o nome do livro para pesquisar: ")
        resultados = livros.pesquisar_livro(pesquisa)

        if len(resultados) == 0:
            print("Nenhum livro encontrado com esse nome.")
        else:
            print("\n--- Resultados da Pesquisa ---")
            for livro in resultados:
                print(f"Encontrado: {livro['titulo']} - Autor: {livro['autor']}")

    elif opcao == "4":
        print("Fechando o sistema. Até logo!")
        break

    else:
        print("Opção inválida! Tente novamente.")