#Menor aumento de custo

from main import resolve_todas_instancias, makespan
    
def solver(R, Pi, Sij):

    n = R

    #pegar o primeiro job, somando o setup de todos e ver qual o mais 'caro
    soma_setups = [sum(linha) for linha in Sij]

    #testar pra ver se pega o .index usando max
    primeiro = soma_setups.index(max(soma_setups))

    seq = [primeiro]
    visitados = [False] * n

    visitados[primeiro] = True

    while len(seq) < n:
        melhor_pos = None
        melhor_job = None
        menor_custo = float('inf')

        for job in range(n):
            if visitados[job]:
                continue

            for pos in range(len(seq) + 1):
                if pos == 0:
                    custo = Sij[job][seq[0]] + Pi[job]
                elif pos == len(seq):
                    last = seq[-1]
                    custo = Sij[last][job] + Pi[job]
                else:
                    ant = seq[pos - 1]
                    prox = seq[pos]
                    custo = (Sij[ant][job] + Pi[job] + Sij[job][prox] - Sij[ant][prox])
                
                if custo < menor_custo:
                    menor_custo = custo
                    melhor_pos = pos
                    melhor_job = job
        #acha o melhor custo e o melhor job e a melhor posição

        #agora colocar ela na seq
        seq.insert(melhor_pos, melhor_job)
        visitados[melhor_job] = True

    return makespan(Sij, Pi, seq), seq


if __name__ == '__main__':
    resolve_todas_instancias("instancias", "solucoesCheapestInsertion", solver)


