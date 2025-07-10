from Lexico.algoritmos.tabela_simbolos import criar_tabela_simbolos
from Lexico.src.interface import mostrar_interface_interativa
from Lexico.src.exp_reg import Exp_Reg
from Lexico.algoritmos.uniao_automatos import uniao_automatos
from Lexico.algoritmos.testar_word import testar_word
from Lexico.algoritmos.er_afd import criar_arvore
from Lexico.algoritmos.def_afd import *
from Lexico.algoritmos.determinizacao_de_automatos import *
from Sintatico.algoritmos.first import *
from Sintatico.algoritmos.follow import *
from Sintatico.algoritmos.colecao_canonica import *
from Sintatico.algoritmos.tabela_analisador import *
from Sintatico.algoritmos.closure import *
from Sintatico.src.gramatica import *
from Sintatico.src.AnalisadorSintaticoSLR import *
import ast

import re

def processar_entrada(er_text, def_text, teste_text):
    print("[DEBUG] Iniciando processar_entrada")
    operacoes = {"|","*",".","+","?"}
    afds_defs = []
    afds_ers = []

    # Processar ERs
    print("[DEBUG] Processando ERs")
    for i, linha in enumerate(er_text.splitlines()):
        print(f"[DEBUG] ER linha {i+1}: {linha}")
        linha = linha.strip().replace(" ", "")
        if ':' in linha:
            pos = linha.find(":")
            nome = linha[:pos]
            exp_reg = linha[pos+1:].strip()
            print(f"[DEBUG] Processando ER '{nome}': {exp_reg}")
            
            alfabeto = gerar_alfabeto(exp_reg, operacoes)
            print(f"[DEBUG] Alfabeto para {nome}: {alfabeto}")
            
            exp_reg_obj = Exp_Reg(exp_reg, alfabeto, operacoes)
            arv = criar_arvore(exp_reg_obj)
            afd = arv.criar_AFD()
            afd.nome = nome
            afds_ers.append(afd)
            print(f"[DEBUG] AFD para {nome} criado com {len(afd.transicoes)} transições")

    # Processar DEFs
    print("[DEBUG] Processando DEFs")
    for i, linha in enumerate(def_text.splitlines()):
        print(f"[DEBUG] DEF linha {i+1}: {linha}")
        linha = linha.strip().replace(" ", "")
        if ':' in linha:
            pos = linha.find(":")
            nome = linha[:pos]
            def_reg = linha[pos+1:].strip()
            print(f"[DEBUG] Processando DEF '{nome}': {def_reg}")
            
            exp_reg = formatar_def_reg(def_reg)
            print(f"[DEBUG] DEF formatada: {exp_reg}")
            
            alfabeto = gerar_alfabeto(exp_reg, operacoes)
            print(f"[DEBUG] Alfabeto para {nome}: {alfabeto}")
            
            exp_reg_obj = Exp_Reg(exp_reg, alfabeto, operacoes)
            arv = criar_arvore(exp_reg_obj)
            afd = arv.criar_AFD()
            afd.nome = nome
            afds_defs.append(afd)
            print(f"[DEBUG] AFD para {nome} criado com {len(afd.transicoes)} transições")

    # União dos AFDs
    print("[DEBUG] União dos AFDs de ERs")
    uniao_ers = uniao_automatos(afds_ers)
    print(f"[DEBUG] União ERs criada com {len(uniao_ers.transicoes)} transições")
    
    print("[DEBUG] Determinização ERs")
    afd_ersFinal = determinizacao_de_automato(uniao_ers)
    print(f"[DEBUG] AFD ER final criado com {len(afd_ersFinal.transicoes)} transições")
    
    print("[DEBUG] União dos AFDs de DEFs")
    uniao_defs = uniao_automatos(afds_defs)
    print(f"[DEBUG] União DEFs criada com {len(uniao_defs.transicoes)} transições")
    
    print("[DEBUG] Determinização DEFs")
    afd_defsFinal = determinizacao_de_automato(uniao_defs)
    print(f"[DEBUG] AFD DEF final criado com {len(afd_defsFinal.transicoes)} transições")

    tokens = []
    posicoes = []

    token_pattern = r':=|[<>]=?|\.\.|!=|"[^"]*"|[a-zA-Z_][a-zA-Z0-9_]*|[0-9]*\.[0-9]+|[0-9]+\.[0-9]*|[0-9]+|[=+\-*/,;.:()\[\]{}<>]|\.'

    keywords = [
        "const","var","proc","funcao","ref","val","intervalo","cadeia",
        "vetor","de","inteiro","real","booleano","caracter","inicio",
        "fim","se","entao","senao","enquanto","faca","repita","ate",
        "leia","escreva","ou","e","nao","falso","verdadeiro"
    ]

    print(f"[DEBUG] Padrão de tokenização: {token_pattern}")
    
    for num_linha, linha in enumerate(teste_text.splitlines()):
        linha = linha.strip()
        print("LINHA: ", linha)
        if not linha:
            continue
        
        print(f"[DEBUG] Processando linha {num_linha+1}: {linha}")
        tokens_linha = re.findall(token_pattern, linha)
        print(f"[DEBUG] Tokens encontrados: {tokens_linha}")
        
        for token_str in tokens_linha:
            print(f"[DEBUG] Processando token: '{token_str}'")
            
            # 1. Testar primeiro no AFD de ERs (mais específico)
            print(f"[DEBUG] Testando token '{token_str}' no AFD ER")
            pertence_er, afd_er_copy = testar_word(afd_ersFinal, token_str)
            
            if pertence_er:
                estado_final = afd_er_copy.estado_atual
                token_tipo = afd_er_copy.mapa_estados_finais.get(estado_final)
                tokens.append(f"<('{token_str}','{token_tipo}')>")
                posicoes.append(num_linha+1)
                print(f"[DEBUG] Token reconhecido como ER: {token_str} -> {token_tipo}")
            else:
                # 2. Se não for ER, testar no AFD de DEFs
                print(f"[DEBUG] Testando token '{token_str}' no AFD DEF")
                pertence_def, afd_def_copy = testar_word(afd_defsFinal, token_str)
                
                if pertence_def:
                    estado_final = afd_def_copy.estado_atual
                    print(afd_def_copy.mapa_estados_finais, "estado_final: ", estado_final)
                    token_tipo = afd_def_copy.mapa_estados_finais.get(estado_final)
                    if token_str in keywords:
                        token_tipo = token_str
                    tokens.append(f"<('{token_str}','{token_tipo}')>")
                    posicoes.append(num_linha+1)
                    print(f"[DEBUG] Token reconhecido como DEF: {token_str} -> {token_tipo}")

    tabela = criar_tabela_simbolos(tokens, posicoes)
    
    with open("tokens.txt", 'w', encoding='utf-8') as f:
        for token in tokens:
            f.write(token + '\n')

    print(f"Tokens gravados em: tokens.txt")
    return tokens, tabela, afd_defsFinal

def realizar_analise_sintatica():
    tokens = []
    with open('tokens.txt', 'r') as file:
        for line in file:
            line = line.replace('<', '').replace('>', '')
            tup = ast.literal_eval(line.strip())
            tokens.append(tup)

    print("Tokens para análise sintática:", tokens)

    analisador = SyntaxAnalyzerSLR()
    analisador.load_grammar("teste.txt")  # Arquivo com a gramática
    analisador.compute_first()
    analisador.compute_follow()
    analisador.build_canonical_collection()
    analisador.build_slr_table()
    resultado = analisador.parse(tokens)

    print("First:", analisador.first_sets)
    print("Follow:", analisador.follow_sets)
    return {
        "first": analisador.first_sets,
        "follow": analisador.follow_sets,
        "resultado": resultado
    }

if __name__ == "__main__":

    mostrar_interface_interativa(processar_entrada)