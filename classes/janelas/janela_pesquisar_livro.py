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
        self.pesquisar_livro.title("Search Books")

        # Configuração da janela
        self.pesquisar_livro.geometry(f'{850}x{500}')

        # Configuração do layout
        self.pesquisar_livro.grid_columnconfigure(1, weight=1)
        self.pesquisar_livro.grid_columnconfigure((2, 3), weight=0)
        self.pesquisar_livro.grid_rowconfigure((0, 1, 2), weight=1)

        # Campo Pesquisar Livro
        self.livro_lbl = customtkinter.CTkLabel(self.pesquisar_livro, text="Title: ", font=customtkinter.CTkFont(family="Helvetica", size=12, weight="normal"))
        self.livro_lbl.grid(row=1, column=0, padx=20, pady=10, sticky="E")
        self.livro_lbl_entry = customtkinter.CTkEntry(self.pesquisar_livro)
        self.livro_lbl_entry.grid(row=1, column=1, padx=20, pady=5, sticky="W")

         # Checkbox de empréstimo
        self.emprestimo_var = IntVar()
        self.emprestimo_cb = customtkinter.CTkCheckBox(self.pesquisar_livro, text="Borrowed", variable=self.emprestimo_var)
        self.emprestimo_cb.grid(row=1, column=2, columnspan = 2, padx=20, pady = 10)

         # Checkbox de devolução
        self.devolvido_var = IntVar()  
        self.devolvido_cb = customtkinter.CTkCheckBox(self.pesquisar_livro, text="Returned", variable=self.devolvido_var)
        self.devolvido_cb.grid(row=2, column=2,  columnspan = 2, padx=20, pady = 1)


        # Configuração do botão de pesquisa de livro
        self.pesquisa_btn = customtkinter.CTkButton(self.pesquisar_livro, text="Search", font=customtkinter.CTkFont(family="Helvetica",size=12, weight="bold"), command=self.executar_pesquisa)
        self.pesquisa_btn.grid(row=7, column=1, columnspan = 2, padx=20, pady = 10)

        # Configuração do botão de sair
        self.sair_btn = customtkinter.CTkButton(self.pesquisar_livro, text="Quit", font=customtkinter.CTkFont(family="Helvetica",size=12, weight="bold"), command=self.pesquisar_livro.destroy)
        self.sair_btn.grid(row=8, column=1,  columnspan = 2, padx=20, pady = 10)

        # Configuração do CTkTreeview para exibir os resultados
        self.tree = ttk.Treeview(self.pesquisar_livro, columns=("ISBN", "Title", "Description", "Year", "Authors"), show="headings")
        self.tree.grid(row=5, column=0,  columnspan = 4, padx=20, pady = 10, sticky="nsew")

        # Configurando as colunas do CTkTreeview
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Authors", text="Authors")

        # Configurando o redimensionamento das colunas
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("#1", stretch=True)
        self.tree.column("#2", stretch=True)
        self.tree.column("#3", stretch=True)
        self.tree.column("#4", stretch=True)

        # Estilizando a árvore
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Escolha do tema
        self.style.configure("Treeview", background="#f0f0f0", foreground="black", fieldbackground="#d3d3d3", font=("Arial", 10))
        self.style.map("Treeview", background=[('selected', '#347083')])  # Cor de fundo ao selecionar uma linha
        
        list_books = self.search(self.livro_lbl_entry.get())

    def executar_pesquisa(self):
        # Limpar resultados anteriores
        for record in self.tree.get_children():
            self.tree.delete(record)

        admin_mode = True 
        resultados = self.search(self.livro_lbl_entry.get())

    def search(self, search_query=""):
        self.borrowed = []
        if self.emprestimo_var.get() == 1:
            self.borrowed.append(1)
        if self.devolvido_var.get() == 1:
            self.borrowed.append(0)
        conn = sqlite3.connect('livraria.db')

        cursor = conn.cursor()

        query = f"""
            SELECT l.isbn_livro, l.nome_livro, l.desc_livro,l.borrowed, a.nome_autor
            FROM livro l
            JOIN autor_livro a ON l.isbn_livro = a.isbn_livro
        """
        if search_query != "" or len(self.borrowed) == 1:
            query += " WHERE"
        if search_query != "":
            query += f" l.nome_livro LIKE '%{search_query}%'"
        if search_query != "" and len(self.borrowed) == 1:
            query += " AND"
        if len(self.borrowed) == 1:
            query += f" l.borrowed = '{self.borrowed[0]}'"
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
