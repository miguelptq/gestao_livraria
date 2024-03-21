import customtkinter
from classes.janelas.janela_principal import JanelaPrincipal


#O tema  padrão é "dark" mas você pode mudar para o tema que preferir, basta trocar a palavra "dark" por outro nome de tema disponível
customtkinter.set_appearance_mode("System") 
#Tipo de Tema 
customtkinter.set_default_color_theme("blue")


#função main
def main():
    janela = JanelaPrincipal()
    janela.janela_principal.mainloop()

#roda função main se o arquivo
if __name__ == '__main__':
    main()lmknjtres