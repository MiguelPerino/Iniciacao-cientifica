from main import resolve_todas_instancias, makespan
import random

def solver(R, Pi, Sij):
    n = R
    melhor_makespan_global = float('inf')
    melhor_seq_global = None
    # executa a heurística várias vezes (10 iterações para ter boas chances)
    
    for _ in range(n):
        primeiro = random.randint(0, n - 1)
        
        disponiveis = [j for j in range(n) if j != primeiro]
        
        segundo = random.choice(disponiveis)
        disponiveis.remove(segundo)
        
        seq = [primeiro, segundo]
        
        while disponiveis:
            new_job = random.choice(disponiveis)
            disponiveis.remove(new_job)
            
            #melhor posição
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
        
        mk = makespan(Sij, Pi, seq)
        
        if mk < melhor_makespan_global:
            melhor_makespan_global = mk
            melhor_seq_global = seq.copy()
    
    return melhor_makespan_global, melhor_seq_global


if __name__ == '__main__':
    resolve_todas_instancias('instancias', 'solucoesRandomInsertion', solver)
