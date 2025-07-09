def compute_first(producoes):
    # Inicializa FIRST para não-terminais
    first = {A: set() for A in producoes}
    
    # Regra 3: Adiciona ε para produções explicitamente vazias
    for A, corpos in producoes.items():
        for corpo in corpos:
            if corpo == [] or corpo == ['&']:
                first[A].add('&')
    
    mudou = True
    while mudou:
        mudou = False
        for A, corpos in producoes.items():
            for corpo in corpos:
                # Flag para verificar se todos os símbolos geram ε
                todos_epsilon = True
                for X in corpo:
                    # Símbolo terminal (Regra 1)
                    if X not in producoes:  # Terminal
                        if X != '&':  # Ignora '&' (já tratado)
                            # Adiciona terminal ao FIRST(A)
                            if X not in first[A]:
                                first[A].add(X)
                                mudou = True
                        # Terminal não gera ε, interrompe a sequência
                        todos_epsilon = False
                        break
                    
                    # Símbolo não-terminal (Regra 2)
                    else:
                        # Adiciona FIRST(X) - {ε} ao FIRST(A)
                        antes = first[A].copy()
                        first[A] |= first[X] - {'&'}
                        if antes != first[A]:
                            mudou = True
                        
                        # Verifica se X gera ε
                        if '&' not in first[X]:
                            todos_epsilon = False
                            break
                
                # Se todos geram ε, adiciona ε ao FIRST(A) (Regra 2)
                if todos_epsilon:
                    if '&' not in first[A]:
                        first[A].add('&')
                        mudou = True
    return first