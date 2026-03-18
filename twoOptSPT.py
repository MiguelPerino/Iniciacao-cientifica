from main import resolve_todas_instancias, makespan
from spt import solver as spt_solver
from twoOpt import aplicar_2opt

def solver(R, Pi, Sij):
    #usa o Random Insertion original para gerar solução inicial
    mk_inicial, sequencia = spt_solver(R, Pi, Sij)

    #melhora a solução com 2-opt
    sequencia = aplicar_2opt(sequencia, Sij, Pi, makespan)
    
    #calcula novo makespan e retorna
    mk_final = makespan(Sij, Pi, sequencia)
    
    return mk_final, sequencia


if __name__ == '__main__':
    resolve_todas_instancias('instancias', 'solucoes2OptSPT', solver)
