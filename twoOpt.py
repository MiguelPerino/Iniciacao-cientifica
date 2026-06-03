# def aplicar_2opt(sequencia, Sij, Pi, makespan_func):
#     """   
#     sequencia: lista com a ordem dos jobs (solução inicial)
#     makespan_func: função que calcula o makespan
#     sequencia melhorada
#     """
#     n = len(sequencia)
#     melhorou = True
    
#     while melhorou:
#         melhorou = False
#         melhor_makespan = makespan_func(Sij, Pi, sequencia)
        
#         # tenta todas as possíveis trocas 2-opt
#         for i in range(n - 1):
#             for j in range(i + 2, n):
#                 # cria nova sequência invertendo o segmento entre i e j
#                 nova_seq = sequencia[:i+1] + sequencia[i+1:j+1][::-1] + sequencia[j+1:]
                
#                 # Calcula o makespan da nova sequência
#                 novo_makespan = makespan_func(Sij, Pi, nova_seq)
                
#                 # se melhorou dai aceita a mudança
#                 if novo_makespan < melhor_makespan:
#                     sequencia = nova_seq
#                     melhor_makespan = novo_makespan
#                     melhorou = True
#                     break
            
#             if melhorou:
#                 break
    
#     return sequencia


##########################
#best improvement


def aplicar_2opt(sequencia, Sij, Pi, makespan_func):
    n = len(sequencia)
    melhor_seq = sequencia.copy()
    melhor_makespan = makespan_func(Sij, Pi, melhor_seq)

    melhorou = True

    while True:
        melhorou = False
        melhor_candidato = melhor_seq.copy()
        melhor_valor = melhor_makespan

        for i in range(n - 1):
            for j in range(i + 2, n):

                nova_seq = (
                    melhor_seq[:i+1] +
                    melhor_seq[i+1:j+1][::-1] +
                    melhor_seq[j+1:]
                )

                novo_makespan = makespan_func(Sij, Pi, nova_seq)

                if novo_makespan < melhor_valor:
                    melhor_candidato = nova_seq.copy()
                    melhor_valor = novo_makespan
                    melhorou = True

        if melhorou:
            melhor_seq = melhor_candidato.copy()
            melhor_makespan = melhor_valor
        else:
            break

    return melhor_seq