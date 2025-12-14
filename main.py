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
    melhor_makespan = float('inf')
    melhor_seq = None


    for i in range(n):
        visitados = [False] * n #qntd de tarefas, tudo com false, para depois ir validando
        sequencia = []  #sequencia das tarefas

        atual = i
        visitados[atual] = True 
        sequencia.append(atual) 

        while len(sequencia) < n:   
            melhor_prox_tarefa = None
            melhor_custo = float('inf')

            for j in range(len(Sij)):
                if visitados[j] == False:
                
                    custo_cada_tarefa = Sij[atual][j] 
                    if custo_cada_tarefa < melhor_custo:
                        melhor_custo = custo_cada_tarefa
                        melhor_prox_tarefa = j

            sequencia.append(melhor_prox_tarefa)
            visitados[melhor_prox_tarefa] = True
            atual = melhor_prox_tarefa 

        mk = makespan(Sij, Pi, sequencia)  

        if mk < melhor_makespan:
            melhor_makespan = mk
            melhor_seq = sequencia.copy()

    return melhor_makespan, melhor_seq


def makespan(Sij, Pi, sequencia):
    makespan = Pi[sequencia[0]] #começa com o tempo de processamento do primeiro job
    for i in range(1, len(sequencia)):
        i_ant = sequencia[i-1]  #pega o indice(job) anterior da lista sequencia 
        i_atual = sequencia[i]  #pega o próximo indice(job) -atual- da lista sequencia

        makespan += Sij[i_ant][i_atual] + Pi[i_atual] #makespan é a soma do tempo de setup da troca dos jobs + o tempo de processamento
    return makespan


def save_results(result, file_to_save):
    with open(file_to_save, 'w', encoding='UTF-8') as f:
        result_makespan = result[0]
        sequencia = result[1]
        f.write(f"MAKESPAN;{result_makespan}\n")
        f.write(f"{sequencia[0]}")
        for idx in sequencia[1:]:
            f.write(f";{idx}")


def resolve_instancia(arq_instancia, arq_solucao, solver_func):
    # Aqui dentro abre qualquer arquivo de instância, resolve e salva no arquivo de solução
    R, pi, Sij = file_handling(arq_instancia)
    result = solver_func(R, pi, Sij)

    save_results(result, arq_solucao)
    print(f'Resolvido: {arq_instancia} -> {arq_solucao}')


def resolve_todas_instancias(pasta_instancias, pasta_solucoes, solver_func):
    instancias = os.listdir(pasta_instancias)
    instancias = instancias[0:]
    instancias.sort()
    for instancia in instancias:
        arq_instancia = os.path.join(pasta_instancias, instancia)
        arq_solucao = os.path.join(pasta_solucoes, instancia)
    
        resolve_instancia(arq_instancia, arq_solucao, solver_func)


if __name__ == "__main__":
    # resolve_todas_instancias(r"C:\Users\Win 10\Downloads\SDSTsDP_Data\SDSTsDP_Data\BenchmarkData", "solucoes")
    resolve_todas_instancias('instancias', 'solucoesSingleMachine', solver)