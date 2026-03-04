import pandas as pd
from scipy import stats
import numpy as np

# 1. Base de dados consolidada
data = {
    'Script': ['belief_prop', 'cvar', 'fft', 'gauss_legendre', 'heat_dist', 'look_and_say'],
    
    'Mono_LOC': [15, 26, 13, 14, 15, 30],
    'Mono_Nodes': [327, 243, 19, 26, 27, 151],
    'Mono_Edges': [386, 359, 22, 27, 30, 455],
    'Mono_Path':  [165, np.nan, 6, 12, 8, np.nan],
    
    'Claude_LOC': [34, 43, 32, 32, 29, 43],
    'Claude_Nodes': [37, 128, 19, 16, 14, 18],
    'Claude_Edges': [57, 136, 20, 15, 24, 16],
    'Claude_Path':  [5, 7, 5, 5, 3, 4],
    
    'Orig_LOC': [23, 28, 22, 24, 18, 33],
    'Orig_Nodes': [37, 123, 19, 16, 11, 6],
    'Orig_Edges': [56, 121, 20, 15, 12, 4],
    'Orig_Path':  [5, 4, 5, 5, 3, 2]
}

df = pd.DataFrame(data)

def fmt(val):
    return "N/A (ciclo)" if pd.isna(val) else f"{int(val)}"

def get_trend_str(v_mono, v_modu, metric):
    if pd.isna(v_mono) or pd.isna(v_modu):
        return "Resolvido" if pd.isna(v_mono) and not pd.isna(v_modu) else ""
    diff = v_modu - v_mono
    if metric == "LOC":
        return f"(Aumentou {diff:+} linhas)"
    else:
        perc = (diff / v_mono) * 100 if v_mono != 0 else 0
        if diff < 0:
            return f"(Reduziu {abs(diff):.0f} | {perc:.1f}%)"
        elif diff == 0:
            return "(Manteve)"
        else:
            return f"(Aumentou {diff})"

def get_trend_num(v_mono, v_modu):
    if pd.isna(v_mono) or pd.isna(v_modu):
        return None, None
    diff = v_modu - v_mono
    perc = (diff / v_mono) * 100 if v_mono != 0 else 0
    return diff, perc

# ---------------------------------------------------------
# CONSTRUINDO A STRING MD E A IMPRESSÃO
# ---------------------------------------------------------
output_md = []
output_md.append("# Resultados da Análise de Modularização e Proveniência\n")
output_md.append("## 1. ANÁLISE DESCRITIVA AOS PARES (REDUÇÃO/AUMENTO)\n")

print("============================================================")
print(" 1. ANÁLISE DESCRITIVA AOS PARES (REDUÇÃO/AUMENTO)")
print("============================================================")

# Preparando lista para exportar CSV/TSV
csv_data = []

