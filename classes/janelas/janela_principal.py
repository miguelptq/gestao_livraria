#importações
from tkinter import *
from tkinter import Tk
from classes.janelas.janela_registo import JanelaRegisto
from classes.janelas.janela_login import JanelaLogin
import customtkinter

#class da janela principal
class JanelaPrincipal:
    def __init__(self):
        
        #Criar a janela princiapl
        self.janela_principal = customtkinter.CTk()
        self.janela_principal.title('Sistema de Gestão de Livros') # muda o titulo

        # Configuração do Texto de Boas Vindas
        self.boas_vindas_lbl = customtkinter.CTkLabel(self.janela_principal, text = 'Sistema de Gestão de Livros',font =customtkinter.CTkFont(size=14, weight='bold'))
        self.boas_vindas_lbl.grid(row = 0, column = 1, columnspan = 1, pady = 20)

        # Configuração do botão de registo
        self.registar_btn = customtkinter.CTkButton(self.janela_principal, text = "Registar", font =customtkinter.CTkFont(size=14, weight='normal'), command = self.abrir_janela_registo)
        self.registar_btn.grid(row = 1, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")

        # Configuração do botão de login
        self.login_btn = customtkinter.CTkButton(self.janela_principal, text = "Login", font =customtkinter.CTkFont(size=14, weight='normal'), command = self.abrir_janela_login)
        self.login_btn.grid(row = 2, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")

        # Configuração do botão de sair
        self.sair_btn = customtkinter.CTkButton(self.janela_principal, text = "Sair", font =customtkinter.CTkFont(size=14, weight='normal'), command = self.janela_principal.destroy)
        self.sair_btn.grid(row = 3, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")
    
    def abrir_janela_registo(self):
        JanelaRegisto()

    def abrir_janela_login(self):
        JanelaLogin()
