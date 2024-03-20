import sqlite3
import customtkinter


def remover_livro(titulo):
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livro WHERE nome_livro=?", (titulo,))
    conn.commit()
    conn.close()


def pesquisar_livros(admin=False):
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    if admin:
        cursor.execute("SELECT * FROM livro")
    else:
        cursor.execute("SELECT * FROM livro")
        pass
    return cursor.fetchall()


class JanelaRemoverLivro:
    def __init__(self, user):
        self.remover_livro = customtkinter.CTkToplevel()
        self.remover_livro.title("Remover Livro")

        # Configuração da janela
        self.remover_livro.geometry(f'{850}x{500}')

        # Configuração do layout
        self.remover_livro.grid_columnconfigure(1, weight=1)
        self.remover_livro.grid_columnconfigure((2, 3), weight=0)
        self.remover_livro.grid_rowconfigure((0, 1, 2), weight=1)

        # Campo Remover Livro
        self.livro_lbl = customtkinter.CTkLabel(self.remover_livro, text="Nome do livro a ser removido:", font=customtkinter.CTkFont(size=12, weight="normal"))
        self.livro_lbl.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.livro_lbl_entry = customtkinter.CTkEntry(self.remover_livro)
        self.livro_lbl_entry.grid(row=1, column=1, padx=20, pady=10)

        # Configuração no botão de remover livro
        self.remover_btn = customtkinter.CTkButton(self.remover_livro, text="Remover Livro", font=customtkinter.CTkFont(size=12, weight="normal"), command=self.executar_remocao)
        self.remover_btn.grid(row=7, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")

        # Configuração do botão de sair
        self.sair_btn = customtkinter.CTkButton(self.remover_livro, text="Sair", font=customtkinter.CTkFont(size=12, weight="normal"), command=self.remover_livro.destroy)
        self.sair_btn.grid(row=8, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")

    def executar_remocao(self):
        titulo = self.livro_lbl_entry.get()
        remover_livro(titulo)
        print("Livro removido com sucesso.")
