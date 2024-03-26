from tkinter import *
from tkinter import ttk
import sqlite3
import customtkinter
import tkinter.messagebox

class JanelaDevolverLivro:
    def __init__(self, user):
        self.logged_user = user
        conn = sqlite3.connect('livraria.db')
        cursor = conn.cursor()
        cursor.execute("Select role_name FROM roles where id = ?",(user['role'],))
        self.role_name = cursor.fetchone()[0]
        
        self.janela_borrow_livro = customtkinter.CTkToplevel()
        self.janela_borrow_livro.title('Return Book')
        self.janela_borrow_livro.iconbitmap('')
        self.janela_borrow_livro.configure(bg="#f0f0f0")
        
        self.book_list_lbl = customtkinter.CTkLabel(self.janela_borrow_livro, text='', font=customtkinter.CTkFont(size=20, weight='bold'))
        self.book_list_lbl.grid(row=0, column=0, columnspan=2, pady=20, sticky='NSEW')
        
        # Filtra os livros
        self.book_title_lbl = customtkinter.CTkLabel(self.janela_borrow_livro, text='Title:', font=customtkinter.CTkFont(size=14, weight='bold'))
        self.book_title_lbl.grid(row=1, column=0, pady=10, sticky='W')
        
        self.book_title_entry = customtkinter.CTkEntry(self.janela_borrow_livro, font=customtkinter.CTkFont(size=14, weight='bold'))
        self.book_title_entry.grid(row=1, column=1, pady=10, sticky='W')
        
        self.filter_btn = customtkinter.CTkButton(self.janela_borrow_livro, text="Filter", font=customtkinter.CTkFont(family="Helvitica",size=12, weight='normal'), command=self.filter_list)
        self.filter_btn.grid(row=1, column=2, pady=10, sticky='W')


        # Mostra os livros
        self.tree = ttk.Treeview(self.janela_borrow_livro, columns=("ISBN", "Title", "Description", "Year", "Authors"), show="headings")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Authors", text="Authors")
        self.tree.grid(row=2, column=0, columnspan=3, sticky='nsew')
        
        self.janela_borrow_livro.grid_rowconfigure(0, weight=1)
        self.janela_borrow_livro.grid_columnconfigure(0, weight=1)

        self.return_btn = customtkinter.CTkButton(self.janela_borrow_livro, text="Return", font=customtkinter.CTkFont(family="Helvitica",size=12, weight='normal'), command=self.return_book)
        self.return_btn.grid(row=3, column=1, pady=10, sticky='W')
        self.return_btn = customtkinter.CTkButton(self.janela_borrow_livro, text="Quit", font=customtkinter.CTkFont(family="Helvitica",size=12, weight='normal'), command=self.janela_borrow_livro.destroy)
        self.return_btn.grid(row=3, column=2, pady=10, sticky='W')
        
        self.populate_book_list()

    def filter_list(self):
        title_search = self.book_title_entry.get()
        self.populate_book_list(title_search)

    def populate_book_list(self, title_search=None):
        conn = sqlite3.connect('livraria.db')
        cursor = conn.cursor()
        if title_search:
            query = """
                SELECT livro.*, GROUP_CONCAT(autor_livro.nome_autor, ', ') AS autores FROM livro
                LEFT JOIN autor_livro ON livro.isbn_livro = autor_livro.isbn_livro
                WHERE livro.nome_livro LIKE ? AND livro.borrowed is TRUE GROUP BY livro.isbn_livro
            """
            if self.role_name in ('SuperAdmin', 'Employer'):
                cursor.execute(query, (f'%{title_search}%',))
            else:
                cursor.execute(query, (self.logged_user['id'], f'%{title_search}%'))
        else:
            if self.role_name in ('SuperAdmin', 'Employer'):
                query = """
                    SELECT livro.*, GROUP_CONCAT(autor_livro.nome_autor, ', ') AS autores FROM livro
                    LEFT JOIN autor_livro ON livro.isbn_livro = autor_livro.isbn_livro
                    WHERE livro.borrowed is TRUE
                    GROUP BY livro.isbn_livro
                """
                cursor.execute(query)
            else:
                cursor.execute("SELECT livro.*, GROUP_CONCAT(autor_livro.nome_autor, ', ') AS autores FROM livro LEFT JOIN autor_livro ON livro.isbn_livro = autor_livro.isbn_livro WHERE livro.user_id = ? AND livro.borrowed is TRUE GROUP BY livro.isbn_livro", (self.logged_user['id'],))
        self.books = cursor.fetchall()
        conn.close()

        # Limpar o Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Preencher o Treeview com os livros
        for book in self.books:
            item = self.tree.insert('', 'end', values=book[:4])  # Excluding the 'autores' column
            self.tree.set(item, "Authors", book[6] if book[6] else '')  # Use "Autores" instead of "autores"

    def return_book(self):
        item = self.tree.selection()[0] 
        book_data = self.tree.item(item, "values")
        conn = sqlite3.connect('livraria.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE livro SET borrowed=FALSE, user_id=NULL WHERE isbn_livro=?", (book_data[0],))
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo("Book Returned",  f"The book {book_data[1]} has been returned!")
        self.populate_book_list()