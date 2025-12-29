from main import file_handling, save_results, resolve_instancia, resolve_todas_instancias, makespan


def solver(R, Pi, Sij):
    n = R
    #Preciso pegar o primeiro Job
    #entao da para somar o setup total de cada job (cada linha) e ver qual é mais cara
    #depois pego o indice (que é o primeiro job)
    soma_setups = []
    for i, linha in enumerate(Sij):
        soma_setups.append(sum(linha))
    
    primeiro = None
    maior_valor = -1

    for i, valor in enumerate(soma_setups):
        if valor > maior_valor:
            maior_valor = valor
            primeiro = i
       
    #Para o segundo job, ver qual é mais longe do primeiro
    segundo = None
    melhor = -1
    for j in range (len(Sij)):
        if j != primeiro and Sij[primeiro][j] > melhor:
            melhor = Sij[primeiro][j]
            segundo = j

    seq = [primeiro, segundo]
    visitados = [False] * n
    visitados[primeiro] = True  
    visitados[segundo] = True
    #achar a cidade mais longe entre a sequencia
    while len(seq) < n:

        distancia = []
        for j in range(n):
            if not visitados[j]:
                maior_dist = max(Sij[j][k] for k in seq)
                distancia.append((maior_dist, j))
        
        _, new_job = max(distancia)


        #inserir o new_job na melhor posição
        #preciso verificar se a melhor posição, se é no começo da lista, no meio ou no final
        #pensei em fazer um if posicao == 0, elif pos == len(seq) para o ultimo elemento, e else, com uma verificação para o meio
        #e depois comparar o custo de cada posicao para ver o melhor custo e a melhor pos
        melhor_pos = 0
        melhor_custo = float('inf')

        for pos in range(len(seq) + 1):
            if pos == 0:
                custo = Sij[new_job][seq[0]] + Pi[new_job]
            elif pos == len(seq):
                last = seq[-1]
                custo = Pi[new_job] + Sij[last][new_job]
            else:
                ant = seq[pos - 1]
                prox = seq[pos]
                custo = (Sij[ant][new_job] + Pi[new_job] + Sij[new_job][prox] - Sij[ant][prox])

            if custo < melhor_custo:
                melhor_custo = custo
                melhor_pos = pos

        seq.insert(melhor_pos, new_job)
        visitados[new_job] = True
    
    #mudanças tsp (que muda do tsp para o problema de engenharia de produção)

    return makespan(Sij, Pi, seq), seq

if __name__ == '__main__':
    resolve_todas_instancias("instancias", "solucoesFarthest", solver)
    