def closure(I, productions):
    """Calcula o fechamento de um conjunto de itens LR(0)"""
    J = set(I)
    added = True
    
    while added:
        added = False
        new_items = set()
        
        for item in J:
            A, alpha, beta = item
            if beta and beta[0] in productions:  # Símbolo não-terminal após o ponto
                B = beta[0]
                for gamma in productions[B]:
                    new_item = (B, tuple(), tuple(gamma))
                    if new_item not in J and new_item not in new_items:
                        new_items.add(new_item)
                        added = True
        
        J |= new_items
    return J