from tkinter import *
import sqlite3
import customtkinter

class EditarDadosLivro:
    def __init__(self, book_data, janela_anterior):
        self.book_data = book_data
        self.janela_anterior = janela_anterior
        
        self.edit_window = customtkinter.CTkToplevel()
        self.edit_window.title('Editar Dados do Livro')
        self.edit_window.iconbitmap('')
        self.edit_window.configure(bg="#f0f0f0")
        
        self.setup_ui()

    def setup_ui(self):
        labels = ['ISBN', 'Título', 'Descrição', 'Ano']

        for i, label_text in enumerate(labels):
            label = customtkinter.CTkLabel(self.edit_window, text=label_text + ":", font=customtkinter.CTkFont(size=14, weight='bold'))
            label.grid(row=i, column=0, padx=10, pady=10, sticky='W')

            entry = customtkinter.CTkEntry(self.edit_window, font=customtkinter.CTkFont(size=14))
            entry.grid(row=i, column=1, padx=10, pady=10, sticky='W')

            # Insere os dados do livro escolhido
            entry.insert(0, self.book_data[i])

            # ISBN so para leitura
            if label_text == 'ISBN':
                entry.configure(state='readonly')

            setattr(self, f"{label_text.lower()}_entry", entry)

        # Listbox para editar autores
        author_label = customtkinter.CTkLabel(self.edit_window, text="Autores:", font=customtkinter.CTkFont(size=14, weight='bold'))
        author_label.grid(row=len(labels), column=0, padx=10, pady=10, sticky='W')

        self.author_listbox = Listbox(self.edit_window, font=customtkinter.CTkFont(size=14))
        self.author_listbox.grid(row=len(labels) + 1, column=0, columnspan=2, padx=10, pady=10, sticky='W')

        # Apresentar autores
        self.populate_author_list()

        # Nome do novo autor
        self.new_author_entry = customtkinter.CTkEntry(self.edit_window, font=customtkinter.CTkFont(size=14))
        self.new_author_entry.grid(row=len(labels) + 2, column=0, padx=10, pady=10, sticky='W')

        # Botao para adicionar autores
        add_author_button = customtkinter.CTkButton(self.edit_window, text="Add Author", font=customtkinter.CTkFont(size=14, weight='bold'), command=self.add_author)
        add_author_button.grid(row=len(labels) + 2, column=1, padx=10, pady=10)

        # Botao de remover autores
        remove_author_button = customtkinter.CTkButton(self.edit_window, text="Remove Author", font=customtkinter.CTkFont(size=14, weight='bold'), command=self.remove_author)
        remove_author_button.grid(row=len(labels) + 3, column=0, columnspan=2, padx=10, pady=10)

        # Alterar autor na listbox
        self.author_listbox.bind("<Double-1>", self.edit_author)

        # Botão de Save
        save_button = customtkinter.CTkButton(self.edit_window, text="Save", font=customtkinter.CTkFont(size=14, weight='bold'), command=self.save_changes)
        save_button.grid(row=len(labels) + 4, column=0, columnspan=2, pady=10)

    def add_author(self):
        new_author = self.new_author_entry.get()
        if new_author:
            self.author_listbox.insert(END, new_author)

    def remove_author(self):
        selected_index = self.author_listbox.curselection()
        if selected_index:
            self.author_listbox.delete(selected_index)

    def edit_author(self, event):
        index = self.author_listbox.nearest(event.y)
        self.author_listbox.activate(index)
        self.author_listbox.focus_set()
        self.author_listbox.edit_set(index)

    def populate_author_list(self):
        # Autores do livro
        conn = sqlite3.connect('livraria.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome_autor FROM autor_livro WHERE isbn_livro = ?", (self.book_data[0],))
        authors = cursor.fetchall()
        conn.close()
        
        for author in authors:
            self.author_listbox.insert(END, author[0])

    def update_book_details(self):
        self.populate_book_list()

    def save_changes(self):
        # Guardar
        updated_data = [getattr(self, f"{label.lower()}_entry").get() for label in ['ISBN', 'Título', 'Descrição', 'Ano']]

        conn = sqlite3.connect('livraria.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE livro SET isbn_livro=?, nome_livro=?, desc_livro=?, ano_livro=? WHERE isbn_livro=?", (*updated_data, self.book_data[0]))

        cursor.execute("DELETE FROM autor_livro WHERE isbn_livro=?", (self.book_data[0],))
        for index in range(self.author_listbox.size()):
            author = self.author_listbox.get(index)
            cursor.execute("INSERT INTO autor_livro (isbn_livro, nome_autor) VALUES (?, ?)", (self.book_data[0], author))

        conn.commit()
        conn.close()

        # Atualizar a tabela da janela anterior
        self.janela_anterior.refresh_book_list()
        self.edit_window.destroy()