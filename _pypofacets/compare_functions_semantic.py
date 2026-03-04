import ast
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extract_functions_raw(filepath):
    """Extrai o código fonte exato de cada função como uma string única."""
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    tree = ast.parse(source)
    lines = source.splitlines()
    functions = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Pega da primeira linha interna até o fim (ignora o 'def')
            if node.body:
                start_line = node.body[0].lineno - 1
            else:
                start_line = node.lineno
            end_line = node.end_lineno
            
            # Junta as linhas em uma única string de texto
            func_code = "\n".join(lines[start_line:end_line])
            functions[node.name] = func_code.strip()
            
    return functions

def main():
    # Carrega um modelo pré-treinado super leve e rápido para gerar embeddings
    # Para resultados focados APENAS em código, você poderia usar 'microsoft/codebert-base'
    print("Carregando o modelo de IA (isso pode demorar na primeira vez)...")
    model = SentenceTransformer('all-MiniLM-L6-v2') 
    
    file_gabarito = "modular_pypofacets.py"
    file_ia = "modular_pypofacets_gemini_v2.py"
    
    funcs_gabarito = extract_functions_raw(file_gabarito)
    funcs_ia = extract_functions_raw(file_ia)
    
    print(f"\n{'Função Original (Gabarito)':<40} | {'Melhor Correspondência (IA)':<35} | Similaridade Semântica")
    print("-" * 105)
    
    # Pré-calcula os embeddings (vetores) para todas as funções da IA para otimizar
    nomes_ia = list(funcs_ia.keys())
    codigos_ia = list(funcs_ia.values())
    if not codigos_ia:
        print("Nenhuma função encontrada na IA.")
        return
        
    embeddings_ia = model.encode(codigos_ia)
    
    # Compara cada função do gabarito com as funções da IA
    for name_g, code_g in funcs_gabarito.items():
        # Transforma a função do gabarito em vetor
        embedding_g = model.encode([code_g])
        
        # Calcula a similaridade de cosseno contra TODAS as funções da IA de uma vez
        similarities = cosine_similarity(embedding_g, embeddings_ia)[0]
        
        # Encontra o índice da maior similaridade
        best_match_idx = np.argmax(similarities)
        best_score = similarities[best_match_idx]
        best_match_name = nomes_ia[best_match_idx]
        
        print(f"{name_g:<40} | {best_match_name:<35} | {best_score:.4f}")

if __name__ == "__main__":
    main()