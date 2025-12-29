from main import resolve_todas_instancias, makespan

def solver(R, Pi, Sij):
    n = R

    soma_setups = []
    for _, linha in enumerate(Sij):
        soma_setups.append(sum(linha))

    primeiro = None
    maior_valor = -1

    for i, valor in enumerate(soma_setups):
        if valor > maior_valor:
            maior_valor = valor
            primeiro = i

    segundo = None
    melhor = float('inf')
    for j, valor in enumerate(Sij):
        if j != primeiro and Sij[primeiro][j] < melhor: #menor por que queremos a cidade mais perto da primeira
            melhor = Sij[primeiro][j]
            segundo = j 
    
    seq = [primeiro, segundo]
    visitados = [False] * n
    visitados[primeiro] = True
    visitados[segundo] = True
    

    while len(seq) < n:
        distancia = []
        for j in range(n):
            if not visitados[j]:
                menor_dist = min(Sij[j][k] for k in seq)
                distancia.append((menor_dist, j))
        
        _, new_job = min(distancia)

        melhor_pos = 0
        melhor_custo = float('inf')

        for pos in range(len(seq) + 1):
            if pos == 0:
                custo = Sij[new_job][seq[0]] + Pi[new_job]
            elif pos == len(seq):
                last = seq[-1]
                custo = Sij[last][new_job] + Pi[new_job]
            else:
                ant = seq[pos - 1]
                prox = seq[pos]
                custo = (Sij[ant][new_job] + Pi[new_job] + Sij[new_job][prox] - Sij[ant][prox])
            
            if custo < melhor_custo:
                melhor_custo = custo
                melhor_pos = pos
        
        seq.insert(melhor_pos, new_job)
        visitados[new_job] = True

    return makespan(Sij, Pi, seq), seq

if __name__ == '__main__':
    resolve_todas_instancias('instancias', 'solucoesNearest', solver)