from Lexico.src.automato import Automato
from Lexico.src.transicao import Transicao

def uniao_automatos(AFDS : list) -> Automato:
    estado_inicial = f"q{Automato.incrementar_contador_estados()}"

    transicoes = []
    estados = []
    alfabeto = set()
    estados_finais = []
    mapa_estados_finais = {}

    for afd in AFDS:
        for transicao in afd.transicoes:
            transicoes.append(transicao)
        transicoes.append(Transicao(estado_inicial, "&", afd.estado_inicial))

    for afd in AFDS:
        alfabeto = alfabeto.union(afd.alfabeto)
        estados += afd.estados

    for afd in AFDS:
        estados_finais += afd.estados_finais

    # faz o mapeamento de cada estado final para um identificador de ER ou def_Reg
    for afd in AFDS:
        for estado_f in afd.estados_finais:
            mapa_estados_finais[estado_f] = afd.nome
    
    automato = Automato(estados, alfabeto, transicoes, estado_inicial, estados_finais)

    automato.mapa_estados_finais = mapa_estados_finais

    return automato