for index, row in df.iterrows():
    script = row['Script'].upper()
    
    print(f"\n--- EXPERIMENTO: {script} ---")
    output_md.append(f"### Experimento: `{script}`\n")
    
    # [1] Monolithic vs IA Modular
    print(f" [1] Monolítico vs IA Modular (Claude)")
    print(f"     - LOC:   {fmt(row['Mono_LOC']):>11}  ->  {fmt(row['Claude_LOC']):<11} {get_trend_str(row['Mono_LOC'], row['Claude_LOC'], 'LOC')}")
    print(f"     - Nodes: {fmt(row['Mono_Nodes']):>11}  ->  {fmt(row['Claude_Nodes']):<11} {get_trend_str(row['Mono_Nodes'], row['Claude_Nodes'], 'Nodes')}")
    print(f"     - Edges: {fmt(row['Mono_Edges']):>11}  ->  {fmt(row['Claude_Edges']):<11} {get_trend_str(row['Mono_Edges'], row['Claude_Edges'], 'Edges')}")
    print(f"     - Path:  {fmt(row['Mono_Path']):>11}  ->  {fmt(row['Claude_Path']):<11} {get_trend_str(row['Mono_Path'], row['Claude_Path'], 'Path')}")
    
    output_md.append("**[1] Monolítico vs IA Modular (Claude)**\n")
    output_md.append(f"- **LOC:** {fmt(row['Mono_LOC'])} -> {fmt(row['Claude_LOC'])} {get_trend_str(row['Mono_LOC'], row['Claude_LOC'], 'LOC')}\n")
    output_md.append(f"- **Nodes:** {fmt(row['Mono_Nodes'])} -> {fmt(row['Claude_Nodes'])} {get_trend_str(row['Mono_Nodes'], row['Claude_Nodes'], 'Nodes')}\n")
    output_md.append(f"- **Edges:** {fmt(row['Mono_Edges'])} -> {fmt(row['Claude_Edges'])} {get_trend_str(row['Mono_Edges'], row['Claude_Edges'], 'Edges')}\n")
    output_md.append(f"- **Path:** {fmt(row['Mono_Path'])} -> {fmt(row['Claude_Path'])} {get_trend_str(row['Mono_Path'], row['Claude_Path'], 'Path')}\n\n")

    # [2] Monolithic vs Original
    print(f" [2] Monolítico vs Original (Humano)")
    print(f"     - LOC:   {fmt(row['Mono_LOC']):>11}  ->  {fmt(row['Orig_LOC']):<11} {get_trend_str(row['Mono_LOC'], row['Orig_LOC'], 'LOC')}")
    print(f"     - Nodes: {fmt(row['Mono_Nodes']):>11}  ->  {fmt(row['Orig_Nodes']):<11} {get_trend_str(row['Mono_Nodes'], row['Orig_Nodes'], 'Nodes')}")
    print(f"     - Edges: {fmt(row['Mono_Edges']):>11}  ->  {fmt(row['Orig_Edges']):<11} {get_trend_str(row['Mono_Edges'], row['Orig_Edges'], 'Edges')}")
    print(f"     - Path:  {fmt(row['Mono_Path']):>11}  ->  {fmt(row['Orig_Path']):<11} {get_trend_str(row['Mono_Path'], row['Orig_Path'], 'Path')}")
    
    output_md.append("**[2] Monolítico vs Original (Humano)**\n")
    output_md.append(f"- **LOC:** {fmt(row['Mono_LOC'])} -> {fmt(row['Orig_LOC'])} {get_trend_str(row['Mono_LOC'], row['Orig_LOC'], 'LOC')}\n")
    output_md.append(f"- **Nodes:** {fmt(row['Mono_Nodes'])} -> {fmt(row['Orig_Nodes'])} {get_trend_str(row['Mono_Nodes'], row['Orig_Nodes'], 'Nodes')}\n")
    output_md.append(f"- **Edges:** {fmt(row['Mono_Edges'])} -> {fmt(row['Orig_Edges'])} {get_trend_str(row['Mono_Edges'], row['Orig_Edges'], 'Edges')}\n")
    output_md.append(f"- **Path:** {fmt(row['Mono_Path'])} -> {fmt(row['Orig_Path'])} {get_trend_str(row['Mono_Path'], row['Orig_Path'], 'Path')}\n\n")

    # Guardar para Tabela
    diff_c_nodes, perc_c_nodes = get_trend_num(row['Mono_Nodes'], row['Claude_Nodes'])
    diff_o_nodes, perc_o_nodes = get_trend_num(row['Mono_Nodes'], row['Orig_Nodes'])
    diff_c_edges, perc_c_edges = get_trend_num(row['Mono_Edges'], row['Claude_Edges'])
    diff_o_edges, perc_o_edges = get_trend_num(row['Mono_Edges'], row['Orig_Edges'])

    csv_data.append({
        'Script': row['Script'],
        'Mono_LOC': row['Mono_LOC'], 'Claude_LOC': row['Claude_LOC'], 'Orig_LOC': row['Orig_LOC'],
        'Mono_Nodes': row['Mono_Nodes'], 'Claude_Nodes': row['Claude_Nodes'], 'Diff_Claude_Nodes': diff_c_nodes, 'Perc_Claude_Nodes': perc_c_nodes, 'Orig_Nodes': row['Orig_Nodes'], 'Diff_Orig_Nodes': diff_o_nodes, 'Perc_Orig_Nodes': perc_o_nodes,
        'Mono_Edges': row['Mono_Edges'], 'Claude_Edges': row['Claude_Edges'], 'Diff_Claude_Edges': diff_c_edges, 'Perc_Claude_Edges': perc_c_edges, 'Orig_Edges': row['Orig_Edges'], 'Diff_Orig_Edges': diff_o_edges, 'Perc_Orig_Edges': perc_o_edges,
        'Mono_Path': row['Mono_Path'], 'Claude_Path': row['Claude_Path'], 'Orig_Path': row['Orig_Path']
    })

