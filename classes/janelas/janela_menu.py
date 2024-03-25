from tkinter import *
from tkinter import Tk
import sqlite3, customtkinter
from classes.janelas.janela_inserir_livro import JanelaInserirLivro
from classes.janelas.janela_devolver_livro import JanelaDevolverLivro
from classes.janelas.janela_editar_livro import JanelaEditarLivro
from classes.janelas.janela_list_users import JanelaListUsers
from classes.janelas.janela_pesquisar_livro import JanelaPesquisarLivro
from classes.janelas.janela_remover_livro import JanelaRemoverLivro
from classes.janelas.janela_registo import JanelaRegisto
from classes.janelas.janela_requisitar_livro import JanelaRequisitarLivro
from functions.functions import *

# Criar class para janela de registo


class JanelaMenu:
    def __init__(self, user):
        self.logged_in_user = user
        conn = sqlite3.connect('livraria.db')

        cursor = conn.cursor()
        permissions = list_permissions(self.logged_in_user)
        cursor.execute("Select role_name FROM roles where id = ?",(self.logged_in_user['role'],))
        role_name= cursor.fetchone()[0]
        conn.close()
        button_count = 1
        self.janela_menu = customtkinter.CTkToplevel()
        self.janela_menu.title(f'Menu do {role_name}') # muda o titulo

        
        # Criar label registo
        self.menu_lbl =  customtkinter.CTkLabel(self.janela_menu, text = f'Menu do {role_name}', font =customtkinter.CTkFont(size=20, weight='bold'))
        self.menu_lbl.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
        for permission in permissions:
            button_var = f"{permission}_{button_count}"
            self.button_var =  customtkinter.CTkButton(self.janela_menu, text=permission, font=customtkinter.CTkFont(size=14, weight='bold'), command=lambda option=permission: self.menu_redirect(option))
            self.button_var.grid(row = button_count, column = 0, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW") 
            button_count += 1
        self.sair_btn =  customtkinter.CTkButton(self.janela_menu, text = "Sair", font= customtkinter.CTkFont(size=14, weight='bold'), command = self.janela_menu.destroy)
        self.sair_btn.grid(row = button_count + 1, column = 0, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")


    def menu_redirect(self, option):
        menu_list = {
            'Search Books': JanelaPesquisarLivro,
            'Request Books': JanelaRequisitarLivro,
            'Return Books' : JanelaDevolverLivro,
            'Insert Books' : JanelaInserirLivro,
            'Remove Books': JanelaRemoverLivro,
            'Update Books': JanelaEditarLivro,
            'Insert New Users': JanelaRegisto,
            'List Users': JanelaListUsers
        }
        menu = menu_list[option](self.logged_in_user)

