def parse_tokens(tokens, ACTION, GOTO):
    pilha = [0]
    a_iter = iter(tokens + [('$','$')])  # adiciona marcador de fim
    a = next(a_iter)
    while True:
        s = pilha[-1]
        action = ACTION.get((s,a[0]))
        print("action: ", action)
        if not action:
            print("Estado atual:", s)
            print("Topo da pilha:", pilha)
            raise Exception(f"Erro sintático em token {a}")
        if action.startswith("shift"):
            _, t = action.split()
            pilha.append(int(t))
            a = next(a_iter)
        elif action.startswith("reduce"):
            partes = action.split()
            A = partes[1]
            alfa = partes[3:]
            for _ in alfa:
                pilha.pop()
            s_prime = pilha[-1]
            pilha.append(GOTO[(s_prime,A)])
        elif action == "accept":
            print("Entrada aceita.")
            return
        else:
            raise Exception("Token inesperado ou tabela mal formada.")