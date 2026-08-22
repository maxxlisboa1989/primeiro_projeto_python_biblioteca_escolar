import csv
import alunos

print("🤖 Iniciando o Robô Importador de Alunos...")

try:
    with open('alunos.csv', mode='r', encoding='latin-1') as arquivo:
        
        # MUDANÇA 1: Avisamos que o separador é o ponto e vírgula do Excel BR!
        leitor = csv.reader(arquivo, delimiter=';')
        
        next(leitor) # Pula a linha de cabeçalho
        
        contador = 0
        for linha in leitor:
            
            # MUDANÇA 2: Trava de Segurança contra linhas vazias fantasmas do Excel
            if len(linha) < 2:
                continue
                
            nome_aluno = linha[0].strip()
            serie_aluno = linha[1].strip()
            
            alunos.cadastrar_aluno(nome_aluno, serie_aluno)
            print(f"✅ Importado: {nome_aluno} - {serie_aluno}")
            contador += 1
            
    print(f"\n🎉 SUCESSO! O robô importou {contador} alunos para o banco de dados!")
    
except FileNotFoundError:
    print("❌ ERRO: O arquivo 'alunos.csv' não foi encontrado.")