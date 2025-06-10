import sqlite3 as conector
import tkinter as tk
from CTkMessagebox import CTkMessagebox
import hashlib
import menuAdmin
import acesso

#--------------------------------------------------------------------------
# Classes
#--------------------------------------------------------------------------
class Acesso:
    def __init__(self, IDFunc, IDLocal, tipo):
        self.__IDFunc = IDFunc
        self.__IDLocal = IDLocal
        self.__tipo = tipo
    
    @property
    def IDFunc(self):
        return self.__IDFunc

    @property
    def IDLocal(self):
        return self.__IDLocal

    @property
    def tipo(self):
        return self.__tipo
    
class Setor:
    def __init__(self):
        self.__IDSetor = 0
        self.__nomeSetor = ''
        self.__descSetor = ''

    @property
    def IDSetor(self):
        return self.__IDSetor

    @IDSetor.setter    
    def IDSetor(self, IDSetor):
        self.__IDSetor = IDSetor

    @property
    def nomeSetor(self):
        return self.__nomeSetor

    @nomeSetor.setter 
    def nomeSetor(self, nomeSetor):
        self.__nomeSetor = nomeSetor

    @property
    def descSetor(self):
        return self.__descSetor

    @descSetor.setter 
    def descSetor(self, descSetor):
        self.__descSetor = descSetor

class Funcionario:
    def __init__(self):
        self.__IDFuncionario = 0
        self.__nomeFuncionario = ''
        self.__IDSetorFuncionario = 0
        self.__emailFuncionario = ''

    @property
    def IDFuncionario(self):
        return self.__IDFuncionario

    @IDFuncionario.setter    
    def IDFuncionario(self, IDFuncionario):
        self.__IDFuncionario = IDFuncionario

    @property
    def nomeFuncionario(self):
        return self.__nomeFuncionario

    @nomeFuncionario.setter    
    def nomeFuncionario(self, nomeFuncionario):
        self.__nomeFuncionario = nomeFuncionario

    @property
    def IDSetorFuncionario(self):
        return self.__IDSetorFuncionario

    @IDSetorFuncionario.setter    
    def IDSetorFuncionario(self, IDSetorFuncionario):
        self.__IDSetorFuncionario = IDSetorFuncionario

    @property
    def emailFuncionario(self):
        return self.__emailFuncionario

    @emailFuncionario.setter    
    def emailFuncionario(self, emailFuncionario):
        self.__emailFuncionario = emailFuncionario

class Usuario:
    def __init__(self):
        self.__IDUsuario = 0
        self.__nomeUsuario = ''
        self.__senhaUsuario = ''
        self.__IDFuncionario = 0
        self.__usuAdmin = ''

    @property
    def IDUsuario(self):
        return self.__IDUsuario

    @IDUsuario.setter    
    def IDUsuario(self, IDUsuario):
        self.__IDUsuario = IDUsuario

    @property
    def nomeUsuario(self):
        return self.__nomeUsuario

    @nomeUsuario.setter    
    def nomeUsuario(self, nomeUsuario):
        self.__nomeUsuario = nomeUsuario

    @property
    def senhaUsuario(self):
        return self.__senhaUsuario

    @senhaUsuario.setter    
    def senhaUsuario(self, senhaUsuario):
        self.__senhaUsuario = senhaUsuario

    @property
    def IDFuncionario(self):
        return self.__IDFuncionario

    @IDFuncionario.setter    
    def IDFuncionario(self, IDFuncionario):
        self.__IDFuncionario = IDFuncionario

    @property
    def usuAdmin(self):
        return self.__usuAdmin

    @usuAdmin.setter    
    def usuAdmin(self, usuAdmin):
        self.__usuAdmin = usuAdmin

class Local:    
    def __init__(self):
        self.__IDLocal = 0
        self.__nomeLocal = ''

    @property
    def IDLocal(self):
        return self.__IDLocal

    @IDLocal.setter    
    def IDLocal(self, IDLocal):
        self.__IDLocal = IDLocal

    @property
    def nomeLocal(self):
        return self.__nomeLocal

    @nomeLocal.setter    
    def nomeLocal(self, nomeLocal):
        self.__nomeLocal = nomeLocal

class Login:
    def __init__(self, lgnUsuario, lgnSenha):
        self.__lgnUsuario = lgnUsuario
        self.__lgnSenha = lgnSenha
    
    @property
    def lgnUsuario(self):
        return self.__lgnUsuario

    @property
    def lgnSenha(self):
        return self.__lgnSenha

#--------------------------------------------------------------------------
# Abrir Conexão
#--------------------------------------------------------------------------
def abrirConexao():
    try:
        conexao = conector.connect('Banco/db_controle_acesso.db')
        cursor = conexao.cursor()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao conectar-se com o banco de dados: {erro}')
    finally:    
        return conexao, cursor

#--------------------------------------------------------------------------
# Fechar Conexão
#--------------------------------------------------------------------------
def fecharConexao(conexao, cursor):
    cursor.close()
    conexao.close()
    return conexao, cursor

#--------------------------------------------------------------------------
# Verificação Funcionário e Email existe
#--------------------------------------------------------------------------
def verificarFuncionario(IDFuncionario, cursor):  # Verifica se funcionário existe
    cursor.execute('SELECT COUNT(*) FROM funcionario WHERE funcionario_ID = ?', (IDFuncionario, ))
    selectFunc = cursor.fetchone()[0]
    return selectFunc

