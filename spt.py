from main import resolve_todas_instancias, makespan

def solver(R, Pi, Sij):
    n = R

    #precisamos pegar os jobs e o tempo de process
    jobs_com_tempo = []
    for i in range(n):
        jobs_com_tempo.append((Pi[i], i)) #pi[i] é o tempo e i é o job
    
    #spt tem que ordenar
    jobs_com_tempo.sort()

    #agora montar a sequencia, temos ja a lista com job e tempo
    seq = [job[1] for job in jobs_com_tempo]

    return makespan(Sij, Pi, seq), seq

if '__main__' == __name__:
    resolve_todas_instancias('instancias', 'solucoesSPT', solver)