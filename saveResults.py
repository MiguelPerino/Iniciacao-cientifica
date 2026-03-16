# from farthestInsertion import solver as fi_solver
# from main import solver as sm_solver, file_handling
# from nearestInsertion import solver as ni_solver
# from cheapestInserton import solver as ci_solver
# from twoOpt import solver as two_solver
# from randomInsertion import solver as random_solver
# from spt import solver as spt_solver

# import os
# import csv

# solvers = {
#     "FarthestInsertion": fi_solver,
#     "NearestNeighbor": sm_solver,
#     "NearestInsertion": ni_solver,
#     "CheapestInsertion": ci_solver,
#     "twoOpt": two_solver,
#     "RandomInsertion": random_solver,
#     "spt": spt_solver
# }

# pasta_instancias = "instancias"
# instancias = sorted(os.listdir(pasta_instancias))


# with open("comparacao.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(["Instância", "Método", "Makespan", "Sequência"])

#     for instancia in instancias: 
#         caminho = os.path.join(pasta_instancias, instancia)

#         R, Pi, Sij = file_handling(caminho)

#         for nome, metodo in solvers.items():
#             mk, seq = metodo(R, Pi, Sij)
#             writer.writerow([instancia, nome, mk, seq])

from farthestInsertion import solver as fi_solver
from main import solver as sm_solver, file_handling
from nearestInsertion import solver as ni_solver
from cheapestInserton import solver as ci_solver
from twoOptNearestNeighbor import solver as two_solver
from randomInsertion import solver as random_solver
from spt import solver as spt_solver

import os
import csv

solvers = {
    "FarthestInsertion": fi_solver,
    "NearestNeighbor": sm_solver,
    "NearestInsertion": ni_solver,
    "CheapestInsertion": ci_solver,
    "twoOptNearestNeighbor": two_solver,
    "RandomInsertion": random_solver,
    "spt": spt_solver
}

pasta_instancias = "instancias"
instancias = sorted(os.listdir(pasta_instancias))

# Dicionário para armazenar resultados de cada instância
resultados = {}

# Executa todos os solvers em todas as instâncias
for instancia in instancias:
    caminho = os.path.join(pasta_instancias, instancia)
    R, Pi, Sij = file_handling(caminho)
    
    resultados[instancia] = {}
    
    for nome, metodo in solvers.items():
        mk, seq = metodo(R, Pi, Sij)
        resultados[instancia][nome] = {
            'makespan': mk,
            'sequencia': seq
        }

# Cria o CSV no formato pivotado (instâncias nas linhas, algoritmos nas colunas)
with open("comparacao.csv", "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Cabeçalho
    nomes_algoritmos = list(solvers.keys())
    header = ["Instância", "Tamanho"] + nomes_algoritmos + ["Melhor"]
    
    # Adiciona colunas de GAP para cada algoritmo
    for nome in nomes_algoritmos:
        header.append(f"Gap {nome}")
    
    writer.writerow(header)
    
    # Processa cada instância
    for instancia in instancias:
        # Extrai o tamanho da instância (assume formato N10_... ou similar)
        # Se não conseguir extrair, usa 0
        tamanho = instancia.split('_')[0].replace('N', '') if 'N' in instancia else '0'
        
        # Pega os makespans de todos os algoritmos
        makespans = {}
        for nome in nomes_algoritmos:
            makespans[nome] = resultados[instancia][nome]['makespan']
        
        # Encontra o melhor (menor) makespan
        melhor_makespan = min(makespans.values())
        
        # Monta a linha com os makespans
        linha = [instancia, tamanho]
        
        # Adiciona makespan de cada algoritmo
        for nome in nomes_algoritmos:
            linha.append(makespans[nome])
        
        # Adiciona o melhor makespan
        linha.append(melhor_makespan)
        
        # Calcula e adiciona os GAPs
        for nome in nomes_algoritmos:
            if melhor_makespan == 0:
                gap = 0.0
            else:
                gap = ((makespans[nome] - melhor_makespan) / melhor_makespan) * 100
            linha.append(f"{gap:.2f}%")
        
        writer.writerow(linha)

print("Arquivo comparacao.csv criado com sucesso!")
print(f"Total de instâncias processadas: {len(instancias)}")
print(f"Total de algoritmos testados: {len(solvers)}")
