import livros

while True:
    print("\n 1. Cadastrar | 2. Ver Livros| 3. Sair")
    opcao = input("Escolha: ")

    if opcao == "1":
        nome = input ("Nome do livro: ")
        escritor = input ("Escritor: ")
        livros.cadastrar_livro(nome, escritor)
        print ("Livro salvo na biblioteca!")

    elif opcao=="2":
        for livro in livros.listar_livros():
            print (f"Livro: {livro["titulo"]} - Autor: {livro["autor"]}")
    elif opcao=="3":
        break