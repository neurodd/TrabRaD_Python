import tkinter as tk
from tkinter import ttk
import customtkinter as ck
import classcrud

def voltar(janelaLocal, janelaMenu):
    janelaMenu.deiconify()
    janelaLocal.destroy()

def local(nvl, janelaMenu):
    # Janela
    janelaLocal = ck.CTkToplevel()
    x, y = 800, 500
    posx, posy = int((janelaLocal.winfo_screenwidth()-x)/2), int((janelaLocal.winfo_screenheight()-y)/2)
    janelaLocal.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaLocal.resizable(False, False)
    janelaLocal.after(200, lambda: janelaLocal.iconbitmap('icon.ico'))
    janelaLocal.title('Sistema de Controle de acesso')
    janelaMenu.withdraw()
    janelaLocal.protocol('WM_DELETE_WINDOW', lambda: voltar(janelaLocal, janelaMenu))

    # Título
    ck.CTkLabel(janelaLocal, text='Locais', font=ck.CTkFont(size=15)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Usuário
    ck.CTkLabel(janelaLocal, text=nvl[0], font=ck.CTkFont(size=15)).place(relx=0.92, rely=0.05, anchor=tk.CENTER)

    # Entry - ID do local
    labelIDL = ck.CTkLabel(janelaLocal, text='ID do local')
    labelIDL.place(relx=0.33, rely=0.16, anchor=tk.CENTER)
    IDLocal = ck.CTkEntry(janelaLocal)
    IDLocal.place(relx=0.33, rely=0.21, anchor=tk.CENTER)

    # Entry - Nome do local
    labelNLocal = ck.CTkLabel(janelaLocal, text='Nome')
    labelNLocal.place(relx=0.66, rely=0.16, anchor=tk.CENTER)
    nomeLocal = ck.CTkEntry(janelaLocal)
    nomeLocal.place(relx=0.66, rely=0.21, anchor=tk.CENTER)

    # Estilo TreeView
    style = ttk.Style()
    style.theme_use('default')
    style.configure('estilo.Treeview.Heading', background='#565b5e', foreground='White',fieldbackground='silver', padding=3)
    style.configure('estilo.Treeview', background='#242424', foreground='White',fieldbackground='#242424')
    style.map('estilo.Treeview.Heading', foreground=[('active','Black')])
    style.map('estilo.Treeview', background=[('selected','#1f6aa5')], foreground=[('selected','white')])
    # TreeView
    colunas = ('ID', 'Nome')            
    treeLocal = ttk.Treeview(janelaLocal, columns=colunas, selectmode='browse', style='estilo.Treeview')
    treeLocal['show'] = 'headings'
    # Scrollbar
    scroll = ck.CTkScrollbar(janelaLocal, orientation='vertical', command=treeLocal.yview, height=224)        
    scroll.pack(side ='right', fill ='x')
    treeLocal.configure(yscrollcommand=scroll.set)
    scroll.place(relx=0.686, rely=0.7, anchor=tk.CENTER)
    # Cabeçalho
    treeLocal.heading('ID', text='ID')
    treeLocal.heading('Nome', text='Nome')
    # Colunas
    treeLocal.column('ID',minwidth=0,width=140, anchor=tk.CENTER)
    treeLocal.column('Nome',minwidth=0,width=140, anchor=tk.CENTER)
    treeLocal.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    # Selecionar
    def selecionarRegistros(event):
        IDLocal.delete(0, tk.END)
        nomeLocal.delete(0, tk.END)

        for selecao in treeLocal.selection():  
            item = treeLocal.item(selecao)  
            IDlocal, nomelocal = item["values"][0:2]  
            IDLocal.insert(0, IDlocal)  
            nomeLocal.insert(0, nomelocal)

    treeLocal.bind("<<TreeviewSelect>>", selecionarRegistros)

    # Button - Inserir
    inserirbtn = ck.CTkButton(janelaLocal, text='Inserir', command=lambda: classcrud.insertLocal(nomeLocal, treeLocal, janelaLocal))
    inserirbtn.place(relx=0.25, rely=0.33, anchor=tk.CENTER)

    # Button - Atualizar
    atualizarbtn = ck.CTkButton(janelaLocal, text='Atualizar', command=lambda: classcrud.updateLocal(IDLocal, nomeLocal, treeLocal, janelaLocal))
    atualizarbtn.place(relx=0.50, rely=0.33, anchor=tk.CENTER)

    # Button - Remover
    removerbtn = ck.CTkButton(janelaLocal, text='Remover', command=lambda: classcrud.deleteLocal(IDLocal, treeLocal, janelaLocal))
    removerbtn.place(relx=0.75, rely=0.33, anchor=tk.CENTER)

    # Button - Voltar
    inserirbtn = ck.CTkButton(janelaLocal, width=50, text='Voltar', command=lambda: voltar(janelaLocal, janelaMenu))
    inserirbtn.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

    # Esc para voltar
    janelaLocal.bind('<Escape>', lambda event: voltar(janelaLocal, janelaMenu))

    # Atualização TreeView
    classcrud.attTreeLocal(treeLocal, janelaLocal)

    janelaLocal.mainloop()
