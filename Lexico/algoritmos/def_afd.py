def expandir_intervalo(inicio: str, fim: str) -> list:
    """Expande um intervalo de caracteres (ex: a-z -> ['a','b',...,'z'])"""
    try:
        cod_inicio = ord(inicio)
        cod_fim = ord(fim)
        if cod_inicio > cod_fim:
            cod_inicio, cod_fim = cod_fim, cod_inicio
        return [chr(cod) for cod in range(cod_inicio, cod_fim + 1)]
    except TypeError:
        return [inicio, fim]

def formatar_def_reg(def_reg):
    caracteres_form = []
    pilha = []
    dentro_col = False

    i = 0
    n = len(def_reg)
    while i < n:
        # ── 0) trata QUALQUER escape (\X) como token único ──
        if def_reg[i] == "\\" and i+1 < n:
            esc = def_reg[i:i+2]   # ex: "\["
            caracteres_form.append(esc)
            i += 2
            continue

        # ── 1) abre colchete não-escapado ──
        if def_reg[i] == "[":
            dentro_col = True
            pilha = []
            i += 1
            continue

        # ── 2) fecha colchete ──
        if def_reg[i] == "]" and dentro_col:
            # pega todo o conteúdo acumulado em pilha
            caracteres_form.append(pilha)
            dentro_col = False
            i += 1
            continue

        # ── 3) conteúdo dentro de [...] ──
        if dentro_col:
            pilha.append(def_reg[i])
        else:
            # fora de colchete, trata literal único
            caracteres_form.append(def_reg[i])
        i += 1

    # trata colchetes não fechados (adiciona conteúdo na ordem original)
    if dentro_col:
        caracteres_form.extend(pilha)
    
    sup = []
    
    for elemento in caracteres_form:
        if type(elemento) == list:
            # Processar intervalos como [a-z]
            elementos_expandidos = []
            i = 0
            while i < len(elemento):
                if i + 2 < len(elemento) and elemento[i+1] == '-':
                    # É um intervalo
                    intervalo = expandir_intervalo(elemento[i], elemento[i+2])
                    elementos_expandidos.extend(intervalo)
                    i += 3  # Pula os 3 elementos do intervalo
                else:
                    elementos_expandidos.append(elemento[i])
                    i += 1
            sup.append("(" + "|".join(elementos_expandidos) + ")")
        else:
            sup.append(elemento)
    
    final = []
    i = 0
    n = len(sup)
    
    while i < n:
        # se o elemento atual for uma lista
        if type(sup[i]) is list:
            # verifica se existe próximo elemento e se também é uma lista
            if i + 1 < n and type(sup[i + 1]) is list:
                # concatena as duas listas e adiciona ao resultado
                final.append(sup[i] + sup[i + 1])
                i += 2      # pula o próximo elemento (já processado)
                continue    
            else:
                final.append(sup[i])
        else:
            final.append(sup[i])
        i += 1  # nao houve concatenacao
    out = ""
    for elemento in final:
        if type(elemento) == list:
            string = ""
            for item in elemento:
                if item == elemento[-1]:
                    string += item
                else:
                    string += item + "|"
            out += string
        else:
            out += elemento
                            
    return out

def gerar_alfabeto(exp_reg: str, operacoes: set) -> set:
    alfabeto = set()
    i = 0
    n = len(exp_reg)
    
    while i < n:
        if exp_reg[i].startswith("\\"):
            alfabeto.add(exp_reg[i+1])
            i += 2
        else:
            char = exp_reg[i]
            if char not in ["(", ")", '\\'] and char not in operacoes:
                alfabeto.add(char)
            i += 1
    
    return alfabeto

