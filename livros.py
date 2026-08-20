estante = []

def cadastrar_livro (titulo, autor):
    novo_livro= {"titulo": titulo, "autor": autor}
    estante.append (novo_livro)

def listar_livros ():
    return  estante