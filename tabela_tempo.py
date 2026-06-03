import csv
import os
import time
from collections import defaultdict

# =========================
# IMPORTA AS HEURÍSTICAS
# =========================

from farthestInsertion import solver as fi_solver
from main import solver as nn_solver, file_handling
from nearestInsertion import solver as ni_solver
from cheapestInserton import solver as ci_solver
from randomInsertion import solver as random_solver

# versões com 2-opt
from twoOptFarthestInsertion import solver as fi_2opt_solver
from twoOptNearestInsertion import solver as ni_2opt_solver
from twoOptCheapestInsertion import solver as ci_2opt_solver
from twoOptRandomInsertion import solver as random_2opt_solver
from twoOptNearestNeighbor import solver as nn_2opt_solver

solvers = {
    "FI": fi_solver,
    "NN": nn_solver,
    "NI": ni_solver,
    "CI": ci_solver,
    "RI": random_solver,

    "FI+2opt": fi_2opt_solver,
    "NN+2opt": nn_2opt_solver,
    "NI+2opt": ni_2opt_solver,
    "CI+2opt": ci_2opt_solver,
    "RI+2opt": random_2opt_solver,
}


pares = [
    ("FI", "FI+2opt"),
    ("NN", "NN+2opt"),
    ("NI", "NI+2opt"),
    ("CI", "CI+2opt"),
    ("RI", "RI+2opt"),
]


pasta_instancias = r"C:/Users/Win 10/Downloads/SDSTsDP_Data/SDSTsDP_Data/BenchmarkData"

instancias = os.listdir(pasta_instancias)
instancias = [arq for arq in instancias if arq.endswith(".txt")]
instancias.sort()


tempos_por_tamanho = defaultdict(lambda: defaultdict(list))


print("MEDINDO TEMPOS DAS HEURÍSTICAS")
print()


# EXECUTA TUDO

for idx, instancia in enumerate(instancias, 1):

    print(f"Processando {idx}/{len(instancias)}: {instancia}")
    
    caminho = os.path.join(pasta_instancias, instancia)

    R, Pi, Sij = file_handling(caminho)

    tamanho = R

    for nome, metodo in solvers.items():

        inicio = time.perf_counter()

        mk, seq = metodo(R, Pi, Sij)

        fim = time.perf_counter()

        tempo = fim - inicio

        tempos_por_tamanho[tamanho][nome].append(tempo)


print()
print("TABELA DE TEMPO MÉDIO (SEGUNDOS)")
print()

# CABEÇALHO

header = f"{'Instâncias':<12}"

for sem, com in pares:
    header += f"{com:>12}"

print(header)
print("-" * 80)



tamanhos = sorted(tempos_por_tamanho.keys())

for tamanho in tamanhos:

    linha = f"N={tamanho:<8}"
    
    for sem, com in pares:
        
        #((tempo com - tempo sem) / tempo sem) 

        tempos_sem = tempos_por_tamanho[tamanho][sem]
        tempos_com = tempos_por_tamanho[tamanho][com]

        proporcoes = []
        for t_sem, t_com in zip(tempos_sem, tempos_com):

            if t_sem > 0:
                prop = ((t_com - t_sem) / t_sem) * 100
            else:
                prop = 0.0

            proporcoes.append(prop)
        
        media_prop = sum(proporcoes) / len(proporcoes)
        linha += f'{media_prop:>12.6f}'


    ##############################################
    # media_sem = sum(tempos_sem) / len(tempos_sem)
    # media_com = sum(tempos_com) / len(tempos_com)

    # diferenca = media_com - media_sem

    # linha += f"{diferenca:>12.4f}"
    ##############################################

    # media_tamanho = soma_prop / len(tamanho)
    # linha += f"{media_tamanho:>12.7f}"
    
    print(linha)


print()

#CSV

with open("tabela_tempos_2opt.csv", "w", newline="", encoding="utf-8-sig") as f:

    writer = csv.writer(f, delimiter=';')

    cabecalho = ["Instâncias"]

    for sem, _ in pares:
        cabecalho.append(sem)

    writer.writerow(cabecalho)

    for tamanho in tamanhos:

        linha_csv = [f"N={tamanho}"]

        for sem, com in pares:

            tempos_sem = tempos_por_tamanho[tamanho][sem]
            tempos_com = tempos_por_tamanho[tamanho][com]

            proporcoes = []

            for t_sem, t_com in zip(tempos_sem, tempos_com):

                if t_sem > 0:
                    prop = ((t_com - t_sem) / t_sem) * 100
                else:
                    prop = 0.0

                proporcoes.append(prop)

            media_prop = sum(proporcoes) / len(proporcoes)

            linha_csv.append(f"{media_prop:.2f}")

        writer.writerow(linha_csv)


print()


print("ESTATÍSTICAS GERAIS")
print()

for sem, com in pares:

    todos_sem = []
    todos_com = []

    for tamanho in tamanhos:

        todos_sem.extend(tempos_por_tamanho[tamanho][sem])
        todos_com.extend(tempos_por_tamanho[tamanho][com])

    media_sem = sum(todos_sem) / len(todos_sem)
    media_com = sum(todos_com) / len(todos_com)

    aumento = media_com - media_sem

    percentual = (aumento / media_sem) * 100 if media_sem > 0 else 0

    print(f"{sem}")
    print(f"  Média sem 2-opt : {media_sem:.6f} s")
    print(f"  Média com 2-opt : {media_com:.6f} s")
    print(f"  Diferença       : {aumento:.6f} s")
    print(f"  Aumento (%)     : {percentual:.2f}%")
    print()