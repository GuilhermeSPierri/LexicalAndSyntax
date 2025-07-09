from Lexico.src.automato import Automato

def testar_word(AFD: Automato, word:str) -> list:
    print(f"[DEBUG] testar_word iniciada para '{word}'")
    estado_original = AFD.estado_atual
    print(f"[DEBUG] Estado inicial: {estado_original}")
    
    # Criar uma cópia temporária para não alterar o autômato original
    from copy import deepcopy
    afd_temp = deepcopy(AFD)
    afd_temp.estado_atual = estado_original

    for char in word:
        print(f"[DEBUG] Processando char: '{char}'")
        print(f"[DEBUG] Estado atual: {AFD.estado_atual}")
        
        if char not in afd_temp.alfabeto:
            print(f"[DEBUG] Char '{char}' não está no alfabeto {afd_temp.alfabeto}")
            #afd_temp.estado_atual = estado_original
            return [False, afd_temp]
        
        transicao_encontrada = False
        for transicao in afd_temp.transicoes:
            if transicao.estado1 == afd_temp.estado_atual and transicao.simbolo == char:
                print(f"[DEBUG] Transição encontrada! Indo para {transicao.estado2}")
                afd_temp.estado_atual = transicao.estado2
                transicao_encontrada = True
                break
        
    resultado = afd_temp.estado_atual in afd_temp.estados_finais
    print(f"[DEBUG] Estado final: {afd_temp.estado_atual}, é final? {resultado}")

    AFD.estado_atual = estado_original
    return [resultado, afd_temp]