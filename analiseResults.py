'''
Preciso atualizar este para analisar todos os resultados
este é o antigo, nao tem as heuristicas com 2Opt
falta adicionar elas e comparar para ver qual deu o melhor resultado
'''



















import csv
from collections import defaultdict #cria um dicionário mesmo se nao existe chave ainda, cria vazio

file = 'comparacao.csv'

resultados = defaultdict(list)

with open(file, 'r', encoding='latin-1') as f:

    reader = csv.DictReader(f)
    for row in reader:
        metodo = row['Método']
        instancia = row['Instância']
        makespan = int(row['Makespan'])

        resultados[instancia].append((metodo, makespan))

count = defaultdict(int)
total_instancias = len(resultados)

for intancia, dados in resultados.items():
    menor_mk = min(mk for _, mk in dados)   
    
    # Conta quantos métodos têm o menor makespan
    metodos_com_menor = [metodo for metodo, mk in dados if mk == menor_mk]
    
    # Se mais de um (empate), ninguém ganha
    if len(metodos_com_menor) == 1:
        count[metodos_com_menor[0]] += 1
            
melhor_metodo = max(count, key=count.get) if count else "Nenhum"
    

print('Analisando os métodos, vendo qual tem mais vitórias:')
for mtd, vitoria in count.items():
    porcentagem = (vitoria / total_instancias)* 100
    print(f'{mtd}: {vitoria}\t | {porcentagem:.2f}%')

print()
print('Método com mais vitória:')
print(melhor_metodo)

