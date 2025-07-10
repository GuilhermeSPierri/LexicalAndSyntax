class TabelaSimbolos:
    def __init__(self):
        self.tabela = []

    def adicionar(self, lexema, tipo, posicao=None):
        # Evita duplicatas para identificadores
        if tipo == "id" and any(simbolo["lexema"] == lexema and simbolo["tipo"] == tipo for simbolo in self.tabela):
            return
        self.tabela.append({
            "lexema": lexema,
            "tipo": tipo,
            "posicao": posicao
        })

    def __str__(self):
        linhas = [f"{'Lexema':<20}{'Tipo':<15}{'Posição':<10}"]
        for simbolo in self.tabela:
            linhas.append(f"{simbolo['lexema']:<20}{simbolo['tipo']:<15}{str(simbolo['posicao']):<10}")
        return "\n".join(linhas)

def criar_tabela_simbolos(tokens, posicoes=None):
    tabela = TabelaSimbolos()
    for i, token in enumerate(tokens):
        # token deve ser do tipo "<(lexema,tipo)>"
        token = token.replace("<", "").replace(">", "").replace("(", "").replace(")", "").replace("'", "")
        partes = token.split(",")
        if len(partes) == 2:
            lexema = partes[0].strip()
            tipo = partes[1].strip()
            posicao = posicoes[i] if posicoes is not None and i < len(posicoes) else None
            tabela.adicionar(lexema, tipo, posicao)
        elif len(partes) == 3:
            lexema = partes[0].strip()
            tipo = partes[1].strip()
            posicao = partes[2].strip()
            tabela.adicionar(lexema, tipo, posicao)
    return tabela