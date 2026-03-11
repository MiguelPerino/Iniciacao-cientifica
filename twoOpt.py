from main import resolve_todas_instancias, makespan
#2opt para nearest neighbor
def solver(R, Pi, Sij):
    n = R
    melhor_makespan_global = float('inf')
    melhor_seq_global = None
    
    # Testa começando de cada job diferente
    for inicio in range(n):
        # Gera solução inicial usando nearest neighbor
        sequencia = nearest_neighbor_inicial(n, Sij, inicio)
        
        # Aplica 2-opt para melhorar a solução
        melhorou = True
        while melhorou:
            melhorou = False
            melhor_makespan = makespan(Sij, Pi, sequencia)
            
            # Tenta todas as possíveis trocas 2-opt
            for i in range(n - 1):
                for j in range(i + 2, n):
                    '''Cria nova sequência invertendo o segmento entre i e j    suponho seq [0,1,2,3,4,5]
                    a primeira parte pega tudo antes do i + 1 (ent qnd for i = 1, sequencia[:2] = [0,1])
                    segunda parte pega a parte que vai ser invertida, qnd i = 1, j vai ser 3, sequencia[2:4] - tem [2, 3] para inverter
                    terceira parte pega tudo depois do segmento invertido, j=3, seq[4:] - tem [4, 5] 
                    [0,1,3,2,4,5] nova_sequencia
                    '''
                    nova_seq = sequencia[:i+1] + sequencia[i+1:j+1][::-1] + sequencia[j+1:]
                    
                    novo_makespan = makespan(Sij, Pi, nova_seq)
                    
                    # Se melhorou, aceita a mudança
                    if novo_makespan < melhor_makespan:
                        sequencia = nova_seq
                        melhor_makespan = novo_makespan
                        melhorou = True
                        break
                
                if melhorou:
                    break
        
        # Verifica se essa solução é a melhor até agora
        mk = makespan(Sij, Pi, sequencia)
        if mk < melhor_makespan_global:
            melhor_makespan_global = mk
            melhor_seq_global = sequencia.copy()
    
    return melhor_makespan_global, melhor_seq_global


def nearest_neighbor_inicial(n, Sij, inicio=0):
    visitados = [False] * n
    sequencia = []
    
    atual = inicio
    visitados[atual] = True
    sequencia.append(atual)
    
    while len(sequencia) < n:
        melhor_prox = None
        melhor_custo = float('inf')
        
        for j in range(n):
            if not visitados[j]:
                custo = Sij[atual][j]
                if custo < melhor_custo:
                    melhor_custo = custo
                    melhor_prox = j
        
        sequencia.append(melhor_prox)
        visitados[melhor_prox] = True
        atual = melhor_prox
    
    return sequencia


if __name__ == '__main__':
    resolve_todas_instancias('instancias', 'solucoes2Opt', solver)