def verificarEmailFuncionario(emailFuncionario, cursor):  # Verifica se email existe
    cursor.execute('SELECT COUNT(*) FROM funcionario WHERE email = ?', (emailFuncionario, ))
    selectemailFuncionario = cursor.fetchone()[0]
    return selectemailFuncionario

#--------------------------------------------------------------------------
# CRUD Acesso
#--------------------------------------------------------------------------
def fillComboboxLocal(janelaAcesso):    # Preenchimento dos locais
    try:
        conexao, cursor = abrirConexao()
        comando = '''SELECT nome_local FROM Local ORDER BY nome_local;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao listar os locais: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
    return registros

def attTreeAcesso(treeAcessos, janelaAcesso):   # Atualização TreeView
    # Apaga registros antigos
    for registro in treeAcessos.get_children():
        treeAcessos.delete(registro)
    try:
        # Select - Acessos
        conexao, cursor = abrirConexao()
        comando = '''SELECT f.nome, s.nome_setor, a.tipo, l.nome_local,  strftime("%d/%m/%Y - %H:%M", a.data_hora)
                        FROM Acesso a
                        JOIN Funcionario f ON a.funcionario_ID = f.funcionario_ID
                        JOIN Setor s ON f.setor_ID = s.setor_ID
                        JOIN Local l ON a.local_ID = l.local_ID
                        ORDER BY a.data_hora DESC;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
        # Coloca novos registros
        for registro in registros:
            treeNome = registro[0]
            treeSetor = registro[1]
            treeTipo = registro[2]
            treeLocal = registro[3]
            treeDt_hr = registro[4]
            treeAcessos.insert('', 'end', values=(treeNome, treeSetor, treeTipo, treeLocal, treeDt_hr))           
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao exibir os acessos: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def pegarIDLocal(local, cursor):    # Pega o ID do local selecionado
    cursor.execute('SELECT local_ID FROM Local WHERE nome_local = ?', (local.get(), ))
    selectLocal_ID = cursor.fetchone()[0]
    return selectLocal_ID

def insertAcesso(IDFunc, local, registros, tipo, treeAcessos, janelaAcesso):   # Insert tabela Acesso
    try:
        conexao, cursor = abrirConexao()
        # Verificação Funcionário
        selectFunc = verificarFuncionario(IDFunc.get(), cursor)
        if selectFunc == 0:
            CTkMessagebox(title='Erro', icon='cancel', message='Funcionário não encontrado')
            return
        # ID admin
        if IDFunc.get() == '1':
            CTkMessagebox(title='Erro', icon='cancel', message='Funcionário não encontrado')
            return
        # ID do local
        if local.get() == 'Sem registros':
            CTkMessagebox(title='Erro', icon='cancel', message='Local não encontrado')
            return
        else:
            selectLocal_ID = pegarIDLocal(local, cursor)
        # Instância da classe Acesso
        acesso = Acesso(IDFunc.get(), selectLocal_ID, tipo.get())
        # Insert - Acesso
        comando = '''INSERT INTO acesso (funcionario_ID, local_ID, tipo) 
                        VALUES (?, ?, ?);'''
        cursor.execute(comando, (acesso.IDFunc, acesso.IDLocal, acesso.tipo))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar acesso?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao inserir os dados: {erro}')
    finally:
        IDFunc.delete(0, tk.END)
        local.set(registros[0][0])
        tipo.set('Entrada')
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeAcesso(treeAcessos, janelaAcesso)

