import tkinter 
import tkinter.messagebox
from typing import Tuple
import customtkinter


class utilizadores(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Configuração da janela
        self.title("Livraria José")
        self.geometry(f'{1100} x {500}')

        #Confugração do layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2,3), weight=0)
        self.grid_rowconfigure((0,1,2), weight=1)

        #menu lateral, label e grid
        self.menu_lateral= customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.menu_lateral.grid(row = 0, column = 0, rowspan = 4, sticky = "NSEW")
        self.menu_lateral.grid_rowconfigure(4, weight=1)
        self.logo_lbl = customtkinter.CTkLabel(self.menu_lateral, text="Users", font= customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_lbl.grid(row=0, column = 0, padx=20, pady=(20,10))
        #botoes e grids
        self.menu_lateral_botao1=customtkinter.CTkButton(self.menu_lateral, text="List Books" , command= self.listar_livros)
        self.menu_lateral_botao1.grid(row=1, column=0, padx=20, pady=10)
        self.menu_lateral_botao2 =customtkinter.CTkButton(self.menu_lateral, text="Borrow Books", command= self.emprestar_livros)
        self.menu_lateral_botao2.grid(row= 2, column = 0, padx=20, pady= 10)
        self.menu_lateral_botao3 = customtkinter.CTkButton(self.menu_lateral, text= "Return Books" ,command= self.devolver_livros)
        self.menu_lateral_botao3.grid(row=3, column=0, padx=20, pady=10)

        #label e grid do modo de aparência
        self.modo_aparencia_menu_opcao = customtkinter.CTkOptionMenu(self.menu_lateral,values=["Modo Dia", "Modo Noite", "Predefinição" ],
                                                                     command= self.mudar_modo_aparencia_event)
        self.modo_aparencia_menu_opcao.grid(row=6, column=0, padx=20, pady=(10,0))
        #label e grid da escala do menu lateral
        self.escala_lbl = customtkinter.CTkButton(self.menu_lateral, text="Escala", anchor="w")
        self.escala_lbl.grid(row=7, column = 0, padx=20, pady=(10,0))
        self.escala_opcao_menu =  customtkinter.CTkOptionMenu(self.menu_lateral,values=["80%", "90%", "100%", "110%", "120%" ],
                                                                     command= self.mudar_escala_event)
        self.escala_opcao_menu.grid(row=8, column=0, padx=20, pady=(10,20))



    def mudar_modo_aparencia_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def mudar_escala_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

