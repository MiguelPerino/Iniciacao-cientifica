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
    "FarthestInsertion": fi_solver,
    "NearestNeighbor": nn_solver,
    "NearestInsertion": ni_solver,
    "CheapestInsertion": ci_solver,
    "RandomInsertion": random_solver,
    "SPT": spt_solver,
    
    "FarthestInsertion+2opt": fi_2opt_solver,
    "NearestNeighbor+2opt": nn_2opt_solver,
    "NearestInsertion+2opt": ni_2opt_solver,
    "CheapestInsertion+2opt": ci_2opt_solver,
    "RandomInsertion+2opt": random_2opt_solver,
    "SPT+2opt": spt_2opt_solver,
}

# Pares de heurísticas (sem 2opt, com 2opt)
pares_2opt = [
    ("FarthestInsertion", "FarthestInsertion+2opt"),
    ("NearestNeighbor", "NearestNeighbor+2opt"),
    ("NearestInsertion", "NearestInsertion+2opt"),
    ("CheapestInsertion", "CheapestInsertion+2opt"),
    ("RandomInsertion", "RandomInsertion+2opt"),
    ("SPT", "SPT+2opt"),
]

pasta_instancias = "C:/Users/Win 10/Downloads/SDSTsDP_Data/SDSTsDP_Data/BenchmarkData"
# instancias = sorted(os.listdir(pasta_instancias))
instancias = os.listdir(pasta_instancias)
instancias = [arq for arq in instancias if arq.endswith('.txt')]
instancias.sort()

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

# Cria o CSV no formato pivotado
with open("comparacao.csv", "w", newline="", encoding='utf-8-sig') as f:
    writer = csv.writer(f, delimiter=';')
    
    # Cabeçalho
    nomes_algoritmos = list(solvers.keys())
    
    # Monta header
    header = ["Instância", "Tamanho"] + nomes_algoritmos
    
    # Adiciona colunas de GAP (melhoria do 2-opt)
    for sem_2opt, com_2opt in pares_2opt:
        header.append(f"Melhoria% {sem_2opt}")
    
    writer.writerow(header)
    
    # Processa cada instância
    for instancia in instancias:
        # Extrai o tamanho da instância
        tamanho = instancia.split('_')[0].replace('N', '') if 'N' in instancia else '0'
        
        # Pega os makespans de todos os algoritmos
        makespans = {}
        for nome in nomes_algoritmos:
            makespans[nome] = resultados[instancia][nome]['makespan']
        
        # Monta a linha com os makespans
        linha = [instancia, tamanho]
        
        # Adiciona makespan de cada algoritmo
        for nome in nomes_algoritmos:
            linha.append(makespans[nome])
        
        for sem_2opt, com_2opt in pares_2opt:
            mk_sem = makespans[sem_2opt]
            mk_com = makespans[com_2opt]
            print(mk_sem, mk_com)
            if mk_sem == 0:
                melhoria = 0.0
            else:
                
                melhoria = ((mk_sem - mk_com) / mk_sem) * 100
            
            linha.append(f"{melhoria:.2f}")
        
        writer.writerow(linha)

print()
print("Arquivo comparacao.csv criado com sucesso!")
print()

# Separar em com e sem 2-opt
print("SEM 2-opt:")
for i, nome in enumerate([k for k in solvers.keys() if '+2opt' not in k], 1):
    print(f"  {i}. {nome}")

print()
print("COM 2-opt:")
for i, nome in enumerate([k for k in solvers.keys() if '+2opt' in k], 1):
    print(f"  {i}. {nome}")
