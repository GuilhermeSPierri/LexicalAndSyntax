from Lexico.src.automato import Automato
from Lexico.src.transicao import Transicao


# Método que calcula o epsilon fecho de cada estado
def epsilon_fecho(automato, estado):
    fecho = set(estado) 
    estados_a_processar = list(estado)
    
    while estados_a_processar:
        estado_atual = estados_a_processar.pop()
        destinos = []
        for transicao in automato.transicoes:
            # Verifica transições épsilon do estado atual
            if transicao.estado1 == estado_atual and transicao.simbolo == "&":

                if isinstance(transicao.estado2, list):
                    for elemento in transicao.estado2:
                        destinos.append(elemento)
                else:
                    destinos.append(transicao.estado2)
                        
                for destino in destinos:
                    if destino not in fecho:
                        fecho.add(destino)
                        estados_a_processar.append(destino)
    return fecho

def determinizacao_de_automato(afnd: Automato) -> Automato:
    # Pré-processa transições para acesso rápido
    transicoes_dict = {}
    for transicao in afnd.transicoes:
        chave = (transicao.estado1, transicao.simbolo)
        destinos = transicao.estado2
        if not isinstance(destinos, list):
            destinos = [destinos]
        
        if chave not in transicoes_dict:
            transicoes_dict[chave] = set()
        transicoes_dict[chave].update(destinos)

    # Estado inicial do AFD é o fecho-épsilon do AFND
    estado_inicial_afd = frozenset(epsilon_fecho(afnd, [afnd.estado_inicial]))
    
    # Inicializa estruturas do AFD
    estados_afd = {estado_inicial_afd}
    estados_finais_afd = list()
    transicoes_afd = []
    fila_estados = [estado_inicial_afd]
    mapa_estados_finais = {}


    # Para cada estado novo encontrado (frozenset) no AFD, vamos fazer a união dos &-fechos encontrados a partir de cada estado que pertence ao "estado novo" procurando por cada símbolo do alfabeto. Sendo assim, encontrando os próximos estados alcançáveis do AFD
    
    while fila_estados:
        estado_atual = fila_estados.pop(0)
        
        # Processa cada símbolo do alfabeto
        for simbolo in afnd.alfabeto:
            if simbolo == "&":
                continue  # Ignora transições por & no AFD, estamos determinizando
                
            proximo_estado = set()
            
            # Para cada estado no conjunto atual
            for estado in estado_atual:
                chave_transicao = (estado, simbolo)
                
                if chave_transicao in transicoes_dict:
                    for destino in transicoes_dict[chave_transicao]:
                        proximo_estado.update(epsilon_fecho(afnd, [destino]))
            
            if not proximo_estado:
                continue  # Nenhuma transição para este símbolo, busca pelo próximo símbolo
                
            proximo_estado = frozenset(proximo_estado)
            
            # Adiciona novo estado se necessário
            if proximo_estado not in estados_afd:
                estados_afd.add(proximo_estado)
                fila_estados.append(proximo_estado)
                
            # Cria transição para o AFD
            transicoes_afd.append(Transicao(estado_atual, simbolo, proximo_estado))
    
    # Estados finais são os que contêm algum estado final original
    for estado in estados_afd:
        for estado_individual in estado:
            if estado_individual in afnd.estados_finais:
                nome = afnd.mapa_estados_finais.get(estado_individual)
                if estado_individual in mapa_estados_finais:
                    nome_existente = mapa_estados_finais[estado]
                    # procura a prioridade dos nomes
                    pos_nome_existente = afnd.prioridade_nomes.index(nome_existente)
                    pos_nome_novo = afnd.prioridade_nomes.index(nome)

                    if pos_nome_novo > pos_nome_existente:
                        mapa_estados_finais[estado] = nome
                else:
                    mapa_estados_finais[estado] = nome
                estados_finais_afd.append(estado)
                
    
    frozen_para_estado = {}
    contador = 0
    
    # Função para obter nome simplificado
    def obter_nome(conjunto):
        nonlocal contador
        if conjunto not in frozen_para_estado:
            frozen_para_estado[conjunto] = f"q{contador}"
            contador += 1
        return frozen_para_estado[conjunto]
    
    # Construir transições com nomes simplificados
    transicoes_simplificadas = []
    for trans in transicoes_afd:
        origem = obter_nome(trans.estado1)
        destino = obter_nome(trans.estado2)
        transicoes_simplificadas.append(Transicao(origem, trans.simbolo, destino))
    
    # Construir lista de estados simplificados
    estados_simplificados = [obter_nome(estado) for estado in estados_afd]
    
    # Obter nome do estado inicial
    estado_inicial_simplificado = obter_nome(estado_inicial_afd)

    finais_simplificados = []
    mapa_estados_finais_simplificado = {}
    for estado_dict, nome in mapa_estados_finais.items():
        estado_final_simplificado = obter_nome(estado_dict)
        mapa_estados_finais_simplificado[estado_final_simplificado] = nome
        finais_simplificados.append(estado_final_simplificado)

    afnd.alfabeto = sorted(afnd.alfabeto)
    estados_simplificados = sorted(estados_simplificados)
    finais_simplificados = sorted(finais_simplificados)

    transicoes_simplificadas = sorted(
        transicoes_simplificadas,
        key=lambda transicao: (transicao.estado1, transicao.simbolo, transicao.estado2)
    )

    automato = Automato(list(estados_simplificados), afnd.alfabeto, transicoes_simplificadas, estado_inicial_simplificado, finais_simplificados)

    automato.mapa_estados_finais = mapa_estados_finais_simplificado

    return automato
    