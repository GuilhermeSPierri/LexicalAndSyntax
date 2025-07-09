from Lexico.src.automato import Automato
from Lexico.src.transicao import Transicao
class Arv_Sntx_Est:
    def __init__(self, raiz, nodos, simbolos):
        self.raiz = raiz
        self.nodos = nodos
        self.simbolos = simbolos
        
        
    def criar_AFD(self):
        
        alfabeto = set()
        pos_to_simbol = {}
        aceitacao_pos = None
        
        todos_nodos = self.nodos + [self.raiz]
        for nodo in todos_nodos:
            if nodo.left == None and nodo.right == None:
                if nodo.simbolo == '#':
                    aceitacao_pos = nodo.posicao
                elif nodo.simbolo != '&':  # Ignorar epsilon
                    alfabeto.add(nodo.simbolo)
                    pos_to_simbol[nodo.posicao] = nodo.simbolo
        
        if aceitacao_pos is None:
            raise ValueError("Símbolo de aceitação '#' não encontrado na árvore")
        
        followpos_global = {}
        for nodo in todos_nodos:
            if nodo.left == None and nodo.right == None and nodo.posicao is not None:
                followpos_global[nodo.posicao] = nodo.followpos
        #print("followpos", followpos_global)
        print("=== DEBUG criar_AFD ===")
        print("aceitacao_pos =", aceitacao_pos)
        print("postfix tokens (pos→simbolo):", pos_to_simbol)
        print("root.firstpos =", self.raiz.firstpos)

        # inicializar DFA
        S0 = frozenset(self.raiz.firstpos)  # Estado inicial
        Dstates = [S0]                      # Estados a processar
        marcado = {S0: False}              # Controle de marcação
        Dtran = {}                           # Tabela de transições
        
        # processar estados usando BFS
        while Dstates:
            S = Dstates.pop(0)
            if marcado[S]:
                continue
            marcado[S] = True
            Dtran[S] = {}
            
            for a in alfabeto:
                U = set()
                # unir followpos para todas as posições em S que correspondem a 'a'
                for p in S:
                    if p in pos_to_simbol and pos_to_simbol[p] == a:
                        U |= followpos_global.get(p, set())
                
                U_frozen = frozenset(U)
                Dtran[S][a] = U_frozen
                
                # adicionar novo estado se necessário
                if U_frozen not in marcado:
                    marcado[U_frozen] = False
                    Dtran[U_frozen] = {}
                    Dstates.append(U_frozen)
        
        print("todos os estados (objetos frozenset):", list(marcado.keys()))
        print("estados de aceitação (frozensets):", [s for s in marcado if aceitacao_pos in s])

        # identificar estados de aceitação
        estados_aceitacao = {estado for estado in marcado if aceitacao_pos in estado}
        
        # adicionar estados
        estados = set()
        for estado in marcado:
            estados.add(str(estado))

        # adicionar transições
        transicoes_list = []
        for estado, transicoes in Dtran.items():
            for simbolo, proximo_estado in transicoes.items():
                transicao = Transicao(str(estado), simbolo, str(proximo_estado))
                transicoes_list.append(transicao)

        # definir estados de aceitação
        estados_finais = []
        for estado in estados_aceitacao:
            estados_finais.append(str(estado))

        # criar e retornar o autômato
        afd = Automato(estados, alfabeto,transicoes_list,str(S0), estados_finais)
        return afd

