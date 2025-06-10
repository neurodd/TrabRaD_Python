import tkinter as tk
from tkinter import ttk
import customtkinter as ck
import classcrud
import acesso
import setor
import funcionario
import usuario
import local

def voltar(janelaMenuAdmin, janelaMain):
    janelaMain.deiconify()
    janelaMenuAdmin.destroy()

def menuAdmin(nvl, janelaMain):
    # Janela
    janelaMenuAdmin = ck.CTkToplevel()
    x, y = 800, 500
    posx, posy = int((janelaMenuAdmin.winfo_screenwidth()-x)/2), int((janelaMenuAdmin.winfo_screenheight()-y)/2)
    janelaMenuAdmin.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaMenuAdmin.resizable(False, False)
    janelaMenuAdmin.after(200, lambda: janelaMenuAdmin.iconbitmap('icon.ico'))
    janelaMenuAdmin.title('Sistema de Controle de acesso')
    janelaMain.withdraw()
    janelaMenuAdmin.protocol("WM_DELETE_WINDOW", lambda: voltar(janelaMenuAdmin, janelaMain))

    # Título
    ck.CTkLabel(janelaMenuAdmin, text='Menu', font=ck.CTkFont(size=15)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Usuário
    ck.CTkLabel(janelaMenuAdmin, text=nvl[0], font=ck.CTkFont(size=15)).place(relx=0.92, rely=0.05, anchor=tk.CENTER)

    # Usuário - Trocar senha
    if nvl[0] != 'admin':
        btnTrocarSenha = ck.CTkButton(janelaMenuAdmin, text='Trocar senha', font=ck.CTkFont(size=11, underline=True), fg_color='transparent', hover_color='#242424', width=45, height=8, command=lambda: usuario.trocarSenha(nvl, janelaMenuAdmin, janelaMain))
        btnTrocarSenha.place(relx=0.92, rely=0.095, anchor=tk.CENTER)

    # Button - Acesso
    acessobtn = ck.CTkButton(janelaMenuAdmin, text='Acesso', width=180, height=30, command=lambda: acesso.acesso(nvl, janelaMenuAdmin))
    acessobtn.place(relx=0.5, rely=0.33, anchor=tk.CENTER)

    # Button - Setor
    setorbtn = ck.CTkButton(janelaMenuAdmin, text='Setor', command=lambda: setor.setor(nvl, janelaMenuAdmin))
    setorbtn.place(relx=0.25, rely=0.5478, anchor=tk.CENTER)

    # Button - Funcionario
    funcionariobtn = ck.CTkButton(janelaMenuAdmin, text='Funcionário', command=lambda: funcionario.funcionario(nvl, janelaMenuAdmin))
    funcionariobtn.place(relx=0.75, rely=0.5478, anchor=tk.CENTER)

    # Button - Usuario
    usuariobtn = ck.CTkButton(janelaMenuAdmin, text='Usuário', command=lambda: usuario.usuario(nvl, janelaMenuAdmin))
    usuariobtn.place(relx=0.25, rely=0.7656, anchor=tk.CENTER)

    # Button - Local
    localbtn = ck.CTkButton(janelaMenuAdmin, text='Local', command=lambda: local.local(nvl, janelaMenuAdmin))
    localbtn.place(relx=0.75, rely=0.7656, anchor=tk.CENTER)

    # Button - Sair
    sairbtn = ck.CTkButton(janelaMenuAdmin, width=50, text='Sair', command=lambda: voltar(janelaMenuAdmin, janelaMain))
    sairbtn.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

    janelaMenuAdmin.mainloop()
