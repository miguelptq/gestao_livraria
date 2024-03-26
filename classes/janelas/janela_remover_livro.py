import sqlite3
import customtkinter, tkinter
from tkinter import ttk


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
        self.livro_lbl = customtkinter.CTkLabel(self.remover_livro, text="Insira alguma informação do livro (Titulo, ISBN, Autor, Descrição):", font=customtkinter.CTkFont(size=12, weight="normal"))
        self.livro_lbl.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.livro_lbl_entry = customtkinter.CTkEntry(self.remover_livro)
        self.livro_lbl_entry.grid(row=1, column=1, padx=20, pady=10)


         # Configuração do botão de pesquisa de livro
        self.pesquisa_btn = customtkinter.CTkButton(self.remover_livro, text="Pesquisar", font=customtkinter.CTkFont(size=12, weight="normal"), command=self.executar_pesquisa)
        self.pesquisa_btn.grid(row=2, column=4, columnspan=2, padx=20, pady=10)


        # Configuração no botão de remover livro
        self.remover_btn = customtkinter.CTkButton(self.remover_livro, text="Remover Livro", font=customtkinter.CTkFont(size=12, weight="normal"), command=self.remover_livro_escolhido)
        self.remover_btn.grid(row=7, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")

        # Configuração do botão de sair
        self.sair_btn = customtkinter.CTkButton(self.remover_livro, text="Sair", font=customtkinter.CTkFont(size=12, weight="normal"), command=self.remover_livro.destroy)
        self.sair_btn.grid(row=8, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")
        
        # Configuração do CTkTreeview para exibir os resultados
        self.tree = ttk.Treeview(self.remover_livro, columns=("ISBN", "Título", "Descrição", "Autores"))
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
        resultados = self.search_remove(self.livro_lbl_entry.get())

    def search_remove(self, search_query="", borrowed=[]):
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
        
    def remover_livro_escolhido(self):
        livro_escolhido = self.tree.selection()

        if livro_escolhido:
            #Informações do livro selecionado
            values = self.tree.item(livro_escolhido)['values']
            titulo_livro = values[1]

            try:
                conn = sqlite3.connect('livraria.db')
                cursor = conn.cursor()

                # Busca o ISBN do livro selecionado
                cursor.execute("SELECT isbn_livro FROM livro WHERE nome_livro=?", (titulo_livro,))
                isbn_livro = cursor.fetchone()[0]

                # Remover o livro da BD
                cursor.execute("DELETE FROM livro WHERE nome_livro=?", (titulo_livro,))

                # Remover os autores associados ao ISBN do livro da tabela 'autor_livro'
                cursor.execute("DELETE FROM autor_livro WHERE isbn_livro=?", (isbn_livro,))

                # Confirmar as alterações no banco de dados
                conn.commit()

                # Fechar a conexão
                conn.close()

                # Remover o item da treeview
                self.tree.delete(livro_escolhido)

                tkinter.messagebox.showinfo("Sucesso", f"O livro '{titulo_livro}' foi removido com sucesso.")
            except sqlite3.Error as e:
                tkinter.messagebox.showerror("Erro", f"Ocorreu um erro ao remover o livro: {e}")
        else:
            # Se nada estiver selecionado, mensagem de erro
            tkinter.messagebox.showerror("Erro", "Nenhum livro foi selecionado")

