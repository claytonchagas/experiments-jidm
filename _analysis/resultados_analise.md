# Resultados da Análise de Modularização e Proveniência
## 1. ANÁLISE DESCRITIVA AOS PARES (REDUÇÃO/AUMENTO)
### Experimento: `BELIEF_PROP`
**[1] Monolítico vs IA Modular (Claude)**
- **LOC:** 15 -> 34 (Aumentou +19 linhas)
- **Nodes:** 327 -> 37 (Reduziu 290 | -88.7%)
- **Edges:** 386 -> 57 (Reduziu 329 | -85.2%)
- **Path:** 165 -> 5 (Reduziu 160 | -97.0%)

**[2] Monolítico vs Original (Humano)**
- **LOC:** 15 -> 23 (Aumentou +8 linhas)
- **Nodes:** 327 -> 37 (Reduziu 290 | -88.7%)
- **Edges:** 386 -> 56 (Reduziu 330 | -85.5%)
- **Path:** 165 -> 5 (Reduziu 160 | -97.0%)

### Experimento: `CVAR`
**[1] Monolítico vs IA Modular (Claude)**
- **LOC:** 26 -> 43 (Aumentou +17 linhas)
- **Nodes:** 243 -> 128 (Reduziu 115 | -47.3%)
- **Edges:** 359 -> 136 (Reduziu 223 | -62.1%)
- **Path:** N/A (ciclo) -> 7 Resolvido

**[2] Monolítico vs Original (Humano)**
- **LOC:** 26 -> 28 (Aumentou +2 linhas)
- **Nodes:** 243 -> 123 (Reduziu 120 | -49.4%)
- **Edges:** 359 -> 121 (Reduziu 238 | -66.3%)
- **Path:** N/A (ciclo) -> 4 Resolvido

### Experimento: `FFT`
**[1] Monolítico vs IA Modular (Claude)**
- **LOC:** 13 -> 32 (Aumentou +19 linhas)
- **Nodes:** 19 -> 19 (Manteve)
- **Edges:** 22 -> 20 (Reduziu 2 | -9.1%)
- **Path:** 6 -> 5 (Reduziu 1 | -16.7%)

**[2] Monolítico vs Original (Humano)**
- **LOC:** 13 -> 22 (Aumentou +9 linhas)
- **Nodes:** 19 -> 19 (Manteve)
- **Edges:** 22 -> 20 (Reduziu 2 | -9.1%)
- **Path:** 6 -> 5 (Reduziu 1 | -16.7%)

### Experimento: `GAUSS_LEGENDRE`
**[1] Monolítico vs IA Modular (Claude)**
- **LOC:** 14 -> 32 (Aumentou +18 linhas)
- **Nodes:** 26 -> 16 (Reduziu 10 | -38.5%)
- **Edges:** 27 -> 15 (Reduziu 12 | -44.4%)
- **Path:** 12 -> 5 (Reduziu 7 | -58.3%)

**[2] Monolítico vs Original (Humano)**
- **LOC:** 14 -> 24 (Aumentou +10 linhas)
- **Nodes:** 26 -> 16 (Reduziu 10 | -38.5%)
- **Edges:** 27 -> 15 (Reduziu 12 | -44.4%)
- **Path:** 12 -> 5 (Reduziu 7 | -58.3%)

### Experimento: `HEAT_DIST`
**[1] Monolítico vs IA Modular (Claude)**
- **LOC:** 15 -> 29 (Aumentou +14 linhas)
- **Nodes:** 27 -> 14 (Reduziu 13 | -48.1%)
- **Edges:** 30 -> 24 (Reduziu 6 | -20.0%)
- **Path:** 8 -> 3 (Reduziu 5 | -62.5%)

**[2] Monolítico vs Original (Humano)**
- **LOC:** 15 -> 18 (Aumentou +3 linhas)
- **Nodes:** 27 -> 11 (Reduziu 16 | -59.3%)
- **Edges:** 30 -> 12 (Reduziu 18 | -60.0%)
- **Path:** 8 -> 3 (Reduziu 5 | -62.5%)

### Experimento: `LOOK_AND_SAY`
**[1] Monolítico vs IA Modular (Claude)**
- **LOC:** 30 -> 43 (Aumentou +13 linhas)
- **Nodes:** 151 -> 18 (Reduziu 133 | -88.1%)
- **Edges:** 455 -> 16 (Reduziu 439 | -96.5%)
- **Path:** N/A (ciclo) -> 4 Resolvido

**[2] Monolítico vs Original (Humano)**
- **LOC:** 30 -> 33 (Aumentou +3 linhas)
- **Nodes:** 151 -> 6 (Reduziu 145 | -96.0%)
- **Edges:** 455 -> 4 (Reduziu 451 | -99.1%)
- **Path:** N/A (ciclo) -> 2 Resolvido

---
## 2. RESULTADOS ESTATÍSTICOS (TESTE DE WILCOXON)

### [COMPARAÇÃO 1: Monolítico vs IA Modular (Claude)]
```text
Linhas de Código (LOC)    | N=6 | W=0.0  | P-valor: 0.0312 *
Nós do Grafo (Nodes)      | N=5 | W=0.0  | P-valor: 0.0625 +
Arestas (Edges)           | N=6 | W=0.0  | P-valor: 0.0312 *
Caminho Longo (Path)      | N=4 | W=0.0  | P-valor: 0.1250 
```

### [COMPARAÇÃO 2: Monolítico vs Original Humano]
```text
Linhas de Código (LOC)    | N=6 | W=0.0  | P-valor: 0.0312 *
Nós do Grafo (Nodes)      | N=5 | W=0.0  | P-valor: 0.0625 +
Arestas (Edges)           | N=6 | W=0.0  | P-valor: 0.0312 *
Caminho Longo (Path)      | N=4 | W=0.0  | P-valor: 0.1250 
```


Legenda de Significância:
 [*] p < 0.05 (Estatisticamente Significativo)
 [+] p < 0.10 (Forte tendência)