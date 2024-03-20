import sqlite3
import customtkinter

def requisitar_livro(usuario, titulo):
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emprestimos (usuario, livro) VALUES (?, ?)", (usuario, titulo))
    conn.commit()
    conn.close()

def pesquisar_livros(titulo, admin=False):
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    if admin:
        cursor.execute("SELECT * FROM livro WHERE nome_livro LIKE ?", ('%' + titulo + '%',))
    else:
        # Implemente a lógica de pesquisa para usuários regulares
        pass
    resultados = cursor.fetchall()
    conn.close()
    return resultados

class JanelaRequisitarLivro:
    def __init__(self, usuario):
        self.requisitar_livro = customtkinter.CTkToplevel()
        self.requisitar_livro.title("Requisitar Livro")

        # Configuração da janela
        self.requisitar_livro.geometry(f'{850}x{500}')

        # Configuração do layout
        self.requisitar_livro.grid_columnconfigure(1, weight=1)
        self.requisitar_livro.grid_columnconfigure((2, 3), weight=0)
        self.requisitar_livro.grid_rowconfigure((0, 1, 2), weight=1)

        # Campo Título do Livro
        self.titulo_lbl = customtkinter.CTkLabel(self.requisitar_livro, text="Título do livro:", font=customtkinter.CTkFont(size=12, weight="normal"))
        self.titulo_lbl.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.titulo_entry = customtkinter.CTkEntry(self.requisitar_livro)
        self.titulo_entry.grid(row=1, column=1, padx=20, pady=10)

        # Configuração no botão de requisitar livro
        self.requisitar_btn = customtkinter.CTkButton(self.requisitar_livro, text="Requisitar Livro", font=customtkinter.CTkFont(size=12, weight="normal"), command=self.executar_requisicao)
        self.requisitar_btn.grid(row=7, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")

        # Configuração do botão de sair
        self.sair_btn = customtkinter.CTkButton(self.requisitar_livro, text="Sair", font=customtkinter.CTkFont(size=12, weight="normal"), command=self.requisitar_livro.destroy)
        self.sair_btn.grid(row=8, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")

        self.usuario = usuario

    def executar_requisicao(self):
        titulo = self.titulo_entry.get()
        requisitar_livro(self.usuario, titulo)
        print("Livro requisitado com sucesso.")