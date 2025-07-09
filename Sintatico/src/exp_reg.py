class Exp_Reg:

    def __init__(self, exp_reg: str, alfabeto: set, operacoes: set):
        self.alfabeto = alfabeto
        self.operacoes = operacoes
        self.exp_reg = self.formatar_exp(exp_reg)
        self.precedencia = {"|" : 1, "." : 2, "*" : 3, "+" : 3, "?" : 3}
        self.post = self.postfix(self.exp_reg)
        print("Formatado", self.exp_reg)
        
    def formatar_exp(self, exp_reg:str):
        exp_reg = "(" + exp_reg + ")#"
        i = 0
        while exp_reg[i] != "#":
            if exp_reg[i] in self.alfabeto or exp_reg[i] == ")":
                if exp_reg[i+1] in self.alfabeto or exp_reg[i+1] == "#" or exp_reg[i+1] == "(":
                    exp_reg = exp_reg[:i+1] + "." + exp_reg[i+1:]
                    i+=2
                    continue
                else:
                    i+=1
            elif exp_reg[i] in self.operacoes:
                if exp_reg[i] == "|":
                    i+=1
                    continue
                elif exp_reg[i] == "*" or exp_reg[i] == "?" or exp_reg[i] == "+":
                    if exp_reg[i+1] in self.alfabeto or exp_reg[i+1] == "(" or exp_reg[i+1] == "#":
                        exp_reg = exp_reg[:i+1] + "." + exp_reg[i+1:]
                        i+=2
                        continue
                    else:
                        i+=1
            else:
                i+=1
        return exp_reg
    
    def postfix(self, exp_reg:str):
        input = exp_reg.strip().replace(' ', '')
        pilha = []
        output = []
        for carac in input:
            if carac in self.alfabeto:
                output.append(carac)
            elif carac == "#":
                output.append("#")
            elif carac == "(":
                pilha.append(carac)
            elif carac == ")":
                while pilha[-1] != "(":
                    output.append(pilha.pop())
                pilha.pop()
            elif carac in self.operacoes:
                while (pilha and pilha[-1] != '(' and self.precedencia[pilha[-1]] >= self.precedencia[carac]):
                    output.append(pilha.pop())
                pilha.append(carac)
        while pilha:
            output.append(pilha.pop())
        return output



                

                    
        
