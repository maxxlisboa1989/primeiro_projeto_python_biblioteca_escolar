import csv
import alunos



print("🤖 Iniciando o Robô Importador de Alunos...")

# Abre o arquivo CSV que você jogou no Codespaces
try:
    with open('alunos.csv', mode='r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo)
        
        # Pula a primeira linha (porque é o cabeçalho "Nome, Serie")
        next(leitor) 
        
        contador = 0
        for linha in leitor:
            # linha[0] é a Coluna A (Nome) e linha[1] é a Coluna B (Série)
            nome_aluno = linha[0].strip()
            serie_aluno = linha[1].strip()
            
            # Chama a sua cozinha para salvar no banco!
            alunos.cadastrar_aluno(nome_aluno, serie_aluno)
            print(f"✅ Importado: {nome_aluno} - {serie_aluno}")
            contador += 1
            
    print(f"\n🎉 SUCESSO! O robô importou {contador} alunos para o banco de dados!")
    
except FileNotFoundError:
    print("❌ ERRO: O arquivo 'alunos.csv' não foi encontrado. Arraste ele para cá primeiro!")