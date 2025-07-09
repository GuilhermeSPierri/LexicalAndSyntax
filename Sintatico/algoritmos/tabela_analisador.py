from Sintatico.algoritmos.goto import goto

# Algoritmo 4.38
def criar_tabela(C, produtos_inc, start_symbol, terminals, nonterminals, follow):
    start_aug = start_symbol + "'"
    n_states = len(C)
    # Inicializa ACTION e GOTO
    ACTION = { (i, a): None for i in range(n_states) for a in list(terminals) + ['$'] }
    GOTO   = { (i, A): None for i in range(n_states) for A in nonterminals }
    
    for i, I in enumerate(C):
        # shift / reduce
        for (A, corpo, pos) in I:
            if pos < len(corpo):
                a = corpo[pos]
                if a in terminals:
                    J = goto(I, a, produtos_inc)
                    if J:
                        j = C.index(J)
                        # Se já existir e conflitar, ideal seria detectar conflito; aqui assumimos SLR
                        ACTION[(i, a)] = f"shift {j}"
            else:
                # ponto no fim: A->α·
                if A == start_aug:
                    # item S'->S·  => aceitar em $
                    ACTION[(i, '$')] = "accept"
                else:
                    # redução pela produção A -> corpo
                    # aqui A é não-terminal original
                    # corpo é tuple; para exibir, faça ' '.join(corpo) ou outra convenção
                    corpo_str = ' '.join(corpo) if corpo else 'ε'
                    for a_term in follow[A]:
                        ACTION[(i, a_term)] = f"reduce {A} -> {corpo_str}"
        # GOTO para não-terminais
        for A in nonterminals:
            J = goto(I, A, produtos_inc)
            if J:
                j = C.index(J)
                GOTO[(i, A)] = j
    return ACTION, GOTO
