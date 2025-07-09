from Lexico.src.transicao import Transicao

class Automato:
    contador_automato = 0
    contador_estados = -1

    def __init__(self, K: list, alfabeto: set, transicoes: list, q0: str, F:list):
        self.estados = K
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = q0
        self.estados_finais = F
        self.incrementar_contador_automato()
        self.estado_atual = self.estado_inicial
        self.nome = None
        self.mapa_estados_finais = {}

    @classmethod
    def incrementar_contador_automato(cls) -> int:
        cls.contador_automato += 1
        return cls.contador_automato
    
    @classmethod
    def incrementar_contador_estados(cls) -> int:
        cls.contador_estados += 1
        return cls.contador_estados
    
    @classmethod
    def get_contador_automato(cls) -> int:
        return cls.contador_automato
    
    @classmethod
    def get_contador_estados(cls) -> int:
        return cls.contador_estados
    
    @classmethod
    def gen_1_simb(cls, simb, alfabeto):
        estado_inicial = f"q{cls.incrementar_contador_estados()}"
        estado_final = f"q{cls.incrementar_contador_estados()}"
        transicao = [Transicao(estado_inicial, simb, estado_final)]
        return Automato([estado_inicial, estado_final], alfabeto, transicao, estado_inicial, [estado_final])

    def transicionar(self, char) -> bool:
        for transicao in self.transicoes:
            if transicao.estado1 == self.estado_atual and transicao.simbolo == char:
                self.estado_atual = transicao.estado2
                return True
        self.estado_atual = self.estado_inicial
        return False
        
    

