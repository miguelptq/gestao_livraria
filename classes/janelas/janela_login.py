import customtkinter, tkinter, tkinter.messagebox
from tkinter import *
from tkinter import Tk
import sqlite3
import hashlib
import os
from classes.janelas.janela_menu import JanelaMenu
from classes.user.user import User

# Criar class para janela de registo

def clear_grid_except_error(frame, error_label):
    # Iterate over all widgets in the grid
    for widget in frame.winfo_children():
        if widget != error_label:
            error_label.destroy()


class JanelaLogin:
    def __init__(self):
        
        #Criar a janela princiapl
        self.janela_login = customtkinter.CTkToplevel()
        self.janela_login.title('Login de Utilizador') # muda o titulo

        # Criar label registo
        self.login_lbl = customtkinter.CTkLabel(self.janela_login, text = 'Login', font = customtkinter.CTkFont(size=20, weight='bold'))
        self.login_lbl.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')

        # Configuração do campo de nome do utilizador
        self.user_name_lbl = customtkinter.CTkLabel(self.janela_login, text = 'Utilizador: ', font =customtkinter.CTkFont(size=14, weight='normal'))
        self.user_name_lbl.grid(row = 1, column = 0, sticky = 'E', pady = 20)
        self.user_name_entry = customtkinter.CTkEntry(self.janela_login, font= customtkinter.CTkFont(size=14, weight='normal'))
        self.user_name_entry.grid(row = 1, column = 1, pady = 10)

        # Configuração do campo de nome do password
        self.user_password_lbl = customtkinter.CTkLabel(self.janela_login, text = 'Password: ', font = customtkinter.CTkFont(size=14, weight='normal'))
        self.user_password_lbl.grid(row = 2, column = 0, sticky = 'E', pady = 20)
        self.user_password_entry = customtkinter.CTkEntry(self.janela_login, font = customtkinter.CTkFont(size=14, weight='normal'), show = '*')
        self.user_password_entry.grid(row = 2, column = 1, pady = 10)

        # Configuração do botão de registar
        self.registar_btn = customtkinter.CTkButton(self.janela_login, text = "Login", font = customtkinter.CTkFont(size=14, weight='bold'), command = self.login_user)
        self.registar_btn.grid(row = 4, column = 0, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")

        # Configuração do botão de sair
        self.sair_btn = customtkinter.CTkButton(self.janela_login, text = "Sair", font = customtkinter.CTkFont(size=14, weight='bold'), command = self.janela_login.destroy)
        self.sair_btn.grid(row = 5, column = 0, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")
    
    def login_user(self):
        # Pegar nos dados inseridos
        username = self.user_name_entry.get()
        password_user = self.user_password_entry.get()

        user = User()
        user.set_username(username)
        user.set_password(password_user)
        login = user.login()
        self.logged_in_user = user.get_logged_in_user()
        self.mensagem_login_concluido = customtkinter.CTkLabel(self.janela_login, text = login[1], fg_color = login[2])
        self.mensagem_login_concluido.grid(row = 3, column = 0, columnspan = 2)
        if login[0] == True:
            self.open_menu_window()
            self.mensagem_login_concluido.after(3000, self.janela_login.destroy)

    def open_menu_window(self):
        janela_menu = JanelaMenu(self.logged_in_user)
    

