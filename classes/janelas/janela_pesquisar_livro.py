import sqlite3
import customtkinter
from functions.functions import *

def pesquisar_livros(admin=False):
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    if admin:
        cursor.execute("SELECT * FROM livro")
    else:
        cursor.execute("SELECT * FROM livro")
        pass
    return cursor.fetchall()

class JanelaPesquisarLivro:
    def __init__(self, user):
        self.logged_user = user 
        if user:
            conn = sqlite3.connect('livraria.db')
            cursor = conn.cursor()
            cursor.execute("Select role_name FROM roles where id = ?",(user['role'],))
            self.registering_role_name = cursor.fetchone()[0]
            conn.close()
            self.permission_list = list_permissions(user, self.registering_role_name)
        print(self.registering_role_name)
        self.pesquisar_livro = customtkinter.CTkToplevel()
        self.pesquisar_livro.title("Pesquisar Livros")

        # Configuração da janela
        self.pesquisar_livro.geometry(f'{850}x{500}')

        # Configuração do layout
        self.pesquisar_livro.grid_columnconfigure(1, weight=1)
        self.pesquisar_livro.grid_columnconfigure((2, 3), weight=0)
        self.pesquisar_livro.grid_rowconfigure((0, 1, 2), weight=1)

        # Campo Pesquisar Livro
        self.livro_lbl = customtkinter.CTkLabel(self.pesquisar_livro, text="Nome, Título, Autor, Descrição", font=customtkinter.CTkFont(size=12, weight="normal"))
        self.livro_lbl.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.livro_lbl_entry = customtkinter.CTkEntry(self.pesquisar_livro)
        self.livro_lbl_entry.grid(row=1, column=1, padx=20, pady=10)

        # Configuração no botão de pesquisa de livro
        self.pesquisa_btn = customtkinter.CTkButton(self.pesquisar_livro, text="Pesquisar", font=customtkinter.CTkFont(size=12, weight="normal"), command=self.executar_pesquisa)
        self.pesquisa_btn.grid(row=1, column=2, columnspan=2, padx=20, pady=10)

        # Configuração do botão de sair
        self.sair_btn = customtkinter.CTkButton(self.pesquisar_livro, text="Sair", font=customtkinter.CTkFont(size=12, weight="normal"), command=self.pesquisar_livro.destroy)
        self.sair_btn.grid(row=8, column=0, columnspan=2, padx=20, pady=10)

    def executar_pesquisa(self):
        admin_mode = True  # Você pode mudar isso de acordo com a lógica do seu programa
        resultados = pesquisar_livros(admin_mode)
        # Aqui você pode processar os resultados, talvez exibi-los em uma nova janela ou em algum outro widget
