from main import makespan, resolve_todas_instancias
from farthestInsertion import solver as farthest_solver
from twoOpt import aplicar_2opt

def solver(R, Pi, Sij):
    mk_inicial, sequencia = farthest_solver(R, Pi, Sij)

    sequencia = aplicar_2opt(sequencia, Sij, Pi, makespan)


    #aqui resolve o makespan da sequencia com o 2Opt aplicado ja
    mk_final = makespan(Sij, Pi, sequencia)

    return mk_final, sequencia

if __name__ == '__main__':
    resolve_todas_instancias('instancias', 'solucoes2OptFarthestInsertion', solver)
