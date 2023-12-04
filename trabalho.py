from time import sleep
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
class Noh:
    def __init__(self, documento, prioridade, nome_arquivo):
        # Criação de um nó com as informações do documento, prioridade e nome do arquivo.
        self.documento = documento
        self.prioridade = prioridade
        self.proximo = None
        self.anterior = None
        self.nome_arquivo = nome_arquivo

class Imprimir:
    def __init__(self):
        # Inicializa a classe de gerenciamento de impressão.
        self.primeiro = None
        self.ultimo = None

    def criar_noh(self, nome, prioridade):
        try:
            # Tenta abrir o arquivo e ler seu conteúdo.
            with open(nome, 'r') as arquivo:
                conteudo = arquivo.read()
                # Cria um novo nó com o conteúdo do arquivo, prioridade e nome do arquivo.
                novo_Noh = Noh(conteudo, prioridade, nome)
                return novo_Noh
        except FileNotFoundError:
            # Para caso o arquivo não for encontrado, imprime uma mensagem de erro.
            print(f'O Arquivo {nome} não foi encontrado :(')
            return None

    def adicionar_na_fila(self, novo_Noh, prioridade):
        if self.primeiro is None:
            # Se a fila estiver vazia, adiciona o novo nó como o primeiro e último
            self.primeiro = novo_Noh
            self.ultimo = novo_Noh
            print(f'Um novo documento {novo_Noh.nome_arquivo} entrou na fila')
        else:
            # Se a fila não estiver vazia, adiciona o novo nó na posição correta
            atual = self.primeiro
            while atual is not None and atual.prioridade >= prioridade:
                atual = atual.proximo

            if atual is None:
                # Adiciona o novo nó no final da fila
                self.ultimo.proximo = novo_Noh
                novo_Noh.anterior = self.ultimo
                self.ultimo = novo_Noh
            elif atual.anterior is None:
                # Se o novo nó for o mais prioritário, adiciona no início da fila
                novo_Noh.proximo = self.primeiro
                self.primeiro.anterior = novo_Noh
                self.primeiro = novo_Noh
            else:
                # Adiciona o novo nó no meio da fila
                novo_Noh.proximo = atual
                novo_Noh.anterior = atual.anterior
                atual.anterior.proximo = novo_Noh
                atual.anterior = novo_Noh
            print(f'Um novo documento {novo_Noh.nome_arquivo} entrou na fila!!')

    def adiciona(self, nome, prioridade):
        # Adiciona um novo documento à fila de impressão.
        novo_Noh = self.criar_noh(nome, prioridade)
        if novo_Noh:
            self.adicionar_na_fila(novo_Noh, prioridade)

    def remove(self, index):
        atual = self.primeiro
        count = 0

        while atual is not None:
            if count == index:
                if atual.anterior:
                    atual.anterior.proximo = atual.proximo
                else:
                    self.primeiro = atual.proximo
                if atual.proximo:
                    atual.proximo.anterior = atual.anterior
                else:
                    self.ultimo = atual.anterior
                return f'O documento {atual.nome_arquivo} foi removido da fila.'

            atual = atual.proximo
            count += 1

        return f'O documento não foi encontrado na fila.'

    def remover_documento_selecionado(self):
        selected_index = lista_documentos.curselection()

        if selected_index:
            mensagem = gerenciador.remove(selected_index[0])
            messagebox.showinfo("Remoção de Documento", mensagem)
            update_display()

    def imprime(self):
        if self.primeiro is None:
            # Se não houver arquivos para imprimir, exibe uma mensagem.
            print("Não há arquivos!!")
            return

        while self.primeiro is not None:
            atual = self.primeiro
            print(f'Imprimindo o arquivo {atual.nome_arquivo}, aguarde...')
            sleep(2)
            self.primeiro = atual.proximo
            if self.primeiro:
                self.primeiro.anterior = None
            else:
                self.ultimo = None
            print(f'O arquivo {atual.nome_arquivo} foi impresso!')
            sleep(2)
        update_display()

    def organiza(self):
        documentos_na_fila = []
        if self.primeiro is None:
            print('Não há documentos!!')
            return documentos_na_fila

        atual = self.primeiro
        while atual is not None:
            documento_info = (f'Grau de prioridade: {atual.prioridade}\n'
                              f'Tamanho: O arquivo possui {len(atual.documento)} caracteres')
            documentos_na_fila.append(documento_info)
            atual = atual.proximo
            if atual == self.primeiro:
                break

        return documentos_na_fila

# Cria uma instância da classe Imprimir.
gerenciador = Imprimir()

# Imprime
gerenciador.imprime()

arquivo_selecionado = None  # Variável global para armazenar o arquivo selecionado

def selecionar_arquivo():
    global arquivo_selecionado
    arquivo_selecionado = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo",
                                                     filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

def adicionar_documento():
    global arquivo_selecionado

    if arquivo_selecionado is None:
        messagebox.showerror("Erro", "Selecione um arquivo antes de adicionar!")
        return

    prioridade = entry_prioridade.get()

    if not prioridade:
        messagebox.showerror("Erro", "Digite um número de prioridade antes de adicionar!")
        return

    prioridade = int(prioridade)
    gerenciador.adiciona(arquivo_selecionado, prioridade)
    update_display()


def remover_documento_selecionado():
    gerenciador.remover_documento_selecionado()
    update_display()

def imprimir_documentos():
    gerenciador.imprime()
    update_display()

def update_display():
    lista_documentos.delete(0, tk.END)
    documentos_na_fila = gerenciador.organiza()
    for documento in documentos_na_fila:
        lista_documentos.insert(tk.END, documento)

root = tk.Tk()
root.title("Sistema de Impressão")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

label_nome_arquivo = tk.Label(frame, text="Busque o arquivo:")
label_nome_arquivo.grid(row=0, column=0, padx=5, pady=5)

button_selecionar = tk.Button(frame, text="Selecionar arquivo", command=selecionar_arquivo)
button_selecionar.grid(row=0, column=1, padx=5, pady=5)

label_prioridade = tk.Label(frame, text="Prioridade:")
label_prioridade.grid(row=1, column=0, padx=5, pady=5)

label_observação1 = tk.Label(frame, text="Presidente: Digite 3")
label_observação1.grid(row=2, column=0, padx=5, pady=5)

label_observação2 = tk.Label(frame, text="Assessor: Digite 2")
label_observação2.grid(row=2, column=1, padx=5, pady=5)

label_observação3 = tk.Label(frame, text="Trainee: Digite 1")
label_observação3.grid(row=2, column=2, padx=5, pady=5)

entry_prioridade = tk.Entry(frame, width=10)
entry_prioridade.grid(row=1, column=1, padx=5, pady=5)

button_adicionar = tk.Button(frame, text="Adicionar", command=adicionar_documento)
button_adicionar.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

button_imprimir = tk.Button(frame, text="Imprimir", command=imprimir_documentos)
button_imprimir.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

button_remover = tk.Button(frame, text="Remover Selecionado", command=remover_documento_selecionado)
button_remover.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

lista_documentos = tk.Listbox(root, width=70)
lista_documentos.pack(padx=20, pady=10)

root.mainloop()