#--------------------------------------------------------------------------
# CRUD Setor
#--------------------------------------------------------------------------
def attTreeSetor(treeSetor, janelaSetor):       # Atualização TreeView
    # Apaga registros antigos
    for registro in treeSetor.get_children():
        treeSetor.delete(registro)
    try:
        # Select - Locais
        conexao, cursor = abrirConexao()
        comando = '''SELECT * FROM setor WHERE setor_ID != 1;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
        # Coloca novos registros
        for registro in registros:
            treeID = registro[0]
            treeNome = registro[1]
            treeDesc = registro[2]
            treeSetor.insert('', 'end', values=(treeID, treeNome, treeDesc))           
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao exibir os setores: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def verificarUpdateNomeSetor(IDSetor, cursor):
    cursor.execute('SELECT nome_setor FROM setor WHERE setor_ID = ?', (IDSetor, ))
    selectNomeSetorID = cursor.fetchone()[0]
    return selectNomeSetorID

def verificarSetor(IDSetor, cursor):    # Verifica se setor existe
    cursor.execute('SELECT COUNT(*) FROM setor WHERE setor_ID = ?', (IDSetor, ))
    selectID = cursor.fetchone()[0]
    return selectID

def verificarNomeSetor(nomeSetor, cursor):   # Verificar nome do setor repetido
    cursor.execute('SELECT COUNT(*) FROM setor WHERE nome_setor= ?', (nomeSetor, ))
    selectNomeSetor = cursor.fetchone()[0]
    return selectNomeSetor

def insertSetor(nomeSetor, descSetor, treeSetor, janelaSetor):   # Insert tabela Setor
    try:
        conexao, cursor = abrirConexao()
        # Verificação nome do setor vazio
        if nomeSetor.get() == '':
            CTkMessagebox(title='Erro', icon='cancel', message='Nome inválido')
            return
        # Verificação nome do setor
        selectNomeSetor = verificarNomeSetor(nomeSetor.get(), cursor)
        if selectNomeSetor != 0:
            CTkMessagebox(title='Erro', icon='cancel', message='Setor já registrado\nTente outro nome')
            return
        # Instância da classe Setor
        setor = Setor()
        setor.nomeSetor = nomeSetor.get()
        setor.descSetor = descSetor.get()
        # Insert - Setor
        comando = '''INSERT INTO setor (nome_setor, desc_setor) 
                        VALUES (?, ?);'''
        cursor.execute(comando, (setor.nomeSetor, setor.descSetor))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar inserção?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao inserir os dados: {erro}')
    finally:
        nomeSetor.delete(0, tk.END)
        descSetor.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeSetor(treeSetor, janelaSetor)

def updateSetor(IDSetor, nomeSetor, descSetor, treeSetor, janelaSetor):  # Update tabela Setor
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarSetor(IDSetor.get(), cursor)
        if selectID == 0:
            CTkMessagebox(title='Erro', icon='cancel', message='ID inválido')
            return
        # ID admin
        if IDSetor.get() == '1':
            CTkMessagebox(title='Erro', icon='cancel', message='ID inválido')
            return
        # Verificação nome do setor vazio
        if nomeSetor.get() == '':
            CTkMessagebox(title='Erro', icon='cancel', message='Nome inválido')
            return
        # Verificação nome do setor
        selectNomeSetor = verificarNomeSetor(nomeSetor.get(), cursor)
        if selectNomeSetor != 0:
            selectNomeSetorID = verificarUpdateNomeSetor(IDSetor.get(), cursor)
            if selectNomeSetorID != nomeSetor.get():
                CTkMessagebox(title='Erro', icon='cancel', message='Setor já registrado\nTente outro nome')
                return
        # Instância da classe Setor
        setor = Setor()
        setor.IDSetor = IDSetor.get()
        setor.nomeSetor = nomeSetor.get()
        setor.descSetor = descSetor.get()
        # Update - Setor
        comando = '''UPDATE Setor
                        SET nome_setor = (?), desc_setor = (?)
                        WHERE setor_ID = (?);'''
        cursor.execute(comando, (setor.nomeSetor, setor.descSetor, setor.IDSetor))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar Atualização?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao atualizar os dados: {erro}')
    finally:
        nomeSetor.delete(0, tk.END)
        descSetor.delete(0, tk.END)
        IDSetor.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeSetor(treeSetor, janelaSetor)

def deleteSetor(IDSetor, treeSetor, janelaSetor): # Delete tabela setor
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarSetor(IDSetor.get(), cursor)
        if selectID == 0:
            CTkMessagebox(title='Erro', icon='cancel', message='ID inválido')
            return
        # ID admin
        if IDSetor.get() == '1':
            CTkMessagebox(title='Erro', icon='cancel', message='ID inválido')
            return
        # Instância da classe Setor
        setor = Setor()
        setor.IDSetor = IDSetor.get()
        # Delete - Setor
        comando = '''DELETE FROM setor WHERE setor_ID = (?);'''
        cursor.execute(comando, (setor.IDSetor, ))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar Remoção?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback()   
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao remover os dados: {erro}')
    finally:
        IDSetor.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeSetor(treeSetor, janelaSetor)

#--------------------------------------------------------------------------
# CRUD Funcionario
#--------------------------------------------------------------------------
def fillComboboxSetor(janelaFuncionario):    # Preenchimento dos locais
    try:
        conexao, cursor = abrirConexao()
        comando = '''SELECT nome_setor FROM Setor WHERE setor_ID != 1;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao listar os setores: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
    return registros

