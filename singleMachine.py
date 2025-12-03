import os

def file_handling (path_instancia):
    R = None
    Pi = []
    Sij = []

    with open(path_instancia, 'r', encoding='utf-8') as instancia:
        for line in instancia:
            line = line.strip()
            if not line:
                continue

            #Lê e guarda o r
            if line.startswith('R'):
                R = int(line.split('=')[1])

            #Lê e guarda o Pi
            elif line.startswith('Pi'):
                elements = line.split('=')[1].strip('()')
                Pi = [int(e) for e in elements.split(',')]
            
            #Lê e guarda o Sij
            elif line.startswith('Sij='):
                for line_sij in instancia:
                    line_sij = line_sij.strip()
                    if not line_sij:
                        continue

                    Sij.append([int(e.strip()) for e in line_sij.split(',')])
                    if len(Sij) == len(Pi):
                        break
        
    return R, Pi, Sij


def solver(R, Pi, Sij):
    n = R #número de tarefas
    visitados = [False] * n #qntd de tarefas, tudo com false, para depois ir validando
    sequencia = []  #sequencia das tarefas
    # Testar todos os inícios possíveis e retornar o melhor deles
    atual = 0   #começa no primeiro
    visitados[atual] = True #valida já o primeiro como true
    sequencia.append(atual) #ja começa a lista 'sequencia' com o primeiro job 

    while len(sequencia) < n:   #enquanto qntd de tarefas de 'sequencia' for menor que a qntd de tarefa total
        melhor_prox_tarefa = None
        melhor_custo = float('inf')

        for j in range(len(Sij)):
            if visitados[j] == False:
                # Para definir a próxima tarefa, só olhe o tempo de setup
                custo_cada_tarefa = Sij[atual][j] + Pi[j]   #soma o custo de ir para o prox job com o tempo de processamento
                if custo_cada_tarefa < melhor_custo:
                    melhor_custo = custo_cada_tarefa
                    melhor_prox_tarefa = j
            
        sequencia.append(melhor_prox_tarefa)
        visitados[melhor_prox_tarefa] = True    #valida como true
        atual = melhor_prox_tarefa  #atualiza para o prox job e reinicia o loop

    # O cálculo do makespan poderia estar numa função a parte pra você poder reaproveitar nos demais algoritmos

    return sequencia, Sij, Pi


def makespan(Sij, Pi, sequencia):
    makespan = 0
    for i in range(1, len(Sij)):
        i_ant = sequencia[i-1]  #pega o indice(job) anterior da lista sequencia 
        i_atual = sequencia[i]  #pega o próximo indice(job) -atual- da lista sequencia

        makespan += Sij[i_ant][i_atual] + Pi[i_atual] #makespan é a soma do tempo de setup da troca dos jobs + o tempo de processamento
    return makespan

def save_results(result, file_to_save):
    with open(file_to_save, 'w', encoding='UTF-8') as f:
        sequencia = result[0]
        result_makespan = makespan(result[1], result[2], sequencia)
        f.write(f"MAKESPAN;{result_makespan}\n")
        f.write(f"{sequencia[0]}")
        for idx in sequencia[1:]:
            f.write(f";{idx}")


def resolve_instancia(arq_instancia, arq_solucao):
    # Aqui dentro abre qualquer arquivo de instância, resolve e salva no arquivo de solução
    R, pi, Sij = file_handling(arq_instancia)
    result = solver(R, pi, Sij)

    save_results(result, arq_solucao)
    print(f'Resolvido: {arq_instancia} -> {arq_solucao}')


def resolve_todas_instancias(pasta_instancias, pasta_solucoes):
    instancias = os.listdir(pasta_instancias)
    instancias.sort()
    for instancia in instancias:
        arq_instancia = os.path.join(pasta_instancias, instancia)
        arq_solucao = os.path.join(pasta_solucoes, instancia)
    
        resolve_instancia(arq_instancia, arq_solucao)


if __name__ == "__main__":
    # with open('instancias.txt', mode='r', encoding='UTF-8') as instancia:
    #     tratado = file_handling(instancia)
    #     r, Pi, Sij = tratado

    # result = solver(r, Pi, Sij)
    # save_results(result, 'sequencia.txt')
    resolve_todas_instancias("instancias", "solucoes")
