from tkinter import *
from tkinter import Tk
import sqlite3, customtkinter
from classes.user.user import User
from classes.book.book import Book

class JanelaInserirLivro:
    def __init__(self, user):
        self.janela_inserir = customtkinter.CTkToplevel()
        self.janela_inserir.title('Insert Books')

        self.autores = []
        self.numeroautores = 0
        self.author_labels_entries = []

        # Label Inserir Livro
        self.inserir_livro_lbl = customtkinter.CTkLabel(self.janela_inserir, text = 'Insert Books', font= customtkinter.CTkFont(family="Helvetica",size=20, weight='normal'))
        self.inserir_livro_lbl.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')

        # Configuração do campo ISBN
        self.isbn_lbl = customtkinter.CTkLabel(self.janela_inserir, text = 'ISBN:', font=customtkinter.CTkFont(family="Helvetica",size=20, weight='bold'))
        self.isbn_lbl.grid(row = 1, column = 0, sticky = 'W', pady = 20)

        self.isbn_lbl_entry = customtkinter.CTkEntry(self.janela_inserir, font=customtkinter.CTkFont(family="Arial",size=14, weight='normal'))
        self.isbn_lbl_entry.grid(row = 1, column = 1, pady = 10)

        # Configuração do campo Nome Livro
        self.nome_livro_lbl = customtkinter.CTkLabel(self.janela_inserir, text = 'Title: ',font=customtkinter.CTkFont(family="Helvetica",size=20, weight='bold'))
        self.nome_livro_lbl.grid(row = 2, column = 0, sticky = 'W', pady = 20)

        self.nome_livro_entry = customtkinter.CTkEntry(self.janela_inserir, font=customtkinter.CTkFont(family="Arial",size=14, weight='normal'))
        self.nome_livro_entry.grid(row = 2, column = 1, pady = 10)

        # Configuração do campo Descrição Livro
        self.desc_livro_lbl = customtkinter.CTkLabel(self.janela_inserir, text = 'Description: ',font=customtkinter.CTkFont(family="Helvetica",size=20, weight='bold'))
        self.desc_livro_lbl.grid(row = 3, column = 0, sticky = 'W', pady = 20)

        self.desc_livro_entry = customtkinter.CTkEntry(self.janela_inserir, font=customtkinter.CTkFont(family="Arial",size=14, weight='normal'))
        self.desc_livro_entry.grid(row = 3, column = 1, pady = 10)

        # Configuração do campo Ano Livro
        self.ano_livro_lbl = customtkinter.CTkLabel(self.janela_inserir, text = 'Year: ',font=customtkinter.CTkFont(family="Helvetica",size=20, weight='bold'))
        self.ano_livro_lbl.grid(row = 4, column = 0, sticky = 'W', pady = 20)

        self.ano_livro_entry = customtkinter.CTkEntry(self.janela_inserir, font=customtkinter.CTkFont(family="Arial",size=14, weight='normal'))
        self.ano_livro_entry.grid(row = 4, column = 1, pady = 10)

        # Criar novo par de Label e Entry para o próximo autor
        self.novo_autor_lbl = customtkinter.CTkLabel(self.janela_inserir, text='Author: ', font=customtkinter.CTkFont(family="Helvetica",size=20, weight='bold'))
        self.novo_autor_lbl.grid(row= 5, column=0, sticky='W', pady=20)

        self.novo_autor_entry = customtkinter.CTkEntry(self.janela_inserir, font=customtkinter.CTkFont(family="Arial",size=14, weight='normal'))
        self.novo_autor_entry.grid(row=5, column=1, pady=10, sticky='EW')  

        # Configuração do botão de Inserir
        self.confimation = customtkinter.CTkLabel(self.janela_inserir, text="", font=customtkinter.CTkFont(size=20, weight='bold'))
        self.confimation.grid(row=6, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")

        self.inserir_btn = customtkinter.CTkButton(self.janela_inserir, text = "Insert", font=customtkinter.CTkFont(family="Helvetica",size=12, weight='bold'), command = self.botao_inserir)
        self.inserir_btn.grid(row = 7, column = 0, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")

        # Configuração do botão de sair
        self.sair_btn = customtkinter.CTkButton(self.janela_inserir, text = "Quit",font=customtkinter.CTkFont(family="Helvetica",size=12, weight='bold'), command = self.janela_inserir.destroy)
        self.sair_btn.grid(row = 8, column = 0, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")

        self.proxima_linha = 6

        self.add_autor_btn = customtkinter.CTkButton(self.janela_inserir, text="+",font=customtkinter.CTkFont(size=14, weight='bold'), command = self.add_autor)
        self.add_autor_btn.grid(row=5, column=2, padx=(10, 20), pady=10)



    def guardar_livro(self, autores):
        isbn = self.isbn_lbl_entry.get()
        title = self.nome_livro_entry.get()
        desc = self.desc_livro_entry.get()
        year = self.ano_livro_entry.get()
        book = Book()
        book.set_isbn(isbn)
        book.set_title(title)
        book.set_desc(desc)
        book.set_year(year)
        creation = book.create(autores)
        if hasattr(self,'book_creation_msg'):
            self.book_creation_msg.destroy()
        self.book_creation_msg = Label(self.janela_inserir, text = creation[1], fg = creation[2])
        self.book_creation_msg.grid(row = self.proxima_linha, column = 0, columnspan = 2)
        return creation[0]

    def add_autor(self):
        self.numeroautores += 1

        # Obter o nome do autor
        novo_autor = self.novo_autor_entry.get()

        # Adicionar o novo autor à lista de autores
        if novo_autor.strip(): 
            self.autores.append(novo_autor)

        # Criar novo par de Label e Entry para o próximo autor
        new_autor_label = customtkinter.CTkLabel(self.janela_inserir, text='Author:',font=customtkinter.CTkFont(family="Helvetica",size=20, weight='bold'))
        new_autor_label.grid(row=self.proxima_linha, column=0, sticky='W', pady=20)
        self.author_labels_entries.append(new_autor_label)

        new_autor_entry = Entry(self.janela_inserir, font=customtkinter.CTkFont(family="Arial",size=14, weight='normal'))
        new_autor_entry.grid(row=self.proxima_linha, column=1, pady=10, sticky='EW')
        self.author_labels_entries.append(new_autor_entry)

        # Atualizar a próxima linha para o próximo autor
        self.proxima_linha += 1

        self.inserir_btn.grid(row=self.proxima_linha + 1, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")
        self.sair_btn.grid(row=self.proxima_linha + 2, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")
        self.confimation.grid(row=self.proxima_linha, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")

    def botao_inserir(self):
        # Get authors from all entry widgets, including the first one
        autores = [self.novo_autor_entry.get()] + [entry.get() for entry in self.author_labels_entries[1::2] if entry.get()]
        
        creation = self.guardar_livro(autores)
        if creation:
            self.clear_entries()
        

    def clear_entries(self):
        # Clear the text in all Entry widgets
        self.isbn_lbl_entry.delete(0, END)
        self.nome_livro_entry.delete(0, END)
        self.desc_livro_entry.delete(0, END)
        self.ano_livro_entry.delete(0, END)
        self.novo_autor_entry.delete(0, END)

        # Delete the saved Entry and Label widgets for authors
        for widget in self.author_labels_entries:
            widget.destroy()

        # Clear the list of saved Entry and Label widgets for authors
        self.author_labels_entries.clear()
        self.autores = []