def attTreeFuncionario(treeFuncionario, janelaFuncionario):       # Atualização TreeView
    # Apaga registros antigos
    for registro in treeFuncionario.get_children():
        treeFuncionario.delete(registro)
    try:
        # Select - Funcionarios
        conexao, cursor = abrirConexao()
        comando = '''SELECT funcionario_ID, nome, email, nome_setor
                    FROM Funcionario
                    LEFT JOIN Setor ON Setor.setor_ID = Funcionario.setor_ID
                    WHERE funcionario_ID != 1;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
        # Coloca novos registros
        for registro in registros:
            treeID = registro[0]
            treeNome = registro[1]
            treeEmail = registro[2]
            treeSetor = registro[3]
            treeFuncionario.insert('', 'end', values=(treeID, treeNome, treeEmail, treeSetor))            
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao exibir os funcionários: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def verificarNomeFuncionario(nomeFuncionario, cursor):   # Verificar nome do funcionario repetido
    cursor.execute('SELECT COUNT(*) FROM funcionario WHERE nome = ?', (nomeFuncionario, ))
    selectNomeFuncionario = cursor.fetchone()[0]
    return selectNomeFuncionario
        
def pegarIDSetor(setor, cursor):    # Pega o ID do setor selecionado
    cursor.execute('SELECT setor_ID FROM Setor WHERE nome_setor = ?', (setor.get(), ))
    selectSetor_ID = cursor.fetchone()[0]
    return selectSetor_ID       

def insertFuncionario(nomeFuncionario, emailFuncionario, setorFuncionario, registros, treeFuncionario, janelaFuncionario):   # Insert tabela Funcionario
    try:
        conexao, cursor = abrirConexao()
        # Verificação de dados do funcionario vazio
        if nomeFuncionario.get() == '':
            CTkMessagebox(title='Erro', icon='cancel', message='Nome vazio')
            return
        
        if setorFuncionario.get() == 'Sem registros':
            CTkMessagebox(title='Erro', icon='cancel', message='Setor não encontrado')
            return
        else:
            selectSetor_ID = pegarIDSetor(setorFuncionario, cursor)
        # Instância da classe Funcionario
        funcionario = Funcionario()
        funcionario.nomeFuncionario = nomeFuncionario.get()
        funcionario.IDSetorFuncionario = setorFuncionario.get()
        funcionario.emailFuncionario = emailFuncionario.get()
        # Insert - Funcionario
        comando = '''INSERT INTO funcionario (nome, setor_ID, email) 
                        VALUES (?, ?, ?);'''
        cursor.execute(comando, (funcionario.nomeFuncionario, selectSetor_ID, funcionario.emailFuncionario))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar inserção?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao inserir os dados: {erro}')
    finally:
        nomeFuncionario.delete(0, tk.END)
        emailFuncionario.delete(0, tk.END)
        setorFuncionario.set(registros[0][0])
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeFuncionario(treeFuncionario, janelaFuncionario)

def updateFuncionario(IDFuncionario, nomeFuncionario, emailFuncionario, setorFuncionario, registros, treeFuncionario, janelaFuncionario):  # Update tabela Funcionario
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectFunc = verificarFuncionario(IDFuncionario.get(), cursor)
        if selectFunc == 0:
            CTkMessagebox(title='Erro', icon='cancel', message='ID inválido')
            return
        # ID admin
        if IDFuncionario.get() == '1':
            CTkMessagebox(title='Erro', icon='cancel', message='ID inválido')
            return
        # Verificação nome e E-mail do funcionario vazio
        if nomeFuncionario.get() == '':
            CTkMessagebox(title='Erro', icon='cancel', message='Nome vazio')
            return
        
        if setorFuncionario.get() == 'Sem registros':
            CTkMessagebox(title='Erro', icon='cancel', message='Setor não encontrado')
            return
        else:
            selectSetor_ID = pegarIDSetor(setorFuncionario, cursor)
        
        # Instância da classe funcionario
        funcionario = Funcionario()
        funcionario.IDFuncionario = IDFuncionario.get()
        funcionario.emailFuncionario = emailFuncionario.get()
        funcionario.nomeFuncionario = nomeFuncionario.get()
        funcionario.IDSetorFuncionario = setorFuncionario.get()

        # Update - Funcionario
        func = (funcionario.nomeFuncionario, funcionario.emailFuncionario, selectSetor_ID, funcionario.IDFuncionario)
        comando = '''UPDATE Funcionario
                        SET nome = (?),
                        email = (?),
                        setor_ID = (?)
                        WHERE funcionario_ID = (?);'''
        cursor.execute(comando, func)
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar Atualização?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao atualizar os dados: {erro}')
    finally:
        IDFuncionario.delete(0, tk.END)
        nomeFuncionario.delete(0, tk.END)
        emailFuncionario.delete(0, tk.END)
        setorFuncionario.set(registros[0][0])
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeFuncionario(treeFuncionario, janelaFuncionario)

def deleteFuncionario(IDFuncionario, treeFuncionario, janelaFuncionario): # Delete tabela Funcionario
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectFunc = verificarFuncionario(IDFuncionario.get(), cursor)
        if selectFunc == 0:
            CTkMessagebox(title='Erro', icon='cancel', message='ID inválido')
            return
        # ID admin
        if IDFuncionario.get() == '1':
            CTkMessagebox(title='Erro', icon='cancel', message='ID inválido')
            return 
        # Instância da classe Funcionario
        funcionario = Funcionario()
        funcionario.IDFuncionario = IDFuncionario.get()
        # Delete - Funcionario
        comando = '''DELETE FROM funcionario WHERE funcionario_ID = (?);'''
        cursor.execute(comando, (funcionario.IDFuncionario, ))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar Remoção?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback() 
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao remover os dados: {erro}')
    finally:
        IDFuncionario.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeFuncionario(treeFuncionario, janelaFuncionario)

#--------------------------------------------------------------------------
# CRUD Usuario
#--------------------------------------------------------------------------
def attTreeUsuario(treeUsuario, janelaUsuario):       # Atualização TreeView
    # Apaga registros antigos
    for registro in treeUsuario.get_children():
        treeUsuario.delete(registro)
    try:
        # Select - Locais
        conexao, cursor = abrirConexao()
        comando = '''SELECT u.usuario_ID, u.nome_usuario, f.nome, u.admin
                        FROM Usuario u
                        JOIN Funcionario f ON u.funcionario_ID = f.funcionario_ID
                        WHERE u.Usuario_ID != 1;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
        # Coloca novos registros
        for registro in registros:
            treeID = registro[0]
            treeNomeUsuario = registro[1]
            treeFuncionario = registro[2]
            treeAdmin = registro[3]
            treeUsuario.insert('', 'end', values=(treeID, treeNomeUsuario, treeFuncionario, treeAdmin))           
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao exibir os usuários: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def registroIDFunc(nomeusu, janelaUsuario):
    try:
        conexao, cursor = abrirConexao()
        cursor.execute('SELECT funcionario_ID FROM Usuario WHERE nome_usuario = ?;', (nomeusu, ))
        idfunc = cursor.fetchone()[0]
        return idfunc
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao inserir os dados: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def switchAdmin(nomeusu, janelaUsuario):
    try:
        conexao, cursor = abrirConexao()
        cursor.execute('SELECT admin FROM Usuario WHERE nome_usuario = ?;', (nomeusu, ))
        switch = cursor.fetchone()[0]
        return switch
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao exibir os dados: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def verificarUpdateNomeUsuario(IDUsuario, cursor):
    cursor.execute('SELECT nome_usuario FROM usuario WHERE usuario_ID = ?', (IDUsuario, ))
    selectNomeUsuID = cursor.fetchone()[0]
    return selectNomeUsuID

