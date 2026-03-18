def aplicar_2opt(sequencia, Sij, Pi, makespan_func):
    """   
    sequencia: lista com a ordem dos jobs (solução inicial)
    makespan_func: função que calcula o makespan
    sequencia melhorada
    """
    n = len(sequencia)
    melhorou = True
    
    while melhorou:
        melhorou = False
        melhor_makespan = makespan_func(Sij, Pi, sequencia)
        
        # tenta todas as possíveis trocas 2-opt
        for i in range(n - 1):
            for j in range(i + 2, n):
                # cria nova sequência invertendo o segmento entre i e j
                nova_seq = sequencia[:i+1] + sequencia[i+1:j+1][::-1] + sequencia[j+1:]
                
                # Calcula o makespan da nova sequência
                novo_makespan = makespan_func(Sij, Pi, nova_seq)
                
                # se melhorou dai aceita a mudança
                if novo_makespan < melhor_makespan:
                    sequencia = nova_seq
                    melhor_makespan = novo_makespan
                    melhorou = True
                    break
            
            if melhorou:
                break
    
    return sequencia
