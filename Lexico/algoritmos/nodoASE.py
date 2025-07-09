class Nodo:
    posicao = 0
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = set()
        self.anulavel = False
        self.simbolo = None

    @classmethod
    def criar_folha(cls, simbolo, posicao):
        nodo = Nodo(None, None)
        nodo.firstpos = {posicao}
        nodo.lastpos = {posicao}
        nodo.anulavel = False
        nodo.simbolo = simbolo
        nodo.posicao = posicao
        return nodo

    @classmethod
    def criar_epsilon(cls):
        nodo = Nodo(None, None)
        nodo.firstpos = set()
        nodo.lastpos = set()
        nodo.anulavel = True
        nodo.simbolo = "&"
        return nodo

    @classmethod
    def incrementar_contador(cls):
        cls.posicao += 1
        return cls.posicao
    
    @classmethod
    def get_posicao(cls):
        return cls.posicao