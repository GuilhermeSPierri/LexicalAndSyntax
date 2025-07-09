from algoritmos.first import *
from algoritmos.follow import *
from algoritmos.colecao_canonica import *
from algoritmos.tabela_analisador import *
from algoritmos.closure import *
from src.gramatica import *
from src.AnalisadorSintaticoSLR import *

tokens = []
""" 
    # Declaração de variável
    ("var", "var"),
    ("id", "x"),
    (":", ":"),
    ("inteiro", "inteiro"),
    (";", ";"),
    
    # Comandos (mínimo: bloco vazio)
    ("inicio", "inicio"),
    ("fim", "fim"),
    
    # Ponto final
    (".", "."),
    
    # Fim de entrada
    ("$", "$") """

with open('tokens.txt', 'r') as file:
    for line in file:
        line.replace('<', '').replace('>', '')
        tokens.append(line.strip().split(','))

print(tokens)

analisador = SyntaxAnalyzerSLR()
analisador.load_grammar("teste.txt")  # Arquivo com a gramática
analisador.compute_first()
analisador.compute_follow()
analisador.build_canonical_collection()
analisador.build_slr_table()
analisador.parse(tokens)


print("First : ",  analisador.first_sets)
print("Follow : ", analisador.follow_sets)