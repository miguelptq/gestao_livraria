from tkinter import *
from tkinter import Tk
from tkinter import ttk
import sqlite3
import hashlib
import os, customtkinter
from classes.user.user import User
from functions.functions import *
from classes.janelas.janela_editar_remover_user import JanelaEditarRemoverUser


class JanelaListUsers:
    def __init__(self, user):
        self.logged_user = user 
        if user:
            conn = sqlite3.connect('livraria.db')
            cursor = conn.cursor()
            cursor.execute("Select role_name FROM roles where id = ?",(user['role'],))
            self.registering_role_name = cursor.fetchone()[0]
            conn.close()
            self.permission_list = list_permissions(user, self.registering_role_name)
        list_of_roles_to_list = list_roles_depending_role(self.registering_role_name)
        list_roles = []
        for role in list_of_roles_to_list:
            if role[1] == 1:
                list_roles.append(role[0])
        self.roles_names = tuple(list_roles)
        self.placeholders = ', '.join(['?' for _ in self.roles_names])
        
        self.janela_lista_users = customtkinter.CTkToplevel()
        self.janela_lista_users.title('Lista de Utilizadores')
        self.janela_lista_users.iconbitmap('') # muda o Icon
        self.janela_lista_users.configure(bg="#f0f0f0")
        self.user_list_lbl = customtkinter.CTkLabel(self.janela_lista_users, text = 'Lista de Utilizadores', font=customtkinter.CTkFont(size=20, weight='bold'))
        self.user_list_lbl.grid(row = 0, column = 0, columnspan = 4, pady = 20, sticky = 'NSEW')
        # Configuração do campo de nome do utilizador
        self.user_name_lbl = customtkinter.CTkLabel(self.janela_lista_users, text = ' Nome do Utilizador', font=customtkinter.CTkFont(size=14, weight='normal'))
        self.user_name_lbl.grid(row = 1, column = 0, pady = 10, sticky='W')
        self.user_name_entry = customtkinter.CTkEntry(self.janela_lista_users, font = customtkinter.CTkFont(size=14, weight='normal'))
        self.user_name_entry.grid(row = 1, column = 1, pady = 10, sticky='W')

        #Botão de filtrar utilizadores
        self.filter_btn = customtkinter.CTkButton(self.janela_lista_users, text = "Filtrar", font=customtkinter.CTkFont(size=14, weight='normal'), command = self.filter_list)
        self.filter_btn.grid(row = 2, column = 1, pady = 10, sticky='W')

        #Botão de editar as informações do utilizadores
        self.editar_btn = customtkinter.CTkButton(self.janela_lista_users, text="Editar", font=customtkinter.CTkFont(size=14, weight='normal'), command=self.user_manager)
        self.editar_btn.grid(row=3, column=1, pady=10, sticky='W')


        #Botáo de sair
        self.sair_btn = customtkinter.CTkButton(self.janela_lista_users, text="Sair", font =customtkinter.CTkFont(size=14, weight='normal'), command = self.janela_lista_users.destroy )
        self.sair_btn.grid(row = 4, column=1, pady=10, sticky= 'W')


        conn = sqlite3.connect('livraria.db')
        cursor = conn.cursor()
        query, roles_names = self.get_list_no_filter()
        cursor.execute(query, roles_names)

        users_to_list = cursor.fetchall()
        conn.close()    
        users_data = {}
        for username, permission_name, role_name in users_to_list:
            if username not in users_data:
                users_data[username] = {'role': role_name, 'permissions': []}
            users_data[username]['permissions'].append(permission_name)

        # Create a Treeview widget
        self.tree= ttk.Treeview(self.janela_lista_users, columns=('Username', 'Cargo', 'Permissões'), show='headings')
        self.tree.heading('Username', text='Username', command=lambda: self.tree.column('Username'))
        self.tree.heading('Cargo', text='Cargo', command=lambda: self.tree.column('Role'))
        self.tree.heading('Permissões', text='Permissões', command=lambda: self.tree.column('Permissions'))

        for username, data in users_data.items():
            permissions = ', '.join(data['permissions'])
            self.tree.insert('', 'end', values=(username, data['role'], permissions))
            self.tree.bind("<Double-1>", lambda event: self.user_manager(event, self.tree))
        self.tree.grid(row=2, column=0, sticky='nsew')
        self.janela_lista_users.grid_rowconfigure(0, weight=1)
        self.janela_lista_users.grid_columnconfigure(0, weight=1)
    
    
    
    def filter_list(self):
        name_search = self.user_name_entry.get()
        query, roles_names = self.get_list_no_filter()
        if name_search != '':
            query += f" AND u.username LIKE '%{name_search}%'"
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect('livraria.db')
        cursor = conn.cursor()
        cursor.execute(query, roles_names)
        results = cursor.fetchall()
        conn.close()
        filtered_data = {}
        for username, permission_name, role_name in results:
            if username not in filtered_data:
                filtered_data[username] = {'role': role_name, 'permissions': []}
            filtered_data[username]['permissions'].append(permission_name)
        for username, data in filtered_data.items():
            permissions = ', '.join(data['permissions'])
            self.tree.insert('', 'end', values=(username, data['role'], permissions))
        

    def get_list_no_filter(self):
        query = f"""SELECT u.username, p.permission_name, r.role_name 
                    FROM users u
                    JOIN roles r ON u.role_id = r.id
                    JOIN user_permissions up ON u.id = up.user_id
                    JOIN permissions p ON up.permission_id = p.id
                    WHERE r.role_name IN ({', '.join(['?'] * len(self.roles_names))})"""
        return query, self.roles_names

    def user_manager(self, event=None):
        #item escolihdo na treeview
        item_escolhido = self.tree.focus()
        if item_escolhido:
            values = self.tree.item(item_escolhido, 'values')
            if values:
                username = values[0]
                role = values[1]
                permissions = values[2]
            user = {
                "username":username,
                "role": role,
                "permissions": permissions.split(', ')
            }
            open_user_manager = JanelaEditarRemoverUser(self.registering_role_name, user)
