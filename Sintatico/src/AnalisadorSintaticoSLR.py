from Sintatico.algoritmos.closure import closure
from Sintatico.algoritmos.colecao_canonica import items
from Sintatico.algoritmos.first import compute_first
from Sintatico.algoritmos.follow import compute_follow_sets


class SyntaxAnalyzerSLR:
    def __init__(self):
        self.productions = {}
        self.start_symbol = None
        self.first_sets = {}
        self.follow_sets = {}
        self.canonical_collection = []
        self.action_table = {}
        self.goto_table = {}
        self.productions_list = []  # Lista plana de todas as produções
    
    def load_grammar(self, filename):
        """
        Carrega a gramática de um arquivo
        """
        self.productions = {}
        self.start_symbol = None
        
        try:
            with open(filename, 'r') as file:
                grammar_str = file.read()
        except FileNotFoundError:
            raise ValueError(f"Arquivo não encontrado: {filename}")
        
        lines = grammar_str.strip().split('\n')
        valid_productions = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Ignora linhas vazias e comentários
            
            # Verifica se é uma linha de produção
            if "::=" not in line:
                continue
                
            head_part, body_part = line.split("::=", 1)
            head = head_part.strip().replace('<', '').replace('>', '')
            
            # Se é o primeiro símbolo válido, define como start symbol
            if not self.start_symbol:
                self.start_symbol = head  # Garante que é uma string, não uma lista
            
            alternatives = []
            for alt in body_part.split('|'):
                alt = alt.strip()
                symbols = []
                
                # Processa símbolos especiais
                if alt == '&':
                    alternatives.append([])
                    continue
                
                # Tokenização inteligente
                while alt:
                    alt = alt.strip()
                    
                    # Símbolo entre chaves < >
                    if alt.startswith('<'):
                        end_pos = alt.find('>')
                        if end_pos == -1:
                            symbol = alt[1:]  # Pega até o final
                            alt = ''
                        else:
                            symbol = alt[1:end_pos]
                            alt = alt[end_pos+1:].strip()
                        symbols.append(symbol)
                    
                    # Terminal entre aspas
                    elif alt.startswith('"'):
                        end_pos = alt.find('"', 1)
                        if end_pos == -1:
                            symbol = alt[1:]  # Pega até o final
                            alt = ''
                        else:
                            symbol = alt[1:end_pos]
                            alt = alt[end_pos+1:].strip()
                        symbols.append(symbol)
                    
                    # Palavra sem formatação
                    else:
                        # Encontra próximo espaço ou fim
                        space_pos = alt.find(' ')
                        if space_pos == -1:
                            symbol = alt
                            alt = ''
                        else:
                            symbol = alt[:space_pos]
                            alt = alt[space_pos+1:].strip()
                        symbols.append(symbol)
                
                alternatives.append(symbols)
            
            # Adiciona ao dicionário de produções
            if head not in self.productions:
                self.productions[head] = []
            self.productions[head].extend(alternatives)
            valid_productions = True
        
        # Verifica se encontrou produções válidas
        if not valid_productions:
            raise ValueError("Nenhuma produção válida encontrada no arquivo")
        
        # Garante que temos um símbolo inicial string
        if not self.start_symbol:
            raise ValueError("Símbolo inicial não definido")
        elif isinstance(self.start_symbol, list):  # Correção adicional
            self.start_symbol = self.start_symbol[0]
    
    def compute_first(self):
        self.first_sets = compute_first(self.productions)
    
    def compute_follow(self):
        if self.first_sets is None:
            self.compute_first()
        self.follow_sets = compute_follow_sets(self.productions, self.start_symbol, self.first_sets)
    
    def build_canonical_collection(self):
        self.canonical_collection = items(self.productions, self.start_symbol)
    
    def build_slr_table(self):
        """Constrói a tabela SLR com resolução automática de conflitos shift/reduce"""
        action = {}
        goto = {}
        prod_list = []
        
        # 1. Lista plana de produções
        prod_list.append(("S'", [self.start_symbol]))
        for A, bodies in self.productions.items():
            for body in bodies:
                prod_list.append((A, body))
        
        # 2. Construir tabelas
        for i, state in enumerate(self.canonical_collection):
            # 2(a): Ações shift
            for item in state:
                A, alpha, beta = item
                if beta:
                    X = beta[0]
                    # Encontrar estado destino
                    dest_state = None
                    for j, target in enumerate(self.canonical_collection):
                        if (A, alpha + (X,), beta[1:]) in target:
                            dest_state = j
                            break
                    
                    if dest_state is not None:
                        if X in self.productions:  # Não-terminal: GOTO
                            goto[(i, X)] = dest_state
                        else:  # Terminal: SHIFT
                            # Resolver conflito shift/reduce priorizando shift
                            if (i, X) in action:
                                existing_action = action[(i, X)]
                                if existing_action[0] == 'reduce':
                                    # Shift tem prioridade sobre reduce
                                    print(f"AVISO: Conflito shift/reduce resolvido no estado {i}, símbolo '{X}' (priorizando shift)")
                                    action[(i, X)] = ('shift', dest_state)
                                else:
                                    raise RuntimeError(f"Conflito SLR no estado {i}, símbolo '{X}': "
                                                    f"Existente: {existing_action}, Novo: shift {dest_state}")
                            else:
                                action[(i, X)] = ('shift', dest_state)
            
            # 2(b) e 2(c): Ações reduce e accept
            for item in state:
                A, alpha, beta = item
                if not beta:  # Item completo
                    if A == "S'":  # Aceitação
                        if (i, '$') in action:
                            existing_action = action[(i, '$')]
                            if existing_action[0] != 'accept':
                                raise RuntimeError(f"Conflito SLR no estado {i}, símbolo '$': "
                                                f"Existente: {existing_action}, Novo: accept")
                        else:
                            action[(i, '$')] = ('accept',)
                    else:
                        # Encontrar índice da produção
                        alpha_list = list(alpha)
                        prod_idx = None
                        for idx, (head, body) in enumerate(prod_list):
                            if head == A and body == alpha_list:
                                prod_idx = idx
                                break
                        
                        if prod_idx is not None:
                            # Para todos os símbolos em FOLLOW(A)
                            for a in self.follow_sets[A]:
                                # Ignorar símbolo vazio
                                if a == '&':
                                    continue
                                
                                # Resolver conflito shift/reduce priorizando shift
                                if (i, a) in action:
                                    existing_action = action[(i, a)]
                                    
                                    # Shift tem prioridade sobre reduce
                                    if existing_action[0] == 'shift':
                                        print(f"AVISO: Conflito shift/reduce resolvido no estado {i}, símbolo '{a}' (priorizando shift)")
                                        continue
                                    
                                    # Conflito reduce/reduce é erro fatal
                                    if existing_action[0] == 'reduce':
                                        raise RuntimeError(f"Conflito reduce/reduce no estado {i}, símbolo '{a}': "
                                                        f"Produção existente: {prod_list[existing_action[1]]}, "
                                                        f"Nova produção: {A} → {alpha}")
                                
                                # Adicionar ação de reduce se não houver conflito
                                action[(i, a)] = ('reduce', prod_idx)
        
        # Armazenar tabelas como atributos da classe
        self.action_table = action
        self.goto_table = goto
        self.productions_list = prod_list
        
        return action, goto, prod_list
    
    def find_goto_dest(self, state_index, X):
        """Encontra o estado destino para GOTO(state_index, X)"""
        current_state = self.canonical_collection[state_index]
        next_items = set()
        
        # Avança o ponto sobre X
        for item in current_state:
            A, alpha, beta = item
            if beta and beta[0] == X:
                new_alpha = alpha + (X,)
                new_beta = beta[1:]
                next_items.add((A, new_alpha, new_beta))
        
        if not next_items:
            return None
        
        # Calcula fechamento do novo conjunto
        closure_next = closure(next_items, self.productions)
        
        # Procura estado correspondente na coleção canônica
        for j, state in enumerate(self.canonical_collection):
            if state == closure_next:
                return j
        
        return None
    
    def find_production_index(self, A, alpha):
        """Encontra o índice de uma produção na lista plana"""
        for idx, (head, body) in enumerate(self.productions_list):
            if head == A and body == alpha:
                return idx
        return None
    
    def handle_conflict(self, state, symbol, new_action, existing_action):
        """Trata conflitos na tabela ACTION"""
        error_msg = (
            f"Conflito SLR no estado {state}, símbolo '{symbol}': "
            f"Ação existente: '{existing_action}', Nova ação: '{new_action}'"
        )
        raise RuntimeError(error_msg)
    
    def print_tables(self):
        """Exibe as tabelas ACTION e GOTO formatadas"""
        print("\nTabela ACTION:")
        print("Estado\tSímbolo\tAção")
        for (state, symbol), action in self.action_table.items():
            print(f"{state}\t{symbol}\t{action}")
        
        print("\nTabela GOTO:")
        print("Estado\tSímbolo\tDestino")
        for (state, symbol), dest in self.goto_table.items():
            print(f"{state}\t{symbol}\t{dest}")

    def parse(self, tokens):
        """Implementação do algoritmo de parsing LR da Figura 4.36"""
        stack = [0]  # Pilha de estados
        output = []  # Produções aplicadas
        token_index = 0
        current_token = tokens[token_index] if tokens else ('$', '$')
        
        while True:
            state = stack[-1]
            token_type, token_value = current_token
            
            # Determinar símbolo para consulta na tabela
            symbol = token_value
            
            # 1. Tentar encontrar ação usando valor do token
            action = self.action_table.get((state, symbol))
            
            # 2. Se não encontrar, tentar usar tipo do token
            if action is None:
                symbol = token_type
                action = self.action_table.get((state, symbol))
            
            # 3. Se ainda não encontrou, gerar erro
            if action is None:
                # Listar símbolos esperados para este estado
                expected_symbols = set()
                for (s, sym), act in self.action_table.items():
                    if s == state:
                        expected_symbols.add(sym)
                raise RuntimeError(
                    f"Erro sintático no estado {state}: "
                    f"Token '{token_value}' inesperado. Esperados: {', '.join(expected_symbols)}"
                )
            
            # 4. Shift
            if action[0] == 'shift':
                next_state = action[1]
                stack.append(next_state)
                token_index += 1
                if token_index < len(tokens):
                    current_token = tokens[token_index]
                else:
                    current_token = ('$', '$')
                continue
            
            # 5. Reduce
            if action[0] == 'reduce':
                prod_idx = action[1]
                A, body = self.productions_list[prod_idx]
                
                # Pop |body| símbolos (se não for produção vazia)
                if body:
                    stack = stack[:-len(body)]
                
                # Estado atual após pop
                t = stack[-1]
                
                # Consultar GOTO table
                next_state = self.goto_table.get((t, A))
                if next_state is None:
                    raise RuntimeError(f"Erro de GOTO no estado {t} para não-terminal {A}")
                
                # Empilhar novo estado
                stack.append(next_state)
                
                # Registrar produção aplicada
                output.append((A, body))
                continue
            
            # 6. Accept
            if action[0] == 'accept':
                break
        
        return output