from farthestInsertion import solver as fi_solver
from main import solver as nn_solver, file_handling
from nearestInsertion import solver as ni_solver
from cheapestInserton import solver as ci_solver
from randomInsertion import solver as random_solver
from spt import solver as spt_solver

# Importando versões com 2-opt
from twoOptFarthestInsertion import solver as fi_2opt_solver
from twoOptNearestInsertion import solver as ni_2opt_solver
from twoOptCheapestInsertion import solver as ci_2opt_solver
from twoOptRandomInsertion import solver as random_2opt_solver
from twoOptSPT import solver as spt_2opt_solver
from twoOptNearestNeighbor import solver as nn_2opt_solver

import os
import csv

# Dicionário com TODAS as heurísticas
solvers = {
    # Heurísticas ORIGINAIS (sem 2-opt)
    "FarthestInsertion": fi_solver,
    "NearestNeighbor": nn_solver,
    "NearestInsertion": ni_solver,
    "CheapestInsertion": ci_solver,
    "RandomInsertion": random_solver,
    "SPT": spt_solver,
    
    # Heurísticas COM 2-opt
    "FarthestInsertion+2opt": fi_2opt_solver,
    "NearestNeighbor+2opt": nn_2opt_solver,
    "NearestInsertion+2opt": ni_2opt_solver,
    "CheapestInsertion+2opt": ci_2opt_solver,
    "RandomInsertion+2opt": random_2opt_solver,
    "SPT+2opt": spt_2opt_solver,
}

pasta_instancias = "instancias"
instancias = sorted(os.listdir(pasta_instancias))

# Dicionário para armazenar resultados de cada instância
resultados = {}

print("=" * 80)
print("EXECUTANDO HEURÍSTICAS COM E SEM 2-OPT")
print("=" * 80)
print(f"Total de instâncias: {len(instancias)}")
print(f"Total de algoritmos: {len(solvers)}")
print()

# Executa todos os solvers em todas as instâncias
for idx, instancia in enumerate(instancias, 1):
    print(f"Processando {idx}/{len(instancias)}: {instancia}")
    
    caminho = os.path.join(pasta_instancias, instancia)
    R, Pi, Sij = file_handling(caminho)
    
    resultados[instancia] = {}
    
    for nome, metodo in solvers.items():
        mk, seq = metodo(R, Pi, Sij)
        resultados[instancia][nome] = {
            'makespan': mk,
            'sequencia': seq
        }

print()
print("Gerando arquivo CSV...")

# Cria o CSV no formato pivotado (instâncias nas linhas, algoritmos nas colunas)
with open("comparacao.csv", "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    
    # Cabeçalho
    nomes_algoritmos = list(solvers.keys())
    header = ["Instância", "Tamanho"] + nomes_algoritmos + ["Melhor"]
    
    # Adiciona colunas de GAP para cada algoritmo
    for nome in nomes_algoritmos:
        header.append(f"Gap {nome}")
    
    writer.writerow(header)
    
    # Processa cada instância
    for instancia in instancias:
        # Extrai o tamanho da instância
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
            linha.append(f"{gap:.2f}")
        
        writer.writerow(linha)

print()
print("=" * 80)
print("Arquivo comparacao.csv criado com sucesso!")
print()
print("ALGORITMOS TESTADOS:")
print()

# Separar em com e sem 2-opt
print("SEM 2-opt:")
for i, nome in enumerate([k for k in solvers.keys() if '+2opt' not in k], 1):
    print(f"  {i}. {nome}")

print()
print("COM 2-opt:")
for i, nome in enumerate([k for k in solvers.keys() if '+2opt' in k], 1):
    print(f"  {i}. {nome}")
