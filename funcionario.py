import tkinter as tk
from tkinter import ttk
import customtkinter as ck
import classcrud

def voltar(janelaFuncionario, janelaMenu):
    janelaMenu.deiconify()
    janelaFuncionario.destroy()

def funcionario(nvl, janelaMenu):
    # Janela
    janelaFuncionario = ck.CTkToplevel()
    x, y = 800, 500
    posx, posy = int((janelaFuncionario.winfo_screenwidth()-x)/2), int((janelaFuncionario.winfo_screenheight()-y)/2)
    janelaFuncionario.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaFuncionario.resizable(False, False)
    janelaFuncionario.after(200, lambda: janelaFuncionario.iconbitmap('icon.ico'))
    janelaFuncionario.title('Sistema de Controle de acesso')
    janelaMenu.withdraw()
    janelaFuncionario.protocol("WM_DELETE_WINDOW", lambda: voltar(janelaFuncionario, janelaMenu))

    # Título
    ck.CTkLabel(janelaFuncionario, text='Funcionários', font=ck.CTkFont(size=15)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Usuário
    ck.CTkLabel(janelaFuncionario, text=nvl[0], font=ck.CTkFont(size=15)).place(relx=0.92, rely=0.05, anchor=tk.CENTER)

    # Entry - ID do funcionário
    labelIDF = ck.CTkLabel(janelaFuncionario, text='ID do Funcionário')
    labelIDF.place(relx=0.2, rely=0.16, anchor=tk.CENTER)
    IDFuncionario = ck.CTkEntry(janelaFuncionario)
    IDFuncionario.place(relx=0.2, rely=0.21, anchor=tk.CENTER)

    # Entry - Nome do funcionário
    labelNFuncionario = ck.CTkLabel(janelaFuncionario, text='Nome')
    labelNFuncionario.place(relx=0.4, rely=0.16, anchor=tk.CENTER)
    nomeFuncionario = ck.CTkEntry(janelaFuncionario)
    nomeFuncionario.place(relx=0.4, rely=0.21, anchor=tk.CENTER)

    # Entry - E-mail do funcionário
    labelEmailFuncionario = ck.CTkLabel(janelaFuncionario, text='E-Mail')
    labelEmailFuncionario.place(relx=0.6, rely=0.16, anchor=tk.CENTER)
    emailFuncionario = ck.CTkEntry(janelaFuncionario)
    emailFuncionario.place(relx=0.6, rely=0.21, anchor=tk.CENTER)

    # ComboBox - setor do funcionário
    labelSFuncionario = ck.CTkLabel(janelaFuncionario, text='Setor')
    labelSFuncionario.place(relx=0.8, rely=0.16, anchor=tk.CENTER)
    registros = classcrud.fillComboboxSetor(janelaFuncionario)
    comboboxPadrao = ck.StringVar(value='Sem registros' if registros == [] else registros[0][0]) 
    setorFuncionario = ck.CTkComboBox(janelaFuncionario, state='readonly', variable=comboboxPadrao, values=['Sem registros'] if registros == [] else [registro[0] for registro in registros])
    setorFuncionario.place(relx=0.8, rely=0.21, anchor=tk.CENTER)
    
    # Estilo TreeView
    style = ttk.Style()
    style.theme_use('default')
    style.configure('estilo.Treeview.Heading', background='#565b5e', foreground='White',fieldbackground='silver', padding=3)
    style.configure('estilo.Treeview', background='#242424', foreground='White',fieldbackground='#242424')
    style.map('estilo.Treeview.Heading', foreground=[('active','Black')])
    style.map('estilo.Treeview', background=[('selected','#1f6aa5')], foreground=[('selected','white')])
    # TreeView
    colunas = ('ID', 'Nome', 'Email', 'Setor')            
    treeFuncionario = ttk.Treeview(janelaFuncionario, columns=colunas, selectmode='browse', style='estilo.Treeview')
    treeFuncionario['show'] = 'headings'
    # Scrollbar
    scroll = ck.CTkScrollbar(janelaFuncionario, orientation='vertical', command=treeFuncionario.yview, height=224)        
    scroll.pack(side ='right', fill ='x')
    treeFuncionario.configure(yscrollcommand=scroll.set)
    scroll.place(relx=0.861, rely=0.7, anchor=tk.CENTER)
    # Cabeçalho
    treeFuncionario.heading('ID', text='ID')
    treeFuncionario.heading('Nome', text='Nome')
    treeFuncionario.heading ('Email', text='E-mail')
    treeFuncionario.heading ('Setor', text='Setor')
    # Colunas
    treeFuncionario.column('ID',minwidth=0,width=140, anchor=tk.CENTER)
    treeFuncionario.column('Nome',minwidth=0,width=140, anchor=tk.CENTER)
    treeFuncionario.column('Email',minwidth=0,width=140, anchor=tk.CENTER)
    treeFuncionario.column('Setor',minwidth=0,width=140, anchor=tk.CENTER)
    treeFuncionario.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    # Selecionar
    def selecionarRegistros(event):
        IDFuncionario.delete(0, tk.END)
        nomeFuncionario.delete(0, tk.END)
        emailFuncionario.delete(0, tk.END)
        setorFuncionario.set(registros[0][0])

        for selecao in treeFuncionario.selection():  
            item = treeFuncionario.item(selecao)  
            idfunc, nomefunc, emailfunc, setorfunc = item["values"][0:4]  
            IDFuncionario.insert(0, idfunc)  
            nomeFuncionario.insert(0, nomefunc)
            emailFuncionario.insert(0, emailfunc)
            setorFuncionario.set(setorfunc)

    treeFuncionario.bind("<<TreeviewSelect>>", selecionarRegistros)

    # Button - Inserir
    inserirbtn = ck.CTkButton(janelaFuncionario, text='Inserir', command=lambda: classcrud.insertFuncionario(nomeFuncionario, emailFuncionario, setorFuncionario, registros, treeFuncionario, janelaFuncionario))
    inserirbtn.place(relx=0.25, rely=0.33, anchor=tk.CENTER)

    # Button - Atualizar
    atualizarbtn = ck.CTkButton(janelaFuncionario, text='Atualizar', command=lambda: classcrud.updateFuncionario(IDFuncionario, nomeFuncionario, emailFuncionario, setorFuncionario, registros, treeFuncionario, janelaFuncionario))
    atualizarbtn.place(relx=0.50, rely=0.33, anchor=tk.CENTER)

    # Button - Remover
    removerbtn = ck.CTkButton(janelaFuncionario, text='Remover', command=lambda: classcrud.deleteFuncionario(IDFuncionario, treeFuncionario, janelaFuncionario))
    removerbtn.place(relx=0.75, rely=0.33, anchor=tk.CENTER)

    # Button - Voltar
    inserirbtn = ck.CTkButton(janelaFuncionario, width=50, text='Voltar', command=lambda: voltar(janelaFuncionario, janelaMenu))
    inserirbtn.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

    # Esc para voltar
    janelaFuncionario.bind('<Escape>', lambda event: voltar(janelaFuncionario, janelaMenu))

    # Atualização TreeView
    classcrud.attTreeFuncionario(treeFuncionario, janelaFuncionario)

    janelaFuncionario.mainloop()
