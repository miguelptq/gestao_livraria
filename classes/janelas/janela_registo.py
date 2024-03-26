# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import Tk
from tkinter import ttk
import tkinter.messagebox
import sqlite3, customtkinter
import hashlib, re
import os
from classes.user.user import User
from functions.functions import *
# Criar class para janela de registo

def clear_grid_except_error(frame, error_label):
    # Iterate over all widgets in the grid
    for widget in frame.winfo_children():
        if widget != error_label:
            error_label.destroy()


def email_verificado(email):
    email_regex =  r'^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

    if re.match(email_regex, email):
        return True
    else:
        return False




class JanelaRegisto:
    def __init__(self, user = None):
        self.registering_role_name = "Client"
        #Criar a janela princiapl
        if user:
            conn = sqlite3.connect('livraria.db')
            cursor = conn.cursor()
            cursor.execute("Select role_name FROM roles where id = ?",(user['role'],))
            self.registering_role_name = cursor.fetchone()[0]
            conn.close()
            self.permission_list = list_permissions(user, self.registering_role_name)
        self.janela_registo =  customtkinter.CTkToplevel()
        self.janela_registo.title('Register a New User') # muda o titulo
        

        # Criar label registo
        self.registo_lbl =  customtkinter.CTkLabel(self.janela_registo, text = 'Register', font =customtkinter.CTkFont(size=20, weight='bold'))
        self.registo_lbl.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')

        # Configuração do campo de nome do utilizador
        self.user_name_lbl =  customtkinter.CTkLabel(self.janela_registo, text = 'USername: ',font =customtkinter.CTkFont(size=14, weight='bold'))
        self.user_name_lbl.grid(row = 1, column = 0, sticky = 'E', pady = 20)
        self.user_name_entry =  customtkinter.CTkEntry(self.janela_registo, font =customtkinter.CTkFont(size=14, weight='bold'))
        self.user_name_entry.grid(row = 1, column = 1, pady = 10)

        # Configuração do campo de email do utilizador
        self.user_email_lbl =  customtkinter.CTkLabel(self.janela_registo, text = 'Email: ',font =customtkinter.CTkFont(size=14, weight='normal'))
        self.user_email_lbl.grid(row = 2, column = 0, sticky = 'E', pady = 20)
        self.user_email_entry =  customtkinter.CTkEntry(self.janela_registo, font =customtkinter.CTkFont(size=14, weight='bold'))
        self.user_email_entry.grid(row = 2, column = 1, pady = 10)

        #Configuração do label de validação de email
        self._user_email_valido_lbl = customtkinter.CTkLabel(self.janela_registo, text="", font =customtkinter.CTkFont(size=14, weight='normal'))
        self._user_email_valido_lbl.grid(row=3, column=2, padx=10)

        # Configuração do campo de nome do password
        self.user_password_lbl =  customtkinter.CTkLabel(self.janela_registo, text = 'Password: ', font =customtkinter.CTkFont(size=14, weight='normal'))
        self.user_password_lbl.grid(row = 3, column = 0, sticky = 'E', pady = 20)
        self.user_password_entry =  customtkinter.CTkEntry(self.janela_registo,font =customtkinter.CTkFont(size=14, weight='bold'), show = '*')
        self.user_password_entry.grid(row = 3, column = 1, pady = 10)

        if self.registering_role_name != "Client":
            choices = ["Client"]
            if self.registering_role_name == "SuperAdmin":
                choices.append("Employer")
            self.user_role_lbl =  customtkinter.CTkLabel(self.janela_registo, text="Pick a Role: ", font =customtkinter.CTkFont(size=14, weight='normal'))
            self.user_role_lbl.grid(row = 4, column = 0, sticky = 'E', pady = 20)
            self.role_name =  customtkinter.CTkComboBox(self.janela_registo, values=choices,state="readonly")
            self.role_name.set("Client")
            self.role_name.grid(row = 4, column = 1, pady = 20)

        if hasattr(self, 'permission_list'):
            self.permission_checkboxes = []
            for index, permission in enumerate(self.permission_list):
                var = IntVar()
                checkbox =  customtkinter.CTkCheckBox(self.janela_registo, text=permission, variable=var, font =customtkinter.CTkFont(size=14, weight='normal'))
                checkbox.grid(row=index + 6, column=0, columnspan=2, pady=5, sticky='W')
                self.permission_checkboxes.append((permission, var))
        row = 7
        if hasattr(self, 'permission_list'):
            row = 7 + len(self.permission_list)
        # Configuração do botão de registar
        self.registar_btn =  customtkinter.CTkButton(self.janela_registo, text = "Register", font =customtkinter.CTkFont(size=14, weight='normal'), command = self.registar_utilizador)
        self.registar_btn.grid(row = row, column = 0, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")

        # Configuração do botão de sair
        self.sair_btn =  customtkinter.CTkButton(self.janela_registo, text = "Quit", font =customtkinter.CTkFont(size=14, weight='normal'), command = self.janela_registo.destroy)
        self.sair_btn.grid(row = row + 1, column = 0, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")
    
    def email_verificado(self):
        email_user = self.user_email_entry.get()

        print("Email recebido", email_user)

        if email_user!= "" and email_verificado(email_user):
            self._user_email_valido_lbl.configure(fg_color="green")
            return True
        else:
            print("Email invalido")
            tkinter.messagebox.showerror("Invalid Email",  "The email is not valid.")
            return False

    def registar_utilizador(self):
        # Pegar nos dados inseridos
        username = self.user_name_entry.get()
        password_user = self.user_password_entry.get()
        email_user = self.user_email_entry.get()
        
        if not self.email_verificado():
            return

        user = User()
        user.set_username(username)
        user.set_password(password_user)
        user.set_email(email_user)
        if hasattr(self, 'permission_list'):
            final_list = tuple([permission for permission, var in self.permission_checkboxes if var.get() == 1])
        else:
            final_list = list_permissions(user, 'Employer')
        if hasattr(self, 'role_name'):
            role_id = get_role_id(self.role_name.get())
            user.set_role_id(role_id)
            if self.role_name.get() == 'Client':
                perms_given = 'Employer'
            else:
                perms_given = 'SuperAdmin'
            available_permissions = list_permissions(user, perms_given)
            final_list = tuple(set(final_list).intersection(set(available_permissions)))
        
        registration = user.register(final_list)
        self.mensagem_registo_concluido = Label(self.janela_registo, text = registration[1], fg = registration[2])
        self.mensagem_registo_concluido.grid(row = 5, column = 0, columnspan = 2)
        if registration[0] == True:
            self.mensagem_registo_concluido.after(3000, self.janela_registo.destroy)