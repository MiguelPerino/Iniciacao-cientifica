from farthestInsertion import solver as fi_solver
from main import solver as sm_solver, file_handling

import os
import csv

solvers = {
    "FarthestInsertion": fi_solver,
    "SingleMachine": sm_solver
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
