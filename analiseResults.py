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
    verificador_empate = 0
    for metodo, mk in dados:
        if mk == menor_mk:
            verificador_empate += 1
            if verificador_empate == 1:
                count[metodo] += 1
            
melhor_metodo = max(count, key=count.get)
    

print('Analisando os métodos, vendo qual tem mais vitórias:')
for mtd, vitoria in count.items():
    porcentagem = (vitoria / total_instancias)* 100
    print(f'{mtd}: {vitoria}\t | {porcentagem:.2f}%')

print()
print('Método com mais vitória:')
print(melhor_metodo)