df_export = pd.DataFrame(csv_data)

# ---------------------------------------------------------
# PARTE 2: WILCOXON (IMPRESSÃO E MD)
# ---------------------------------------------------------
def run_wilcoxon(metric_name, col_mono, col_modu):
    valid_data = df[[col_mono, col_modu]].dropna()
    diff = valid_data[col_mono] - valid_data[col_modu]
    valid_data = valid_data[diff != 0] 
    
    n_samples = len(valid_data)
    if n_samples == 0:
        return f"{metric_name:<25} | Sem diferença válida nas amostras para aplicar o teste"
        
    stat, p_value = stats.wilcoxon(valid_data[col_mono], valid_data[col_modu], alternative='two-sided')
    sig = "*" if p_value < 0.05 else ("+" if p_value < 0.10 else "")
    return f"{metric_name:<25} | N={n_samples} | W={stat:<4.1f} | P-valor: {p_value:.4f} {sig}"

print("\n\n============================================================")
print(" 2. RESULTADOS ESTATÍSTICOS (TESTE DE WILCOXON)")
print("============================================================")

output_md.append("---\n## 2. RESULTADOS ESTATÍSTICOS (TESTE DE WILCOXON)\n\n")

# Comparação 1
print("\n[COMPARAÇÃO 1: Monolítico vs IA Modular (Claude)]")
w_loc_1 = run_wilcoxon("Linhas de Código (LOC)", 'Mono_LOC', 'Claude_LOC')
w_nod_1 = run_wilcoxon("Nós do Grafo (Nodes)", 'Mono_Nodes', 'Claude_Nodes')
w_edg_1 = run_wilcoxon("Arestas (Edges)", 'Mono_Edges', 'Claude_Edges')
w_pth_1 = run_wilcoxon("Caminho Longo (Path)", 'Mono_Path', 'Claude_Path')

print(w_loc_1); print(w_nod_1); print(w_edg_1); print(w_pth_1)

output_md.append("### [COMPARAÇÃO 1: Monolítico vs IA Modular (Claude)]\n```text\n")
output_md.append(f"{w_loc_1}\n{w_nod_1}\n{w_edg_1}\n{w_pth_1}\n```\n\n")

# Comparação 2
print("\n[COMPARAÇÃO 2: Monolítico vs Original Humano]")
w_loc_2 = run_wilcoxon("Linhas de Código (LOC)", 'Mono_LOC', 'Orig_LOC')
w_nod_2 = run_wilcoxon("Nós do Grafo (Nodes)", 'Mono_Nodes', 'Orig_Nodes')
w_edg_2 = run_wilcoxon("Arestas (Edges)", 'Mono_Edges', 'Orig_Edges')
w_pth_2 = run_wilcoxon("Caminho Longo (Path)", 'Mono_Path', 'Orig_Path')

print(w_loc_2); print(w_nod_2); print(w_edg_2); print(w_pth_2)

output_md.append("### [COMPARAÇÃO 2: Monolítico vs Original Humano]\n```text\n")
output_md.append(f"{w_loc_2}\n{w_nod_2}\n{w_edg_2}\n{w_pth_2}\n```\n\n")

legend = "\nLegenda de Significância:\n [*] p < 0.05 (Estatisticamente Significativo)\n [+] p < 0.10 (Forte tendência)"
print(legend)
output_md.append(legend)

# ---------------------------------------------------------
# PARTE 3: EXPORTANDO OS ARQUIVOS
# ---------------------------------------------------------

# Exportando para Markdown
with open('resultados_analise.md', 'w', encoding='utf-8') as f:
    f.writelines(output_md)

# Exportando para CSV (Separado por vírgula)
df_export.to_csv('resultados_descritivos.csv', index=False, encoding='utf-8')

# Exportando para TSV (Separado por tabulação)
df_export.to_csv('resultados_descritivos.tsv', sep='\t', index=False, encoding='utf-8')

print("\n\n✅ Exportação concluída! Os arquivos .md, .csv e .tsv foram criados na pasta atual.")