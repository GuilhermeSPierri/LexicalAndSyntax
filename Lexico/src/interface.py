import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def mostrar_interface_interativa(processar_callback):
    root = tk.Tk()
    root.title("Gerador de Analisadores Léxicos")
    root.geometry("580x700") 

    frame_botoes = ttk.Frame(root)
    frame_botoes.pack(fill="x", padx=10, pady=5)
    
    def carregar_def():
        caminho = filedialog.askopenfilename(
            title="Selecione um arquivo de definição regular",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if not caminho:
            return
            
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                
            # Separar ERs e DEFs
            er_lines = []
            def_lines = []
            for linha in conteudo.splitlines():
                linha = linha.strip()
                if linha.startswith("er") and ':' in linha:
                    er_lines.append(linha)
                elif ':' in linha:
                    def_lines.append(linha)
                    
            text_def.delete("1.0", tk.END)
            text_def.insert(tk.END, "\n".join(def_lines))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao ler arquivo:\n{str(e)}")
    
    btn_carregar_gramatica = ttk.Button(
        frame_botoes, 
        text="Carregar Definição Regular",
        command=carregar_def
    )
    btn_carregar_gramatica.pack(side="left", padx=5)

    def carregar_expressao_regular():
        caminho = filedialog.askopenfilename(
            title="Selecione um arquivo de expressão regular",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if not caminho:
            return

        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
            text_er.delete("1.0", tk.END)
            text_er.insert(tk.END, conteudo)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao ler arquivo:\n{str(e)}")

    btn_carregar_expressao_regular = ttk.Button(
        frame_botoes, 
        text="Carregar Expressão Regular",
        command=carregar_expressao_regular
    )
    btn_carregar_expressao_regular.pack(side="left", padx=5)
    
    # Botão para carregar arquivo de entrada
    def carregar_entrada():
        caminho = filedialog.askopenfilename(
            title="Selecione um arquivo de entrada",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if not caminho:
            return
            
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                
            text_teste.delete("1.0", tk.END)
            text_teste.insert(tk.END, conteudo)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao ler arquivo:\n{str(e)}")
    
    btn_carregar_entrada = ttk.Button(
        frame_botoes, 
        text="Carregar Entrada",
        command=carregar_entrada
    )
    btn_carregar_entrada.pack(side="left", padx=5)
    
    # Botão para limpar todos os campos
    def limpar_campos():
        text_er.delete("1.0", tk.END)
        text_def.delete("1.0", tk.END)
        text_teste.delete("1.0", tk.END)
    
    btn_limpar = ttk.Button(
        frame_botoes, 
        text="Limpar Campos",
        command=limpar_campos
    )
    btn_limpar.pack(side="right", padx=5)

    # Segmento para ERentrada
    frame_er = ttk.LabelFrame(root, text="Expressões Regulares (ER)")
    frame_er.pack(fill="x", padx=10, pady=5)
    text_er = tk.Text(frame_er, height=5, width=80)
    scroll_er = ttk.Scrollbar(frame_er, command=text_er.yview)
    text_er.configure(yscrollcommand=scroll_er.set)
    text_er.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    scroll_er.pack(side="right", fill="y", padx=(0,5), pady=5)
    text_er.insert(tk.END, "er1: a?(a|b)+\ner2: b?(a|b)+")  # Exemplo

    # Segmento para DEFentrada
    frame_def = ttk.LabelFrame(root, text="Definições Regulares (DEF)") 
    frame_def.pack(fill="x", padx=10, pady=5)
    text_def = tk.Text(frame_def, height=5, width=80)
    scroll_def = ttk.Scrollbar(frame_def, command=text_def.yview)
    text_def.configure(yscrollcommand=scroll_def.set)
    text_def.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    scroll_def.pack(side="right", fill="y", padx=(0,5), pady=5)
    text_def.insert(tk.END, "id: [a-zA-Z]([a-zA-Z] | [0-9])*\nnum: [1-9]([0-9])* | 0")  # Exemplo

    # Segmento para arquivo_teste
    frame_teste = ttk.LabelFrame(root, text="Entrada")
    frame_teste.pack(fill="x", padx=10, pady=5)
    text_teste = tk.Text(frame_teste, height=16, width=80)
    scroll_teste = ttk.Scrollbar(frame_teste, command=text_teste.yview)
    text_teste.configure(yscrollcommand=scroll_teste.set)
    text_teste.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    scroll_teste.pack(side="right", fill="y", padx=(0,5), pady=5)
    text_teste.insert(tk.END, "a1\n0\nteste2\n21\nalpha123\n3444\na43teste\naa\nbbbba\nababab\nbbbbb")  # Exemplo

    # Função para mostrar tokens e tabela após processamento
    def mostrar_resultado(tokens, tabela, afd=None):
        resultado = tk.Toplevel(root)
        resultado.title("Tokens e Tabela de Símbolos")
        resultado.geometry("500x720")

        frame_tokens = ttk.LabelFrame(resultado, text="Tokens")
        frame_tokens.pack(fill="x", padx=10, pady=5)
        listbox_tokens = tk.Listbox(frame_tokens, height=16, width=80)
        for token in tokens:
            listbox_tokens.insert(tk.END, token)
        listbox_tokens.pack(fill="x", padx=5, pady=5)

        frame_tabela = ttk.LabelFrame(resultado, text="Tabela de Símbolos")
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=5)
        colunas = ("Lexema", "Tipo", "Posição")

        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", relief="ridge", borderwidth=2, font=("Arial", 10, "bold"))
        style.configure("Custom.Treeview", rowheight=25, borderwidth=2, relief="ridge")
        style.map("Custom.Treeview.Heading", background=[('active', '#e1e1e1')])

        tree = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings",
            style="Custom.Treeview"
        )
        for col in colunas:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=150, anchor="center")
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        for simbolo in tabela.tabela:
            tree.insert("", tk.END, values=(simbolo["lexema"], simbolo["tipo"], simbolo["posicao"]))

        # Botão para visualizar o AFD
        def visualizar_afd():
            if afd is None:
                tk.messagebox.showinfo("AFD", "AFD não disponível.")
                return
            janela_afd = tk.Toplevel(resultado)
            janela_afd.title("Visualização do AFD")
            janela_afd.geometry("600x500")

            text = tk.Text(janela_afd, wrap="word", font=("Consolas", 10))
            text.pack(fill="both", expand=True, padx=10, pady=10)

            # Exibe a quíntupla
            text.insert(tk.END, "Quíntupla do AFD:\n")
            text.insert(tk.END, f"Estados (K): {afd.estados}\n")
            text.insert(tk.END, f"Alfabeto (Σ): {afd.alfabeto}\n")
            text.insert(tk.END, f"Estado inicial (q0): {afd.estado_inicial}\n")
            text.insert(tk.END, f"Estados finais (F): {afd.estados_finais}\n")
            text.insert(tk.END, "Transições (δ):\n")
            for trans in afd.transicoes:
                text.insert(tk.END, f"  δ({trans.estado1}, {trans.simbolo}) -> {trans.estado2}\n")

            text.config(state="disabled")

        btn_afd = ttk.Button(resultado, text="Visualizar AFD", command=visualizar_afd)
        btn_afd.pack(pady=10)

        def ao_analise_sintatica():
            try:
                from main import realizar_analise_sintatica
                data = realizar_analise_sintatica()
                
                janela_resultado = tk.Toplevel(root)
                janela_resultado.title("Resultado da Análise Sintática")
                janela_resultado.geometry("600x400")
                
                texto = tk.Text(janela_resultado, wrap="word")
                texto.pack(fill="both", expand=True, padx=10, pady=10)
                
                texto.insert(tk.END, "Conjuntos FIRST:\n")
                for nt, first in data["first"].items():
                    texto.insert(tk.END, f"{nt}: {first}\n")
                
                texto.insert(tk.END, "\nConjuntos FOLLOW:\n")
                for nt, follow in data["follow"].items():
                    texto.insert(tk.END, f"{nt}: {follow}\n")
                
                texto.insert(tk.END, "\nResultado da análise: ")
                texto.insert(tk.END, "Sucesso!" if data["resultado"] else "Erro!")
                
                texto.config(state="disabled")
                
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        
        btn_sintatico = ttk.Button(
            resultado, 
            text="Realizar Análise Sintática",
            command=ao_analise_sintatica
        )
        btn_sintatico.pack(pady=10)

    # Ajuste ao_processar para passar o AFD para mostrar_resultado
    def ao_processar():
        er_text = text_er.get("1.0", tk.END).strip()
        def_text = text_def.get("1.0", tk.END).strip()
        teste_text = text_teste.get("1.0", tk.END).strip()
        try:
            tokens, tabela, afd = processar_callback(er_text, def_text, teste_text)
            mostrar_resultado(tokens, tabela, afd)
        except Exception as e:
            messagebox.showerror("Erro ao processar", str(e))

    btn_processar = ttk.Button(root, text="Processar", command=ao_processar)
    btn_processar.pack(pady=10)

    root.mainloop()