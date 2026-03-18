'''
antigo save results
o novo agora compara com as heuristicas 2opt
este dfeixei para caso precisa mudar alguam coisa ou implementar alguma nova comparação
'''

from farthestInsertion import solver as fi_solver
from main import solver as sm_solver, file_handling
from nearestInsertion import solver as ni_solver
from cheapestInserton import solver as ci_solver
from twoOptNearestNeighbor import solver as twoOptNearestNeighbor_solver
from randomInsertion import solver as random_solver
from spt import solver as spt_solver
from twoOptRandomInsertion import solver as twooptrandom

import os
import csv

solvers = {
    "FarthestInsertion": fi_solver,
    "NearestNeighbor": sm_solver,
    "NearestInsertion": ni_solver,
    "CheapestInsertion": ci_solver,
    "twoOptNearestNeighbor": twoOptNearestNeighbor_solver,
    "RandomInsertion": random_solver,
    "spt": spt_solver,
    "twoopt_random": twooptrandom
}

pasta_instancias = "instancias"
instancias = sorted(os.listdir(pasta_instancias))


with open("comparacao.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Instância", "Método", "Makespan", "Sequência"])

    for instancia in instancias: 
        caminho = os.path.join(pasta_instancias, instancia)

        R, Pi, Sij = file_handling(caminho)

        for nome, metodo in solvers.items():
            mk, seq = metodo(R, Pi, Sij)
            writer.writerow([instancia, nome, mk, seq])

