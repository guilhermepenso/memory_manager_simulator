from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tkinter.simpledialog
from tkinter import ttk
import itertools
import random
import string
def gerador_nome_processo():
    tamanho = 1
    while True:
        for s in itertools.product(string.ascii_uppercase, repeat=tamanho):
            yield "".join(s)
        tamanho += 1
class GerenciadorMemoria:
    def __init__(self, mestre):
        self.mestre = mestre
        self.grade = [None] * 100
        self.grupos = {}
        self.chars = gerador_nome_processo()
        self.status = [0] * 100
        self.criar_grade()
    def criar_grade(self):
        quadro = tk.Frame(self.mestre)
        quadro.pack(expand=True)
        for i in range(100):
            rotulo = tk.Label(quadro, bg="white", width=10, height=3, relief="solid", borderwidth=1.2)
            rotulo.grid(row=i//10, column=i%10)
            self.grade[i] = rotulo
    def alocar(self):
        n = tkinter.simpledialog.askinteger("Alocar", "Digite o Tamanho do Processo")
        blocos_livres = []
        best_fit = None
        total_livre = 0
        for i in range(100):
            if self.status[i] == 0:
                total_livre += 1
                blocos_livres.append(i)
            else:
                if len(blocos_livres) >= n:
                    if best_fit is None or len(best_fit) > len(blocos_livres):
                        best_fit = list(blocos_livres)
                blocos_livres = []
        if len(blocos_livres) >= n:
            if best_fit is None or len(best_fit) > len(blocos_livres):
                best_fit = list(blocos_livres)
        if total_livre < n:
            messagebox.showinfo("Erro", "Sem Espaço Total")
            return
        if best_fit is None:
            messagebox.showinfo("Erro", "Sem Espaço Sequencial")
            return
        cor_bloco = "#{:06x}".format(random.randint(0x0000, 0xFFFFFF))
        nome_bloco = next(self.chars)
        for k in range(n):
            self.grade[best_fit[k]]["text"] = nome_bloco
            self.grade[best_fit[k]]["background"] = cor_bloco
            self.grupos[nome_bloco] = cor_bloco
            self.status[best_fit[k]] = 1
    def desalocar(self):
        d = tkinter.simpledialog.askstring("Desalocar", "Digite o Nome do Processo")
        for i in range(100):
            if self.grade[i]["text"] == d.upper():
                self.grade[i]['background'] = "white"
                self.grade[i]["text"] = ""
                self.status[i] = 0
    def limpar_processos(self):
        for i in range(100):
            if self.status[i] == 1:
                self.grade[i]["background"] = "white"
                self.grade[i]["text"] = ""
                self.status[i] = 0
    def realocar(self):
        tamanho_memoria = 0
        texto_memoria = None
        for pos in range(1, 100):
            if self.status[pos - 1] == 0 and self.status[pos] == 1:
                texto_memoria = self.grade[pos]["text"]
                while pos < 100 and self.grade[pos]["text"] == texto_memoria:
                    tamanho_memoria += 1
                    pos += 1
                break
        if texto_memoria is None:
            return self.grade
        for pos in range(100):
            if texto_memoria == self.grade[pos]["text"]:
                self.grade[pos]["text"] = ""
                self.grade[pos]["background"] = "white"
                self.status[pos] = 0
        for pos in range(100):
            if self.status[pos] == 0 and tamanho_memoria > 0:
                self.grade[pos]["text"] = texto_memoria
                self.grade[pos]["background"] = self.grupos[texto_memoria]
                self.status[pos] = 1
                tamanho_memoria -= 1
        return self.grade
    def ajuda(self):
        janela_ajuda = tk.Toplevel()
        janela_ajuda.title("Ajuda")
        largura_ajuda = 600
        altura_ajuda = 300
        largura_tela = raiz.winfo_screenwidth()
        altura_tela = raiz.winfo_screenheight()
        x = (largura_tela/2) - (largura_ajuda/2)
        y = (altura_tela/2) - (altura_ajuda/2)
        janela_ajuda.geometry('%dx%d+%d+%d' % (largura_ajuda, altura_ajuda, x, y))
        Info = Label(janela_ajuda, text="Explicação do funcionamento de cada botão")
        Info.pack(padx=10, pady=10)
        nb = ttk.Notebook(janela_ajuda, width=600, height=400)
        nb.pack(padx=10, pady=10)
        funcionamento = Frame(nb)
        nb.add(funcionamento, text="Funcionamento do Programa")
        label_funcionamento = Label(funcionamento,
                                    text="Esse Programa simula uma memória de um computador.\nVocê poderá alocar processos em uma memória com até 100 blocos de memória\n os processos serão criadas em ordem alfabética e cores aleatórias.\nVocê poderá desalocar um processo especifico da memória ou limpar todos os processos.\nConforme o uso do programa haverá espaços vazios no meio de processos que não podem ser alocados\n com processos maiores, então o programa possui um meio de realocar os blocos de processos até o inicio\n da memória e liberar o mesmo espaço vazio para a parte final da memória.")
        label_funcionamento.pack(pady=20, anchor=CENTER, fill="both")
        label_criadores = Label(funcionamento,
                                text="Desenvolvido por: Guilherme Penso, Matheus Guilherme, Murilo Lustosa\n e Emanoel Andre.")
        label_criadores.pack(padx=10, pady=0)
        label_criadores.config(font="Arial 12")
        Alocar = Frame(nb)
        label_info = Label(Alocar, text="Funcionamento do Botão Alocar.")
        label_info.pack(padx=10, pady=10)
        mensagealocar = Label(Alocar, 
                              text="Antes de alocar um processo, a memória estará vazia. Após o clicar no botão Alocar, abrirá uma aba\n onde é possível adicionar o tamanho de um processo com números inteiros, após confirmar\n o tamanho, a Memória adicionará um processo com a quantidade de blocos nomeada de forma sequencial\n do alfabeto e cor aleatória.")
        mensagealocar.pack()
        nb.add(Alocar, text="Alocar")
        Desalocar = Frame(nb)
        label_info2 = Label(Desalocar, text="Funcionamento do Botão Desalocar.")
        label_info2.pack(padx=10, pady=10)
        mensagedesalocar = Label(Desalocar, 
                                 text="A Memória estando com um processo, é possível desalocar com a letra correspondente\n ao processo, que irá remover o processo em específico.")
        mensagedesalocar.pack()
        nb.add(Desalocar, text="Desalocar")
        Desalocar_tudo = Frame(nb)
        label_info3 = Label(Desalocar_tudo, text="Funcionamento do Botão Limpar Processos.")
        label_info3.pack(padx=10, pady=10)
        mensagelimpar1 = Label(Desalocar_tudo, 
                               text="A Memória estando com alguns processos, é possível apagar tudo ao clicar.")
        mensagelimpar1.pack()
        nb.add(Desalocar_tudo, text="Limpar Processos")
        Realocar = Frame(nb)
        label_info4 = Label(Realocar, text="Funcionamento do Botão Limpar Processos.")
        label_info4.pack(padx=10, pady=10)
        mensageRealocar = Label(Realocar,
                                 text="Com espaços vazios entre os processos que podem ser reutilizados para alocar outros processos, a \ncada clique será realocado o primeiro bloco de processo que tenha espaço vazio antes de seu início. ")
        mensageRealocar.pack()
        nb.add(Realocar, text="Realocar")
raiz = tk.Tk()
largura_menu = 800
altura_menu = 600
raiz.resizable(0, 0)
raiz.title('Gerenciador de Memória')
largura_tela = raiz.winfo_screenwidth()
altura_tela = raiz.winfo_screenheight()
x = (largura_tela/2) - (largura_menu/2)
y = (altura_tela/2) - (altura_menu/2)
raiz.geometry('%dx%d+%d+%d' % (largura_menu, altura_menu, x, y))
mm = GerenciadorMemoria(raiz)
quadro_botao = tk.Frame(raiz)
quadro_botao.pack(side="top", fill="x", pady=20)
botao_alocar = tk.Button(quadro_botao, text="Alocar", command=mm.alocar, height=5, width=21, bg='gray', borderwidth=0)
botao_alocar.pack(side="left", padx=5)
botao_desalocar = tk.Button(quadro_botao, text="Desalocar", command=mm.desalocar, height=5, width=21, bg='gray', borderwidth=0)
botao_desalocar.pack(side="left", padx=5)
botao_limpar_processos = tk.Button(quadro_botao, text="Limpar Processos", command=mm.limpar_processos, height= 5, width=21, bg='gray', borderwidth=0)
botao_limpar_processos.pack(side='left', padx=5)
botao_realocar = tk.Button(quadro_botao, text="Realocar", command=mm.realocar, height=5, width=21, bg='gray', borderwidth=0)
botao_realocar.pack(side="left", padx=5)
botao_ajuda = tk.Button(quadro_botao,text="Ajuda",command=mm.ajuda, height=5, width=21,bg='gray',borderwidth=0)
botao_ajuda.pack(side="left", padx=5)
raiz.mainloop()