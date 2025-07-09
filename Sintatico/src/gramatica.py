class Gramatica:
    
    def __init__(self, N, T, P, S):
        self.n_terminais = N
        self.terminais = T
        self.producoes = P
        self.inicial = S