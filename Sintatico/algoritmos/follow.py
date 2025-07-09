# Algoritmo na seção 4.4.2 do livro

def compute_follow_sets(produtos, start_symbol, first):
    follow = {A: set() for A in produtos}
    follow[start_symbol].add('$')
    mudou = True
    while mudou:
        mudou = False
        for A, corpos in produtos.items():
            for corpo in corpos:
                current_follow = follow[A].copy()
                # percorre a produção de trás para frente
                for X in reversed(corpo):
                    if X in produtos:  # X é não-terminal
                        antes = len(follow[X])
                        follow[X] |= current_follow
                        if '&' in first[X]:
                            current_follow |= (first[X] - {'&'})
                        else:
                            current_follow = first[X].copy()
                        if len(follow[X]) > antes:
                            mudou = True
                    else:
                        current_follow = {X}  # X é terminal
    return follow