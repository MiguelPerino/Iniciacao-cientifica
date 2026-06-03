import csv
from collections import defaultdict

file = 'comparacao.csv'

# Estruturas
vitorias = defaultdict(float)
soma_makespan = defaultdict(int)
gap_total = defaultdict(float)
ranking_total = defaultdict(float)

total_instancias = 0

with open(file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    
    # nomes dos algoritmos
    nomes_algoritmos = reader.fieldnames[2:]
    nomes_algoritmos = [n for n in nomes_algoritmos if "Melhoria%" not in n]

    for row in reader:
        total_instancias += 1
        
        # pega makespans
        valores = {nome: int(row[nome]) for nome in nomes_algoritmos}
        
        #MÉDIA (soma)
        for nome, mk in valores.items():
            soma_makespan[nome] += mk
        
        #VITÓRIAS (com empate dividido)
        menor_mk = min(valores.values())
        vencedores = [n for n, mk in valores.items() if mk == menor_mk]
        
        for v in vencedores:
            vitorias[v] += 1 / len(vencedores)
        
        #GAP (%)
        for nome, mk in valores.items():
            gap = ((mk - menor_mk) / menor_mk) * 100 if menor_mk != 0 else 0
            gap_total[nome] += gap
        
        #RANKING
        ordenados = sorted(valores.items(), key=lambda x: x[1])
        
        posicao = 1
        for nome, _ in ordenados:
            ranking_total[nome] += posicao
            posicao += 1



############################
print("=" * 60)
print("RESULTADOS GERAIS")
print("=" * 60)

print("\nMÉDIA DE MAKESPAN:")
media_makespan = {}
for nome in nomes_algoritmos:
    media = soma_makespan[nome] / total_instancias
    media_makespan[nome] = media
    print(f"{nome}: {media:.2f}")

print("\nVITÓRIAS (com empate):")
for nome in nomes_algoritmos:
    perc = (vitorias[nome] / total_instancias) * 100
    print(f"{nome}: {vitorias[nome]:.2f} | {perc:.2f}%")

print("\nGAP MÉDIO (%):")
gap_medio = {}
for nome in nomes_algoritmos:
    gap = gap_total[nome] / total_instancias
    gap_medio[nome] = gap
    print(f"{nome}: {gap:.2f}%")


#É a posição média que um algoritmo fica em cada instância
print("\nRANKING MÉDIO:")
ranking_medio = {}
for nome in nomes_algoritmos:
    rank = ranking_total[nome] / total_instancias
    ranking_medio[nome] = rank
    print(f"{nome}: {rank:.2f}")

# MELHORES

print("\nMELHORES MÉTODOS:")

melhor_media = min(media_makespan, key=media_makespan.get)
melhor_vitoria = max(vitorias, key=vitorias.get)
melhor_gap = min(gap_medio, key=gap_medio.get)
melhor_ranking = min(ranking_medio, key=ranking_medio.get)

print(f"Menor média de makespan: {melhor_media}")
print(f"Mais vitórias: {melhor_vitoria}")
print(f"Menor GAP médio: {melhor_gap}")
print(f"Melhor ranking médio: {melhor_ranking}")

# with open('analise.txt', 'w', encoding='utf-8') as f:
#     f.write("=" * 60 + "\n")
#     f.write("RESULTADOS GERAIS\n")
#     f.write("=" * 60 + "\n\n")

#     f.write("MEDIA DE MAKESPAN:\n")
#     for nome in nomes_algoritmos:
#         media = media_makespan[nome]
#         f.write(f"{nome}: {media:.2f}\n")

#     f.write("\nVITORIAS (com empate):\n")
#     for nome in nomes_algoritmos:
#         perc = (vitorias[nome] / total_instancias) * 100
#         f.write(f"{nome}: {vitorias[nome]:.2f} | {perc:.2f}%\n")

#     f.write("\nGAP MEDIO (%):\n")
#     for nome in nomes_algoritmos:
#         gap = gap_medio[nome]
#         f.write(f"{nome}: {gap:.2f}%\n")

#     f.write("\nRANKING MEDIO:\n")
#     for nome in nomes_algoritmos:
#         rank = ranking_medio[nome]
#         f.write(f"{nome}: {rank:.2f}\n")

#     f.write("\nMELHORES METODOS:\n")
#     f.write(f"Menor media: {melhor_media}\n")
#     f.write(f"Mais vitorias: {melhor_vitoria}\n")
#     f.write(f"Menor GAP: {melhor_gap}\n")
#     f.write(f"Melhor ranking: {melhor_ranking}\n")