def verificarUsuario(IDUsuario, cursor):    # Verifica se usuario existe
    cursor.execute('SELECT COUNT(*) FROM usuario WHERE usuario_ID = ?', (IDUsuario, ))
    selectID = cursor.fetchone()[0]
    return selectID

def verificarNomeUsuario(nomeUsuario, cursor):   # Verificar nome de usuário repetido
    cursor.execute('SELECT COUNT(*) FROM usuario WHERE nome_usuario = ?;', (nomeUsuario, ))
    selectNomeUsuario = cursor.fetchone()[0]
    return selectNomeUsuario

def verificarFuncionarioUsuario(IDFuncionario, cursor): # Verificar se funcionário já tem usuário
    cursor.execute('SELECT COUNT(*) FROM usuario WHERE funcionario_ID = ?;', (IDFuncionario, ))
    selectFuncUsuario = cursor.fetchone()[0]
    return selectFuncUsuario

def insertUsuario(nomeUsuario, senhaUsuario, IDFuncionario, switchAdmin, treeUsuario, janelaUsuario): # Insert tabela Usuario
    try:
        conexao, cursor = abrirConexao()
        # Verificação nome de usuário vazio
        if nomeUsuario.get() == '':
            CTkMessagebox(title='Erro', icon='cancel', message='Nome de usuário inválido')
            return
        # Verificação nome do usuário
        selectNomeUsuario = verificarNomeUsuario(nomeUsuario.get(), cursor)
        if selectNomeUsuario != 0:
            CTkMessagebox(title='Erro', icon='cancel', message='Usuário já registrado\nTente outro nome')
            return
        # Verificação senha vazia
        if senhaUsuario.get() == '':
            CTkMessagebox(title='Erro', icon='cancel', message='Senha inválida')
            return
        # Verificação ID do funcionário vazio
        if IDFuncionario.get() == '':
            CTkMessagebox(title='Erro', icon='cancel', message='ID do funcionário inválido')
            return
        # Verificação Funcionário
        selectFunc = verificarFuncionario(IDFuncionario.get(), cursor)
        if selectFunc == 0:
            CTkMessagebox(title='Erro', icon='cancel', message='Funcionário não encontrado')
            return
        elif IDFuncionario.get() == '1':    # ID admin
            CTkMessagebox(title='Erro', icon='cancel', message='ID do funcionário inválido')
            return 
        else:
            selectFuncUsuario = verificarFuncionarioUsuario(IDFuncionario.get(), cursor)
            if selectFuncUsuario != 0:
                CTkMessagebox(title='Erro', icon='cancel', message='Funcionário já tem um usuário')
                return

        # Hash na senha
        senhaHash = hashlib.sha256(senhaUsuario.get().encode()).hexdigest()

        # Instância da classe Usuário
        usuario = Usuario()
        usuario.nomeUsuario = nomeUsuario.get()
        usuario.senhaUsuario = senhaHash
        usuario.IDFuncionario = IDFuncionario.get()
        usuario.usuAdmin = switchAdmin.get()
        # Insert - Usuario
        comando = '''INSERT INTO usuario (nome_usuario, senha, funcionario_ID, admin) 
                        VALUES (?, ?, ?, ?);'''
        cursor.execute(comando, (usuario.nomeUsuario, usuario.senhaUsuario, usuario.IDFuncionario, usuario.usuAdmin))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar inserção?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao inserir os dados: {erro}')
    finally:
        nomeUsuario.delete(0, tk.END)
        senhaUsuario.delete(0, tk.END)
        IDFuncionario.delete(0, tk.END)
        switchAdmin.deselect()
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeUsuario(treeUsuario, janelaUsuario)

