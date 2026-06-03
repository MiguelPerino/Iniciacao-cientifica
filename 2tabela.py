import csv
from collections import defaultdict

file = 'comparacao.csv'

heuristicas = [
    "FarthestInsertion+2opt",
    "NearestNeighbor+2opt",
    "NearestInsertion+2opt",
    "CheapestInsertion+2opt",
    "RandomInsertion+2opt",
]
mapa_nomes = {
    "FarthestInsertion+2opt": "FI+2opt",
    "NearestNeighbor+2opt": "NN+2opt",
    "NearestInsertion+2opt": "NI+2opt",
    "CheapestInsertion+2opt": "CI+2opt",
    "RandomInsertion+2opt": "RI+2opt",
}

# estrutura:
gaps_por_tamanho = defaultdict(lambda: defaultdict(list))

# quantidade de instâncias por tamanho
quantidade_instancias = defaultdict(int)

with open(file, 'r', encoding='utf-8-sig') as f:

    reader = csv.DictReader(f, delimiter=';')

    for row in reader:

        tamanho = int(row['Tamanho'])

        quantidade_instancias[tamanho] += 1

        # pega makespans de TODAS heurísticas da instância
        makespans = {}

        for coluna in row:

            if coluna in ['Instância', 'Tamanho']:
                continue

            if "Melhoria%" in coluna:
                continue

            makespans[coluna] = int(row[coluna])

        # melhor solução da instância
        best = min(makespans.values())

        # calcula gap das heurísticas escolhidas
        for heuristica in heuristicas:

            mk = makespans[heuristica]

            if best > 0:
                gap = ((mk - best) / best) * 100
            else:
                gap = 0.0

            gaps_por_tamanho[tamanho][heuristica].append(gap)


###############################################
tamanhos = sorted(gaps_por_tamanho.keys())

print("TABELA DE GAP MÉDIO (%)")
print("=" * 80)
print()

# cabeçalho
header = f"{'Instâncias':<12}{'Qtd':<8}"

for heuristica in heuristicas:
    nome_curto = mapa_nomes[heuristica]
    header += f"{nome_curto:>12}"

print(header)
print("-" * 80)

# linhas
for tamanho in tamanhos:

    qtd = quantidade_instancias[tamanho]

    linha = f"N={tamanho:<8}{qtd:<8}"

    for heuristica in heuristicas:

        gaps = gaps_por_tamanho[tamanho][heuristica]

        media_gap = sum(gaps) / len(gaps)

        linha += f"{media_gap:>12.2f}"

    print(linha)


###############################################

with open(
    "tabela_gap_best.csv", "w", newline="", encoding="utf-8-sig") as f:

    writer = csv.writer(f, delimiter=';')

    # cabeçalho
    cabecalho = ["Instâncias", "Qtd"]

    for heuristica in heuristicas:
        cabecalho.append(mapa_nomes[heuristica])

    writer.writerow(cabecalho)

    # dados
    for tamanho in tamanhos:

        qtd = quantidade_instancias[tamanho]

        linha_csv = [f"N={tamanho}", qtd]

        for heuristica in heuristicas:

            gaps = gaps_por_tamanho[tamanho][heuristica]

            media_gap = sum(gaps) / len(gaps)

            linha_csv.append(f"{media_gap:.2f}")

        writer.writerow(linha_csv)

print('deu certo')