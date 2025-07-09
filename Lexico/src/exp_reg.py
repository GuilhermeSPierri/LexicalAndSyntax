class Exp_Reg:

    def __init__(self, exp_reg: str, alfabeto: set, operacoes: set):
        self.alfabeto = alfabeto
        self.operacoes = operacoes
        self.exp_reg = self.formatar_exp(exp_reg)
        self.precedencia = {"|" : 1, "." : 2, "*" : 3, "+" : 3, "?" : 3}
        self.post = self.postfix(self.exp_reg)
        print("postfix: ", self.post)
        
    def formatar_exp(self, exp_reg: str):
        exp_reg = "(" + exp_reg + ")#"
        i = 0
        while i < len(exp_reg) and exp_reg[i] != "#":
            #Se for uma sequência de escape, pula sem inserir concatenação:
            if exp_reg[i] == "\\" and i+1 < len(exp_reg):
                i += 2
                continue

            if exp_reg[i] == '"':
                # Encontrou a aspa de abertura, agora busca a de fechamento
                j = i + 1
                while j < len(exp_reg) and exp_reg[j] != '"':
                    j += 1
                if j >= len(exp_reg):
                    raise ValueError("Literal não fechado")
                # j está na aspa de fechamento
                # Adiciona ponto após a aspa de fechamento, se não houver já um ponto, operador, ), | ou #
                if j+1 < len(exp_reg) and exp_reg[j+1] not in '.|)#':
                    exp_reg = exp_reg[:j+1] + '.' + exp_reg[j+1:]
                    j += 1  # ajusta para avançar após o novo ponto inserido
                i = j + 1  # continua após a aspa de fechamento (e possível ponto)
                continue

            elif exp_reg[i] in self.alfabeto or exp_reg[i] == ")":
                if i+1 < len(exp_reg) and (exp_reg[i+1] in self.alfabeto or exp_reg[i+1] == "#" or exp_reg[i+1] == "(" or exp_reg[i+1] == '"'):
                    exp_reg = exp_reg[:i+1] + "." + exp_reg[i+1:]
                    i += 2
                    continue
                else:
                    i += 1

            elif exp_reg[i] in self.operacoes:
                if exp_reg[i] == "|":
                    i += 1
                    continue
                elif exp_reg[i] in "*?+":
                    if i+1 < len(exp_reg) and (exp_reg[i+1] in self.alfabeto or exp_reg[i+1] == "(" or exp_reg[i+1] == "#" or exp_reg[i+1] == '"'):
                        exp_reg = exp_reg[:i+1] + "." + exp_reg[i+1:]
                        i += 2
                        continue
                    else:
                        i += 1
            else:
                i += 1
        return exp_reg



    
    def postfix(self, exp_reg: str):
        input_str = exp_reg.strip().replace(' ', '')
        pilha = []
        output = []
        i = 0
        n = len(input_str)

        while i < n:
            if input_str[i] == "\\" and i+1 < n:
                print("to aqui!", input_str[i])
                # pega "\"+caractere e joga pro output como um token literal
                output.append("\\" + input_str[i+1])
                print("output: ", output)
                i += 2
                print("após somar i+2", input_str[i])
                continue

            elif input_str[i] == '"':
                start = i
                i += 1  # Pula a aspa inicial
                # Encontra a aspa de fechamento
                while i < n and input_str[i] != '"':
                    i += 1
                if i >= n:
                    raise ValueError('Cadeia literal não fechada com aspas')
                # Pega o conteúdo literal (sem as aspas)
                literal_content = input_str[start+1:i]
                # Adiciona como token único entre aspas
                output.append('"' + literal_content + '"')
                i += 1  # Pula a aspa final


            elif input_str[i] in self.operacoes:
                while (pilha and pilha[-1] != '(' and 
                    self.precedencia.get(pilha[-1], 0) >= self.precedencia.get(input_str[i], 0)):
                    output.append(pilha.pop())
                pilha.append(input_str[i])
                i += 1

            elif input_str[i] == "#":
                output.append("#")
                i += 1

            elif input_str[i] == "(":
                pilha.append(input_str[i])
                i += 1

            elif input_str[i] == ")":
                while pilha and pilha[-1] != "(":
                    output.append(pilha.pop())
                print("pilha atual: ", pilha)
                if pilha and pilha[-1] == "(":
                    pilha.pop()  # Remove '('
                print("pilha atual: ", pilha)
                i += 1

            elif input_str[i] in self.operacoes:
                while (pilha and pilha[-1] != '(' and 
                    self.precedencia.get(pilha[-1], 0) >= self.precedencia.get(input_str[i], 0)):
                    output.append(pilha.pop())
                pilha.append(input_str[i])
                i += 1

            elif input_str[i] in self.alfabeto:
                output.append(input_str[i])
                i += 1
            else:
                i += 1  # Caracteres não reconhecidos são ignorados
        while pilha:
            output.append(pilha.pop())
        
        return output