def updateUsuario(IDUsuario, nomeUsuario, senhaUsuario, switchAdmin, treeUsuario, janelaUsuario):  # Update tabela Usuario
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarUsuario(IDUsuario.get(), cursor)
        if selectID == 0:
            CTkMessagebox(title='Erro', icon='cancel', message='ID do usuário inválido')
            return
        # ID admin
        if IDUsuario.get() == '1':
            CTkMessagebox(title='Erro', icon='cancel', message='ID do usuário inválido')
            return 
        # Verificação nome de usuário vazio
        if nomeUsuario.get() == '':
            CTkMessagebox(title='Erro', icon='cancel', message='Nome de usuário inválido')
            return
        # Verificação nome do usuário
        selectNomeUsuario = verificarNomeUsuario(nomeUsuario.get(), cursor)
        if selectNomeUsuario != 0:
            selectNomeUsuID = verificarUpdateNomeUsuario(IDUsuario.get(), cursor)
            if selectNomeUsuID != nomeUsuario.get():
                CTkMessagebox(title='Erro', icon='cancel', message='Usuário já registrado\nTente outro nome')
                return

        # Senha vazia não altera a senha
        if senhaUsuario.get() == '':
            # Instância da classe Usuário
            usuario = Usuario()
            usuario.IDUsuario = IDUsuario.get()
            usuario.nomeUsuario = nomeUsuario.get()
            usuario.usuAdmin = switchAdmin.get()
            # Update - Usuário
            comando = '''UPDATE Usuario
                            SET nome_usuario = (?), admin = (?)
                            WHERE usuario_ID = (?);'''
            cursor.execute(comando, (usuario.nomeUsuario, usuario.usuAdmin, usuario.IDUsuario))
            # Messagebox - Confirmação
            msg = CTkMessagebox(title='Confirmação', message='Confirmar Atualização?', icon='question', option_1='Não', option_3='Sim')
            resposta = msg.get()
            if resposta=='Sim':
                conexao.commit()
            else:
                conexao.rollback()

        # Senha não vazia altera a senha
        else:
            # Hash na senha
            senhaHash = hashlib.sha256(senhaUsuario.get().encode()).hexdigest()

            # Instância da classe Usuário
            usuario = Usuario()
            usuario.IDUsuario = IDUsuario.get()
            usuario.nomeUsuario = nomeUsuario.get()
            usuario.senhaUsuario = senhaHash
            usuario.usuAdmin = switchAdmin.get()
            # Update - Usuário
            comando = '''UPDATE Usuario
                            SET nome_usuario = (?), senha = (?), admin = (?)
                            WHERE usuario_ID = (?);'''
            cursor.execute(comando, (usuario.nomeUsuario, usuario.senhaUsuario, usuario.usuAdmin, usuario.IDUsuario))
            # Messagebox - Confirmação
            msg = CTkMessagebox(title='Confirmação', message='Confirmar Atualização?', icon='question', option_1='Não', option_3='Sim')
            resposta = msg.get()
            if resposta=='Sim':
                conexao.commit()
            else:
                conexao.rollback()
                
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao atualizar os dados: {erro}')
    finally:
        IDUsuario.delete(0, tk.END)
        nomeUsuario.delete(0, tk.END)
        senhaUsuario.delete(0, tk.END)
        switchAdmin.deselect()
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeUsuario(treeUsuario, janelaUsuario)

def deleteUsuario(IDUsuario, treeUsuario, janelaUsuario): # Delete tabela Usuario
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarUsuario(IDUsuario.get(), cursor)
        if selectID == 0:
            CTkMessagebox(title='Erro', icon='cancel', message='ID do usuário inválido')
            return
        # ID admin
        if IDUsuario.get() == '1':
            CTkMessagebox(title='Erro', icon='cancel', message='ID do usuário inválido')
            return 
        # Instância da classe Usuario
        usuario = Usuario()
        usuario.IDUsuario = IDUsuario.get()
        # Delete - Usuario
        comando = '''DELETE FROM Usuario WHERE usuario_ID = (?);'''
        cursor.execute(comando, (usuario.IDUsuario, ))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar Remoção?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback() 
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao remover os dados: {erro}')
    finally:
        IDUsuario.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeUsuario(treeUsuario, janelaUsuario)        

