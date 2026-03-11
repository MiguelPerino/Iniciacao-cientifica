''' Fazer algo como TwoOpt, aprimorar um que ja existe, algo relacionado com SPT ou alguma heuristica e melhorar ele
pegar oque o SPT - Ou outra heurisitica - faz e tentar dar um increase

SPT puro só olha para Pi (tempo de processamento)
Mas ignora os tempos de setup Sij entre jobs


custo[job] = Pi[job] + penalidade_setup[job]
penalidade_setup[job] pode ser:

alguns da literatura:
    Média dos setups: soma(Sij[job]) / n
    Máximo setup: max(Sij[job])
    Soma total: soma(Sij[job])
    Peso balanceado (50%-50%):
    custo[job] = 0.5 * Pi[job] + 0.5 * média(Sij[job])
ai depois ordena por ordem de job com menor custo

pensei em pegar alguma heuristica e fazer um mixed, por exemplo com penalidade_setup escrito acima, fazer com media, maximo e soma por exemplo,
algo que faça sentido para diminuir o makespan



'''