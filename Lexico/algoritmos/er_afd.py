from Lexico.src.exp_reg import Exp_Reg
from Lexico.algoritmos.nodoASE import Nodo
from Lexico.algoritmos.arv_sntx_est import Arv_Sntx_Est

def criar_arvore(exp_reg: Exp_Reg) -> Arv_Sntx_Est:
    nodos = []  
    pilha = []
    simbolos = []
    pos_to_node = {}
    i = 0
    n = len(exp_reg.post)
    
    while i < n:
        token = exp_reg.post[i]

        if token.startswith("\\"):
            simbolo_literal = token[1:]
            folha = Nodo.criar_folha(
                simbolo_literal,
                Nodo.incrementar_contador()
            )
            nodos.append(folha)
            pilha.append(folha)
            simbolos.append(simbolo_literal)
            pos_to_node[folha.posicao] = folha
            i += 1
            continue


        elif token in exp_reg.operacoes:
            if token == "|":
                n1 = pilha.pop()
                n2 = pilha.pop()
                nodo_ou = Nodo(n1, n2)
                nodo_ou.anulavel = n1.anulavel or n2.anulavel
                nodo_ou.firstpos = n1.firstpos | n2.firstpos
                nodo_ou.lastpos = n1.lastpos | n2.lastpos
                nodos.append(nodo_ou)
                pilha.append(nodo_ou)

            elif token == "*":
                n1 = pilha.pop()
                nodo_estrela = Nodo(n1, None)
                nodo_estrela.anulavel = True        # Sempre True
                nodo_estrela.firstpos = n1.firstpos
                nodo_estrela.lastpos = n1.lastpos
                for pos in n1.lastpos:
                    if pos in pos_to_node:
                        node = pos_to_node[pos]
                        node.followpos = node.followpos | n1.firstpos
                
                nodos.append(nodo_estrela)
                pilha.append(nodo_estrela)

            elif token == "?":
                n1 = pilha.pop()
                nodo_opcional = Nodo(n1, None)
                nodo_opcional.anulavel = True       # Sempre True
                nodo_opcional.firstpos = n1.firstpos
                nodo_opcional.lastpos = n1.lastpos
                nodos.append(nodo_opcional)
                pilha.append(nodo_opcional)

            elif token == "+":
                n1 = pilha.pop()
                nodo_pos = Nodo(n1, None)
                nodo_pos.anulavel = False           # Sempre False
                nodo_pos.firstpos = n1.firstpos
                nodo_pos.lastpos = n1.lastpos
                for pos in n1.lastpos:
                    if pos in pos_to_node:
                        node = pos_to_node[pos]
                        node.followpos |= n1.firstpos
                
                nodos.append(nodo_pos)
                pilha.append(nodo_pos)
    
            elif token == ".":
                n2 = pilha.pop()
                n1 = pilha.pop()
                nodo_conc = Nodo(n1,n2)
                nodo_conc.anulavel = n1.anulavel and n2.anulavel

                if n1.anulavel:
                    nodo_conc.firstpos = n1.firstpos | n2.firstpos
                else:
                    nodo_conc.firstpos = n1.firstpos
                if n2.anulavel:
                    nodo_conc.lastpos = n1.lastpos | n2.lastpos
                else:
                    nodo_conc.lastpos = n2.lastpos

                for elemento in nodo_conc.left.lastpos:
                    for nodo in nodos:
                        if nodo.posicao == elemento:
                            nodo.followpos |= nodo_conc.right.firstpos

                nodos.append(nodo_conc)
                pilha.append(nodo_conc)

        elif token in exp_reg.alfabeto or token == "#":
            folha = Nodo.criar_folha(token, Nodo.incrementar_contador())
            nodos.append(folha)
            pilha.append(folha)
            simbolos.append(token)
            pos_to_node[folha.posicao] = folha

        elif token == "&":
            epsilon = Nodo.criar_epsilon()
            nodos.append(epsilon)
            pilha.append(epsilon)
            
        i += 1

    raiz = pilha[0] if pilha else None
    if raiz and raiz in nodos:
        nodos.remove(raiz)
    
    arvore = Arv_Sntx_Est(raiz, nodos, simbolos)
    return arvore

def encontrar_no_por_posicao(pos, todos_nodos):
    for nodo in todos_nodos:
        if nodo.eh_folha() and nodo.posicao == pos:
            return nodo
    return None

