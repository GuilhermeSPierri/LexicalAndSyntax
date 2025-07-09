from Sintatico.algoritmos.closure import closure

def goto(I, X, productions):
    """Calcula o conjunto GOTO(I, X)"""
    J = set()
    for item in I:
        A, alpha, beta = item
        if beta and beta[0] == X:
            new_alpha = alpha + (X,)
            new_beta = beta[1:]
            J.add((A, new_alpha, new_beta))
    
    return closure(J, productions) if J else set()