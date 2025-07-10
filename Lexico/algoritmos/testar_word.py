from Lexico.src.automato import Automato

def testar_word(AFD: Automato, word:str) -> list:
    estado_original = AFD.estado_atual
    
    # Criar uma cópia temporária para não alterar o autômato original
    from copy import deepcopy
    afd_temp = deepcopy(AFD)
    afd_temp.estado_atual = estado_original

    for char in word:
        
        if char not in afd_temp.alfabeto:
            return [False, afd_temp]
        
        for transicao in afd_temp.transicoes:
            if transicao.estado1 == afd_temp.estado_atual and transicao.simbolo == char:
                afd_temp.estado_atual = transicao.estado2
                break
        
    resultado = afd_temp.estado_atual in afd_temp.estados_finais

    AFD.estado_atual = estado_original
    return [resultado, afd_temp]