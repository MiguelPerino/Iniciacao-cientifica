import csv
from collections import defaultdict

print("=" * 80)
print("ANÁLISE DE GAP DO 2-OPT POR TAMANHO DE INSTÂNCIA")
print("=" * 80)
print()

file = 'comparacao.csv'

pares = [
    ("FarthestInsertion", "FarthestInsertion+2opt", "FI"),
    ("NearestNeighbor", "NearestNeighbor+2opt", "NN"),
    ("NearestInsertion", "NearestInsertion+2opt", "NI"),
    ("CheapestInsertion", "CheapestInsertion+2opt", "CI"),
    ("RandomInsertion", "RandomInsertion+2opt", "RI"),
    ("SPT", "SPT+2opt", "SPT"),
]

# Estrutura: tamanho -> heuristica -> [lista de gaps]
gaps_por_tamanho = defaultdict(lambda: defaultdict(list))

qty_instancias = defaultdict(int)
with open(file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    
    for row in reader:
        # Pega o tamanho da instância
        tamanho = int(row['Tamanho'])
        qty_instancias[tamanho] += 1
        # Para cada par de heurísticas
        for sem_2opt, com_2opt, nome_curto in pares:
            mk_sem = int(row[sem_2opt])
            mk_com = int(row[com_2opt])
            
            if mk_sem > 0:
                gap = ((mk_sem - mk_com) / mk_sem) * 100
            else:
                gap = 0.0
            
            gaps_por_tamanho[tamanho][nome_curto].append(gap)

# Calcula médias
tamanhos = sorted(gaps_por_tamanho.keys())
nomes_heuristicas = [p[2] for p in pares]

print("TABELA DE GAP MÉDIO (%) - MELHORIA DO 2-OPT")
print("=" * 80)
print()

# Cabeçalho
header = f"{'Instâncias':<12}"
for nome in nomes_heuristicas:
    header += f"{nome:>10}"
print(header)
print("-" * 80)

# Dados
for tamanho in tamanhos:
    linha = f"N={tamanho:<8}"
    
    for nome in nomes_heuristicas:
        if nome in gaps_por_tamanho[tamanho]:
            gaps = gaps_por_tamanho[tamanho][nome]
            media_gap = sum(gaps) / len(gaps)
            linha += f"{media_gap:>11.2f}"
        else:
            linha += f"{'N/A':>10}"
    
    print(linha)

print("=" * 80)
print()

# Salva em CSV também

with open('tabela_gap_2opt.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f, delimiter=';')
    
    # Cabeçalho
    header_csv = ['Instâncias'] + nomes_heuristicas
    writer.writerow(header_csv)
    
    # Dados
    for tamanho in tamanhos:
        linha_csv = [f'N={tamanho}']
        
        for nome in nomes_heuristicas:
            if nome in gaps_por_tamanho[tamanho]:
                gaps = gaps_por_tamanho[tamanho][nome]
                media_gap = sum(gaps) / len(gaps)
                linha_csv.append(f'{media_gap:.2f}')
            else:
                linha_csv.append('N/A')
        
        writer.writerow(linha_csv)

print()

# Estatísticas adicionais
print("=" * 80)
print("ESTATÍSTICAS GERAIS")
print("=" * 80)
print()

for nome in nomes_heuristicas:
    todos_gaps = []
    for tamanho in tamanhos:
        if nome in gaps_por_tamanho[tamanho]:
            todos_gaps.extend(gaps_por_tamanho[tamanho][nome])
    
    if todos_gaps:
        media_geral = sum(todos_gaps) / len(todos_gaps)
        max_gap = max(todos_gaps)
        min_gap = min(todos_gaps)
        
        print(f"{nome}:")
        print(f"  Média geral: {media_geral:.2f}%")
        print(f"  Melhor caso: {max_gap:.2f}%")
        print(f"  Pior caso:   {min_gap:.2f}%")
        print(f"  Total inst:  {len(todos_gaps)}")
        print()

print("=" * 80)

for tamanho in sorted(qty_instancias):
    qtd = qty_instancias[tamanho]
    print(f"N={tamanho}: {qtd} instâncias")