#--------------------------------------------------------------------------
# CRUD Local
#--------------------------------------------------------------------------
def attTreeLocal(treeLocal, janelaLocal):       # Atualização TreeView
    # Apaga registros antigos
    for registro in treeLocal.get_children():
        treeLocal.delete(registro)
    try:
        # Select - Locais
        conexao, cursor = abrirConexao()
        comando = '''SELECT * FROM local;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
        # Coloca novos registros
        for registro in registros:
            treeID = registro[0]
            treeNome = registro[1]
            treeLocal.insert('', 'end', values=(treeID, treeNome))            
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao exibir os locais: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def verificarLocal(IDlocal, cursor):    # Verifica se local existe
    cursor.execute('SELECT COUNT(*) FROM local WHERE local_ID = ?', (IDlocal, ))
    selectID = cursor.fetchone()[0]
    return selectID

def verificarNomeLocal(nomeLocal, cursor):   # Verificar nome do local repetido
    cursor.execute('SELECT COUNT(*) FROM local WHERE nome_local= ?', (nomeLocal, ))
    selectNomeLocal = cursor.fetchone()[0]
    return selectNomeLocal

def insertLocal(nomeLocal, treeLocal, janelaLocal):   # Insert tabela Local
    try:
        conexao, cursor = abrirConexao()
        # Verificação nome do local vazio
        if nomeLocal.get() == '':
            CTkMessagebox(title='Erro', icon='cancel', message='Nome inválido')
            return
        # Verificação nome do local
        selectNomeLocal = verificarNomeLocal(nomeLocal.get(), cursor)
        if selectNomeLocal != 0:
            CTkMessagebox(title='Erro', icon='cancel', message='Local já registrado\nTente outro nome')
            return
        # Instância da classe Local
        local = Local()
        local.nomeLocal = nomeLocal.get()
        # Insert - Local
        comando = '''INSERT INTO local (nome_local) 
                        VALUES (?);'''
        cursor.execute(comando, (local.nomeLocal, ))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar inserção?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao inserir os dados: {erro}')
    finally:
        nomeLocal.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeLocal(treeLocal, janelaLocal)

def updateLocal(IDLocal, nomeLocal, treeLocal, janelaLocal):  # Update tabela Local
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarLocal(IDLocal.get(), cursor)
        if selectID == 0:
            CTkMessagebox(title='Erro', icon='cancel', message='ID inválido')
            return
        # Verificação nome do local vazio
        if nomeLocal.get() == '':
            CTkMessagebox(title='Erro', icon='cancel', message='Nome inválido')
            return
        # Verificação nome do local
        selectNomeLocal = verificarNomeLocal(nomeLocal.get(), cursor)
        if selectNomeLocal != 0:
            CTkMessagebox(title='Erro', icon='cancel', message='Local já registrado\nTente outro nome')
            return
        # Instância da classe Local
        local = Local()
        local.IDLocal = IDLocal.get()
        local.nomeLocal = nomeLocal.get()
        # Update - Local
        comando = '''UPDATE Local
                        SET nome_local = (?)
                        WHERE local_ID = (?);'''
        cursor.execute(comando, (local.nomeLocal, local.IDLocal))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar Atualização?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao atualizar os dados: {erro}')
    finally:
        nomeLocal.delete(0, tk.END)
        IDLocal.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeLocal(treeLocal, janelaLocal)

def deleteLocal(IDLocal, treeLocal, janelaLocal): # Delete tabela Local
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarLocal(IDLocal.get(), cursor)
        if selectID == 0:
            CTkMessagebox(title='Erro', icon='cancel', message='ID inválido')
            return
        # Instância da classe Local
        local = Local()
        local.IDLocal = IDLocal.get()
        # Delete - Local
        comando = '''DELETE FROM Local WHERE local_ID = (?);'''
        cursor.execute(comando, (local.IDLocal, ))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar Remoção?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
        else:
            conexao.rollback()  
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao remover os dados: {erro}')
    finally:
        IDLocal.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeLocal(treeLocal, janelaLocal)

#--------------------------------------------------------------------------
# Main - Login
#--------------------------------------------------------------------------
def verificarLgnUsuario(lgnUsuario, cursor):    # Verifica Login Usuario
    cursor.execute('SELECT COUNT(*) FROM usuario WHERE nome_usuario = ?', (lgnUsuario, ))
    selectLgnUsuario = cursor.fetchone()[0]
    return selectLgnUsuario

def verificarLgnSenha(lgnUsuario, cursor):    # Verifica Login Senha
    cursor.execute('SELECT senha FROM usuario WHERE nome_usuario = ?', (lgnUsuario, ))
    selectLgnSenha = cursor.fetchone()[0]
    return selectLgnSenha

def nivel(lgnUsuario):  # Nível
    try:
        conexao, cursor = abrirConexao()
        comando = '''SELECT u.nome_usuario, s.nome_setor, u.admin
                        FROM Usuario u
                        JOIN Funcionario f ON u.funcionario_ID = f.funcionario_ID
                        JOIN Setor s ON f.setor_ID = s.setor_ID
                        WHERE nome_usuario = ?;'''
        cursor.execute(comando, (lgnUsuario.get(), ))
        nvl = cursor.fetchone()
        return nvl

    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao criar as tabelas: {erro}')
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor) 

def entrar(lgnUsuario, lgnSenha, janelaMain):   # Login
    try:
        conexao, cursor = abrirConexao()

        # Hash na senha
        senhaHash = hashlib.sha256(lgnSenha.get().encode()).hexdigest()

        # Instância da classe Login
        login = Login(lgnUsuario.get(), senhaHash)

        # Verificação Login
        selectLgnUsuario = verificarLgnUsuario(login.lgnUsuario, cursor)
        if selectLgnUsuario == 0:
            CTkMessagebox(title='Erro', icon='cancel', message='Usuário e/ou senha inválidos')
            lgnUsuario.delete(0, tk.END)
            lgnSenha.delete(0, tk.END)
            return
        else:
            selectLgnSenha = verificarLgnSenha(login.lgnUsuario, cursor)
            if selectLgnSenha != login.lgnSenha:
                CTkMessagebox(title='Erro', icon='cancel', message='Usuário e/ou senha inválidos')
                lgnUsuario.delete(0, tk.END)
                lgnSenha.delete(0, tk.END)
                return     
        # Níveis
        nvl = nivel(lgnUsuario)
        lgnUsuario.delete(0, tk.END)
        lgnSenha.delete(0, tk.END)
        if nvl[1] == 'Administrador' or nvl[2] == 'Sim':
            menuAdmin.menuAdmin(nvl, janelaMain)
        else:
            acesso.acesso(nvl, janelaMain)
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao se conectar com o banco de dados: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

#--------------------------------------------------------------------------
# Usuário troca a senha
#--------------------------------------------------------------------------
def verificarSenhaAtual(nvl, cursor):    # Verifica Senha Atual
    cursor.execute('SELECT senha FROM usuario WHERE nome_usuario = ?', (nvl[0], ))
    selectSenhaAtual = cursor.fetchone()[0]
    return selectSenhaAtual

def trocarSenha(nvl, entrySenhaAtual, entryNovaSenha, janelaTrocaSenha):
    try:
        conexao, cursor = abrirConexao()
        
        senhaAtual = verificarSenhaAtual(nvl, cursor)
        entrySenhaAtual = hashlib.sha256(entrySenhaAtual.get().encode()).hexdigest()
        if entrySenhaAtual != senhaAtual:
            CTkMessagebox(title='Erro', icon='cancel', message='Senha atual inválida')
            return
        if entryNovaSenha.get() == '':
            CTkMessagebox(title='Erro', icon='cancel', message='Nova senha inválida')
            return

        entryNovaSenha = hashlib.sha256(entryNovaSenha.get().encode()).hexdigest()

        # Instância da classe Usuário
        usuario = Usuario()
        usuario.nomeUsuario = nvl[0]
        usuario.senhaUsuario = entryNovaSenha
        # Update - Usuário
        comando = '''UPDATE Usuario
                        SET senha = (?)
                        WHERE nome_usuario = (?);'''
        cursor.execute(comando, (usuario.senhaUsuario ,usuario.nomeUsuario))
        # Messagebox - Confirmação
        msg = CTkMessagebox(title='Confirmação', message='Confirmar Alteração?', icon='question', option_1='Não', option_3='Sim')
        resposta = msg.get()
        if resposta=='Sim':
            conexao.commit()
            CTkMessagebox(title='Senha Alterada', icon='check', message='Senha alterada com sucesso')
            janelaTrocaSenha.destroy()
        else:
            conexao.rollback()
    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao alterar a senha: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

#--------------------------------------------------------------------------
# Tabelas
#--------------------------------------------------------------------------
def tabelas():  # Criação das tabelas (caso não exista)
    try:
        conexao, cursor = abrirConexao()
        # Setor
        comando = '''CREATE TABLE IF NOT EXISTS "Setor" (
                        "setor_ID" INTEGER NOT NULL,
                        "nome_setor" VARCHAR(50) NOT NULL UNIQUE,
                        "desc_setor" VARCHAR(255),
                        PRIMARY KEY("setor_ID" AUTOINCREMENT)
                    );'''
        cursor.execute(comando, )
        conexao.commit()

        # Funcionário
        comando = '''CREATE TABLE IF NOT EXISTS "Funcionario" (
	                    "funcionario_ID" INTEGER NOT NULL,
	                    "nome"	VARCHAR(50) NOT NULL,
	                    "email"	VARCHAR(100),
	                    "setor_ID" INTEGER NOT NULL,
	                    PRIMARY KEY("funcionario_ID" AUTOINCREMENT),
	                    FOREIGN KEY("setor_ID") REFERENCES "Setor"("setor_ID")
                    );'''
        cursor.execute(comando, )
        conexao.commit()

        # Usuario
        comando = '''CREATE TABLE IF NOT EXISTS "Usuario" (
	                    "usuario_ID" INTEGER NOT NULL,
	                    "nome_usuario" VARCHAR(50) NOT NULL UNIQUE,
	                    "senha" TEXT NOT NULL,
	                    "funcionario_ID" INTEGER NOT NULL,
                        "admin"	TEXT NOT NULL,
	                    PRIMARY KEY("usuario_ID" AUTOINCREMENT)
	                    FOREIGN KEY("funcionario_ID") REFERENCES "Funcionario"("funcionario_ID") ON DELETE CASCADE
                    );'''
        cursor.execute(comando, )
        conexao.commit()

        # Local
        comando = '''CREATE TABLE IF NOT EXISTS "Local" (
                        "local_ID" INTEGER NOT NULL,
                        "nome_local" VARCHAR(50) NOT NULL UNIQUE,
                        PRIMARY KEY("local_ID" AUTOINCREMENT)
                    );'''
        cursor.execute(comando, )
        conexao.commit()

        # Acesso
        comando = '''CREATE TABLE IF NOT EXISTS "Acesso" (
                        "data_hora" DATETIME DEFAULT (datetime('now', 'localtime')),
                        "tipo"	VARCHAR(7) NOT NULL,
                        "funcionario_ID" INTEGER NOT NULL,
                        "local_ID" INTEGER NOT NULL,
                        FOREIGN KEY("local_ID") REFERENCES "Local"("local_ID"),
                        FOREIGN KEY("funcionario_ID") REFERENCES "Funcionario"("funcionario_ID"),
                        PRIMARY KEY("data_hora","funcionario_ID","local_ID")
                    );'''
        cursor.execute(comando, )
        conexao.commit()

        # Usuário admin
        comando = '''SELECT COUNT(*) FROM setor;'''
        cursor.execute(comando, )
        slctSetor = cursor.fetchone()[0]

        comando = '''SELECT COUNT(*) FROM funcionario;'''
        cursor.execute(comando, )
        slctFunc = cursor.fetchone()[0]

        comando = '''SELECT COUNT(*) FROM Usuario;'''
        cursor.execute(comando, )
        slctUsu = cursor.fetchone()[0]

        if slctSetor == 0 and slctFunc == 0 and slctUsu == 0:
            comando = '''INSERT INTO Setor (nome_setor, desc_setor) 
                            VALUES ('Administrador', 'Usuário Administrador');'''
            cursor.execute(comando, )

            comando = '''INSERT INTO Funcionario (nome, setor_ID) 
                            VALUES ('Administrador', 1);'''
            cursor.execute(comando, )

            senhaAdmin = 'admin'
            senhaHash = hashlib.sha256(senhaAdmin.encode()).hexdigest()
            comando = '''INSERT INTO Usuario (nome_usuario, senha, funcionario_ID, admin) 
                            VALUES ('admin', ?, 1, 'Sim');'''
            cursor.execute(comando, (senhaHash, ))
            
            conexao.commit()

    except conector.Error as erro:
        CTkMessagebox(title='Erro', icon='cancel', message=f'Erro ao criar as tabelas: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
            
