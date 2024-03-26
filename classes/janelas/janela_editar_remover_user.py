from tkinter import *
from tkinter import Tk
from tkinter import ttk
import sqlite3
import hashlib
import os, customtkinter
from classes.user.user import User
from functions.functions import *
from tkinter import messagebox


class JanelaEditarRemoverUser():
    def __init__(self, logged_role, user):
        self.janela_user_manage = customtkinter.CTkToplevel()
        self.janela_user_manage.title('Manage Users') # muda o titulo
        self.janela_user_manage.iconbitmap('') # muda o Icon
        self.janela_user_manage.configure(bg="#f0f0f0")
        self.user_title = customtkinter.CTkLabel(self.janela_user_manage, text = f'Manage Users: {user['username']}',font=customtkinter.CTkFont(size=20, weight='bold'))
        self.user_title.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
        self.permission_list = list_permissions(user, logged_role)
        self.permission_checkboxes = []
        for index, permission in enumerate(self.permission_list):
            var = IntVar()
            checkbox = customtkinter.CTkCheckBox(self.janela_user_manage, text=permission, variable=var, font=customtkinter.CTkFont(size=14, weight='bold'), command=lambda var=var: self.permission_checkbox_state_changed(var))
            checkbox.grid(row=index + 1, column=0, columnspan=2, pady=5, sticky='W')
            if permission in tuple(user['permissions']):
                var.set(1)
            self.permission_checkboxes.append((permission, var))        
        self.update_button = customtkinter.CTkButton(self.janela_user_manage, text = "Save", font=customtkinter.CTkFont(size=14, weight='normal'), command = lambda: self.update_user(user, logged_role))
        self.update_button.grid(row = index + 2, column = 0, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")
        self.remove_button = customtkinter.CTkButton(self.janela_user_manage, text = "Remove", font=customtkinter.CTkFont(size=14, weight='normal'), command = lambda: self.remove_user(user))
        self.remove_button.grid(row = index + 3, column = 0, columnspan = 2, padx = 20, pady = 10, sticky = "NSEW")
    
    def update_user(self, user, final_list):
        try:
            final_list = tuple([permission for permission, var in self.permission_checkboxes if var.get() == 1])
        
            if user['role'] == 'Client':
                perms_given = 'Employer'
            else:
                perms_given = 'SuperAdmin'
            available_permissions = list_permissions(user, perms_given)
            final_list = tuple(set(final_list).intersection(set(available_permissions)))
            final_list_id = self.get_permissions_ids(final_list)

            self.delete_user_permissions(user['username'])
            for permission in final_list_id:
                self.insert_user_permission(user['username'], permission)
            
                messagebox.showinfo("Updated", "User updated sucessfully.")
            if self.janela_user_manage:
                self.janela_user_manage.withdraw()
        except Exception as e:
                messagebox.showerror("Error", f"\n{(e)}")
            

    def remove_user(self, user):
        try:
            result = messagebox.askquestion(title="Delete User", message=f"Are you sure you want to delete '{user['username']}'?")
            if result == 'yes':
                conn = sqlite3.connect('livraria.db')
                c = conn.cursor()
                c.execute("SELECT COUNT(*) FROM livro WHERE user_id = (SELECT id FROM users WHERE username = ?)", (user['username'],))
                count = c.fetchone()[0]
                if count > 0:
                    messagebox.showerror("Erro", f"O utilizador{user['username']} tem de devolver os livros primeiro, tem {count} livros por devolver!")
                else:
                    self.delete_user_permissions(user['username'])
                    c.execute("DELETE FROM users WHERE username = ?", (user['username'],))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo(title="Delete User", message=f"O utilizador {user['username']} foi eliminado com sucesso.")
            if self.janela_user_manage:
                self.janela_user_manage.withdraw()
        except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível remover o utilizador")
       
        
        pass

    def permission_checkbox_state_changed(self, var):
        permission, state = self.permission_checkboxes[var.get()]
        print(f"Permissão '{permission}' modificada para {state}")
    
    def get_user_permissions(self,username):
        conn = sqlite3.connect('livraria.db')
        c = conn.cursor()
        c.execute("SELECT p.permission_name FROM user_permissions up JOIN permissions p ON up.permission_id = p.id WHERE user_id = (SELECT id FROM users WHERE username = ?)",(username,))
        permissions = [row[0] for row in c.fetchall()]
        conn.close()
        return permissions

    def delete_user_permissions(self,username):
        conn = sqlite3.connect('livraria.db')
        c = conn.cursor()
        c.execute("DELETE FROM user_permissions WHERE user_id = (SELECT id FROM users WHERE username = ?)", (username,))
        conn.commit()
        conn.close()

    def insert_user_permission(self, username, permission):
        conn = sqlite3.connect('livraria.db')
        c = conn.cursor()
        c.execute("INSERT INTO user_permissions (user_id, permission_id) SELECT id, ? FROM users WHERE username = ?", (permission, username))
        conn.commit()
        conn.close()
    
    def get_permissions_ids(self, permissions):
        permissions = permissions
        query = f"SELECT id FROM permissions WHERE permission_name IN ({', '.join(['?'] * len(permissions))})"
        conn = sqlite3.connect('livraria.db')
        cursor = conn.cursor()
        cursor.execute(query,permissions)
        permissions_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return permissions_ids