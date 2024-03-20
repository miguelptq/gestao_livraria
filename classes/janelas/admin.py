import tkinter 
import tkinter.messagebox
from typing import Tuple
import customtkinter


class Admin(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Configuração da janela
        self.title("Livraria José")
        self.geometry(f'{850} x {500}')

        #Confugração do layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2,3), weight=0)
        self.grid_rowconfigure((0,1,2), weight=1)

        #menu lateral, label e grid
        self.menu_lateral= customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.menu_lateral.grid(row = 0, column = 0, rowspan = 4, sticky = "NSEW")
        self.menu_lateral.grid_rowconfigure(4, weight=1)
        self.logo_lbl = customtkinter.CTkLabel(self.menu_lateral, text="Super Admin", font= customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_lbl.grid(row=0, column = 0, padx=20, pady=(20,10))
        #botoes e grids
        self.menu_lateral_botao1=customtkinter.CTkButton(self.menu_lateral, text="Adicionar Livros" , command= self.menu_lateral_button_adicionar_livro)
        self.menu_lateral_botao1.grid(row=1, column=0, padx=20, pady=10)
        self.menu_lateral_botao2 =customtkinter.CTkButton(self.menu_lateral, text="Remover Livros", command=self.menu_lateral_button_remover_livro)
        self.menu_lateral_botao2.grid(row= 2, column = 0, padx=20, pady= 10)
        self.menu_lateral_botao3 = customtkinter.CTkButton(self.menu_lateral, text= "Listar Livros", command=self.menu_lateral_button_listar_livro)
        self.menu_lateral_botao3.grid(row=3, column=0, padx=20, pady=10)
        self.menu_lateral_botao3 = customtkinter.CTkButton(self.menu_lateral, text= "Editar Livros", command=self.menu_lateral_button_editar_livro)
        self.menu_lateral_botao3.grid(row=4, column=0, padx=20, pady=10)
        self.menu_lateral_botao4 = customtkinter.CTkButton(self.menu_lateral, text= "Gerir Utilizadores")
        self.menu_lateral_botao4.grid(row=5, column=0, padx=20, pady=10)



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


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Insira um numero", title="")
        print("Número inserido:", dialog.get_input())

    def mudar_modo_aparencia_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def mudar_escala_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


    def menu_lateral_button_adicionar_livro(self):

        adicionar_livros = AdicionarLivros(self)

    def menu_lateral_button_remover_livro(self):
        remover_livros = RemoverLivros(self)

    def menu_lateral_button_listar_livro(self):
        listar_livros = ListarLivros(self)

    def menu_lateral_button_editar_livro(self):
        editar_livros = EditarLivros(self)




class RemoverLivros(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        #Configuração da janela
        self.title("Livraria José")
        self.geometry(f'{850} x {500}')

        #Confugração do layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2,3), weight=0)
        self.grid_rowconfigure((0,1,2), weight=1)        

        self.logo_lbl = customtkinter.CTkLabel(self, text="Insira o Titulo, Autor ou ISBN do livro: ", font= customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_entry = customtkinter.CTkEntry(self)
        self.logo_lbl.grid(row=0, column = 0, padx=20, pady=(20,10))
        self.logo_entry.grid(row=0, column=1, padx=20, pady=(20,10))

       # Botão para confirmar a remoção do livro
        self.confirmar_btn = customtkinter.CTkButton(self, text="Confirmar", command=self.confirmar_livro_removido)
        self.confirmar_btn.grid(row=4, column=0, padx=20, pady=(20, 10))    
    
    def confirmar_livro_removido(self):
        tkinter.messagebox.showinfo("Adicionar Livro", "Livro removido com sucesso")
        self.deiconify()  # Mostrar a janela principal novamente após o livro ser adicionado com sucesso
        self.destroy()  # Fechar a janela

class EditarLivros(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # Configuração da janela
        self.title("Editar Livro")
        self.geometry(f'{400}x{300}')

        # Labels para as opções de edição
        self.titulo_check = customtkinter.CTkCheckBox(self, text="Título")
        self.titulo_check.grid(row=0, column=0, padx=20, pady=10)
        self.titulo_check.grid(row=0, column=1, padx=20, pady=(20,10))        
        
        self.autor_check = customtkinter.CTkCheckBox(self, text="Autor")
        self.autor_check.grid(row=1, column=0, padx=20, pady=10)
        self.autor_check.grid(row=1, column=1, padx=20, pady=(20,10))        

        self.descricao_check = customtkinter.CTkCheckBox(self, text="Descrição")
        self.descricao_check.grid(row=2, column=0, padx=20, pady=10)
        self.descricao_check.grid(row=2, column=1, padx=20, pady=(20,10))

        # Botão para confirmar a edição do livro
        self.confirmar_btn = customtkinter.CTkButton(self, text="Confirmar", command=self.confirmar_edicao)
        self.confirmar_btn.grid(row=3, column=0, padx=20, pady=10)

    def confirmar_edicao(self):
        # Aqui podes adicionar a lógica para aplicar as edições
        # por exemplo, verifica quais as checkboxes estão marcados e edita as propriedades correspondentes
        # depois, fecha a janela
        tkinter.messagebox.showinfo("Adicionar Livro", "Livro editado com sucesso")
        self.deiconify()  # Mostrar a janela principal novamente após o livro ser adicionado com sucesso
        self.destroy()  # Fechar a janela



class ListarLivros(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # Configuração da janela
        self.title("Editar Livro")
        self.geometry(f'{400}x{300}')

        # Lista de livros
        self.lista_livros = customtkinter.CTkListbox(self)
        self.lista_livros.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        # Botão para atualizar a lista
        self.atualizar_btn = customtkinter.CTkButton(self, text="Atualizar Lista", command=self.atualizar_lista)
        self.atualizar_btn.grid(row=1, column=0, padx=20, pady=10)

        # Populando a lista de livros inicialmente
        self.atualizar_lista()

def atualizar_lista(self):
    # Aqui pdoes adicionar a lógica para atualizar a lista de livros
    # Por exemplo, limpar a lista atual e adicionar os livros devolvidos ou emprestados
     # Após a atualização, você pode chamar este método para refletir as alterações na interface do usuário
    self.lista_livros.delete(0, customtkinter.END)
    # Adicione os livros à lista, conforme necessário
    # Exemplo: self.lista_livros.insert(customtkinter.END, "Título do Livro")
    tkinter.messagebox.showinfo("Adicionar Livro", "Livros atualizados!")
    self.deiconify()  # Mostrar a janela principal novamente após o livro ser adicionado com sucesso
    self.destroy()  # Fechar a janela

