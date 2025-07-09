from Sintatico.algoritmos.closure import closure
from Sintatico.algoritmos.goto import goto

# Algoritmo da figura 4.33

def items(productions, start_symbol):
    """Constrói a coleção canônica de conjuntos de itens LR(0)"""
    # Gramática aumentada
    augmented_prod = productions.copy()
    augmented_prod["S'"] = [[start_symbol]]
    
    # Item inicial
    I0 = closure({("S'", tuple(), (start_symbol,))}, augmented_prod)
    C = [I0]
    queue = [I0]
    processed = set()
    
    while queue:
        I = queue.pop(0)
        if id(I) in processed:
            continue
        processed.add(id(I))
        
        # Obter todos os símbolos que podem ser avançados
        symbols = set()
        for item in I:
            _, _, beta = item
            if beta:
                symbols.add(beta[0])
        
        for X in symbols:
            g = goto(I, X, augmented_prod)
            if not g:
                continue
            
            # Adicionar novo conjunto se for único
            if not any(g == existing for existing in C):
                C.append(g)
                queue.append(g)
    
    return C