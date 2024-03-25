import sqlite3
import customtkinter, tkinter
from tkinter import IntVar, ttk
from functions.functions import *

def pesquisar_livros(admin=False):
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    if admin:
        cursor.execute("SELECT * FROM livro")
    else:
        cursor.execute("SELECT * FROM livro")
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

        self.pesquisar_livro = customtkinter.CTkToplevel()
        self.pesquisar_livro.title("Pesquisar Livros")

        # Configuração da janela
        self.pesquisar_livro.geometry(f'{850}x{500}')

        # Configuração do layout
        self.pesquisar_livro.grid_columnconfigure(1, weight=1)
        self.pesquisar_livro.grid_columnconfigure((2, 3), weight=0)
        self.pesquisar_livro.grid_rowconfigure((0, 1, 2), weight=1)

        # Campo Pesquisar Livro
        self.livro_lbl = customtkinter.CTkLabel(self.pesquisar_livro, text="Pesquise o Titulo do livro:", font=customtkinter.CTkFont(size=12, weight="normal"))
        self.livro_lbl.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.livro_lbl_entry = customtkinter.CTkEntry(self.pesquisar_livro)
        self.livro_lbl_entry.grid(row=1, column=1, padx=20, pady=10)

         # Checkbox de empréstimo
        self.emprestimo_var = IntVar()
        self.emprestimo_cb = customtkinter.CTkCheckBox(self.pesquisar_livro, text="Emprestados", variable=self.emprestimo_var)
        self.emprestimo_cb.grid(row=1, column=2, padx=20, pady=10)

         # Checkbox de devolução
        self.devolvido_var = IntVar()  
        self.devolvido_cb = customtkinter.CTkCheckBox(self.pesquisar_livro, text="Devolvidos", variable=self.devolvido_var)
        self.devolvido_cb.grid(row=1, column=3, padx=20, pady=10)


        # Configuração do botão de pesquisa de livro
        self.pesquisa_btn = customtkinter.CTkButton(self.pesquisar_livro, text="Pesquisar", font=customtkinter.CTkFont(size=12, weight="normal"), command=self.executar_pesquisa)
        self.pesquisa_btn.grid(row=2, column=4, columnspan=2, padx=20, pady=10)

        # Configuração do botão de sair
        self.sair_btn = customtkinter.CTkButton(self.pesquisar_livro, text="Sair", font=customtkinter.CTkFont(size=12, weight="normal"), command=self.pesquisar_livro.destroy)
        self.sair_btn.grid(row=3, column=5, columnspan=1, padx=20, pady=10, sticky="nsew")

        # Configuração do CTkTreeview para exibir os resultados
        self.tree = ttk.Treeview(self.pesquisar_livro, columns=("ISBN", "Título", "Descrição", "Autores"))
        self.tree.grid(row=2, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        # Configurando as colunas do CTkTreeview
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Autores", text="Autores")

        # Configurando o redimensionamento das colunas
        self.tree.column("#1", stretch=True)
        self.tree.column("#2", stretch=True)
        self.tree.column("#3", stretch=True)

         # Estilizando a árvore
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Escolha do tema
        self.style.configure("Treeview", background="#f0f0f0", foreground="black", fieldbackground="#d3d3d3", font=("Arial", 10))
        self.style.map("Treeview", background=[('selected', '#347083')])  # Cor de fundo ao selecionar uma linha

    def executar_pesquisa(self):
        # Limpar resultados anteriores
        for record in self.tree.get_children():
            self.tree.delete(record)

        admin_mode = True 
        resultados = self.search(self.livro_lbl_entry.get())

    def search(self, search_query="", borrowed=[]):
        conn = sqlite3.connect('livraria.db')

        cursor = conn.cursor()

        query = f"""
            SELECT l.isbn_livro, l.nome_livro, l.desc_livro,l.borrowed, a.nome_autor
            FROM livro l
            JOIN autor_livro a ON l.isbn_livro = a.isbn_livro
        """
        if search_query != "":
            query += f" WHERE l.nome_livro LIKE '%{search_query}%'"
        if len(borrowed) == 1:
            query += f" AND l.borrowed LIKE '%{borrowed[0]}%'"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        filtered_data = {}
        for isbn,title,desc, borrowed, author in results:
            if isbn not in filtered_data:
                filtered_data[isbn] = {'isbn':isbn,'title': title,'desc':desc, 'authors': []}
            filtered_data[isbn]['authors'].append(author)
        for isbn, data in filtered_data.items():
            data['authors'] = ', '.join(data['authors'])
            self.tree.insert('', 'end', values=(data['isbn'], data['title'], data['desc'], data['authors']))
        pass
