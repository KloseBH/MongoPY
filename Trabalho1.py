import tkinter as tk
from pymongo import MongoClient
from tkinter import messagebox

# Configuração do MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
except pymongo.errors.ConnectionFailure:
    messagebox.showerror("Erro", "Erro de conexão com o MongoDB. Verifique se o servidor está em execução.")
db = client["trabalho1"]  # Substitua pelo nome do seu banco de dados
colecao = db["usuarios"]  # Substitua pelo nome da sua coleção

#==========================================================================================================

# Fonte padrão para os widgets
fonte_padrao = ("Arial", 12)

# Estilo para botões
botoes_estilo = {
    "bg": "#28a745",  # Cor de fundo (verde)
    "fg": "white",  # Cor do texto (branco)
    "font": fonte_padrao,
    "relief": "raised",  # Estilo de borda elevada
    "width": 30,  # Largura do botão
    "height": 2,  # Altura do botão
}

botoes_estilo_vermelho = {
    "bg": "#dc3545",  # Cor de fundo (vermelho)
    "fg": "white",  # Cor do texto (branco)
    "font": fonte_padrao,
    "relief": "raised",  # Estilo de borda elevada
    "width": 30,  # Largura do botão
    "height": 2,  # Altura do botão
}

# Configuração de estilo para os campos de entrada
estilo_entry = {
    "font": fonte_padrao,  # Fonte definida anteriormente
    "bg": "#f0f0f0",  # Cor de fundo (cinza claro)
    "fg": "#000000",  # Cor da fonte (preta)
    "relief": "solid",  # Estilo de borda sólida
}

#==========================================================================================================

# Função para imprimir a mensagem de apresentação
def imprimir_mensagem_apresentacao():
    mensagem = "Trabalho 1 de Banco de Dados NoSQL\nFeito por DANIEL HENRIQUE ALVES BICALHO DIAS"
    janela_mensagem = tk.Toplevel()
    janela_mensagem.title("Apresentação")
    tk.Label(janela_mensagem, text=mensagem, font=("Arial", 12)).pack(padx=20, pady=20)
    tk.Button(janela_mensagem, text="OK", command=janela_mensagem.destroy, **botoes_estilo).pack(pady=10)

#==========================================================================================================

# Funções para exibir menus
def exibir_menu_principal():
    menu_principal.deiconify()

def exibir_menu_cadastro():
    menu_cadastro.deiconify()

def exibir_menu_consulta():
    menu_consulta.deiconify()

def exibir_menu_atualizacao():
    menu_atualizacao.deiconify()

def exibir_menu_exclusao():
    menu_exclusao.deiconify()

# Funções para fechar menus 
def fechar_menu_cadastro():
    menu_cadastro.withdraw()

def fechar_menu_consulta():
    menu_consulta.withdraw()

def fechar_menu_atualizacao():
    menu_atualizacao.withdraw()

def fechar_menu_exclusao():
    menu_exclusao.withdraw()

#==========================================================================================================

#CADASTRO
def confirmar_envio():
    # Função para confirmar o envio dos dados
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    CPF = entry_cpf.get()
    
    # Verifique se os campos obrigatórios não estão vazios
    if not (nome and email and telefone and CPF):
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos obrigatórios.")
        return
        
    if (colecao.find_one({"_id": CPF})):
        messagebox.showerror("Erro", "CPF já cadastrado!!!")
        entry_nome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        return
    
    # Salvando no banco
    documento = {
        "_id": CPF,
        "nome": nome,
        "email": email,
        "telefone": telefone
    }
    
    try:
        colecao.insert_one(documento)
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso.")
    except pymongo.errors.DuplicateKeyError:
        messagebox.showerror("Erro", "Erro: CPF já existe no banco de dados")
            
    
    # Limpa os campos de entrada após confirmar o envio
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)

#==========================================================================================================

#CONSULTA
def buscar():
    CPF = entry_consulta.get()
    
    # Verifique se os campos obrigatórios não estão vazios
    if not (CPF):
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos obrigatórios.")
        return
    
    # Puxar do banco de dados
    resultado = colecao.find_one({"_id": CPF})
    
    mostrarBusca(resultado)
    
    # Limpa os campos de entrada após confirmar a colsulta
    entry_consulta.delete(0, tk.END)
    
def mostrarBusca(resultado):
    # Cria uma nova janela para exibir o resultado
    janela_resultado = tk.Toplevel()
    janela_resultado.title("Resultado da Consulta")

    if resultado:
        # Exibe os dados do documento em Labels na janela de resultado
        tk.Label(janela_resultado, text="Resultado encontrado:", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Exibindo os dados do documento
        tk.Label(janela_resultado, text=f"Nome: {resultado.get('nome', 'N/A')}").pack(pady=5)
        tk.Label(janela_resultado, text=f"CPF: {resultado.get('_id', 'N/A')}").pack(pady=5)
        tk.Label(janela_resultado, text=f"E-mail: {resultado.get('email', 'N/A')}").pack(pady=5)
        tk.Label(janela_resultado, text=f"Telefone: {resultado.get('telefone', 'N/A')}").pack(pady=5)
        
    else:
        # Se não houver resultado, exibe uma mensagem informando isso
        tk.Label(janela_resultado, text="Nenhum resultado encontrado", font=("Arial", 12, "bold")).pack(pady=10)
    
    # Botão para fechar a janela de resultado
    tk.Button(janela_resultado, text="Fechar", command=janela_resultado.destroy, **botoes_estilo_vermelho).pack(pady=10)

    
def exibir_consulta_geral():
    # Função para verificar todos os usuários e seus IDs (CPF)
    try:
        todos = colecao.find()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao consultar usuários: {e}")
        return
    
    # Cria uma nova janela para exibir todos os usuários
    janela_todos = tk.Toplevel()
    janela_todos.title("Todos os Usuários")

    for usuario in todos:
        try:
            # Verifica se o documento tem os campos 'nome' e '_id' (CPF)
            nome = usuario.get('nome', 'N/A')
            cpf = usuario.get('_id', 'N/A')
            
            # Cria um rótulo para exibir o nome e CPF do usuário
            tk.Label(janela_todos, text=f"Nome: {nome} - CPF: {cpf}").pack(pady=5)
        
        except KeyError as e:
            messagebox.showerror("Erro", f"Erro ao acessar um campo no documento: {e}")
    
    # Adiciona um botão para fechar a janela
    tk.Button(janela_todos, text="Fechar", command=janela_todos.destroy, **botoes_estilo_vermelho).pack(pady=10)

        

#==========================================================================================================

#ATUALIZAÇÃO
def atualizar():
    # Função para realizar a atualização
    CPF = entry_atualizacao_cpf.get()
    nome = entry_atualizacao_nome.get()
    email = entry_atualizacao_email.get()
    telefone = entry_atualizacao_telefone.get()
    
    # Verifique se os campos obrigatórios não estão vazios
    if not (CPF):
        messagebox.showwarning("Aviso", "Por favor, preencha o CPF.")
        return
   
    # Verifica se o CPF existe no banco de dados
    resultado = colecao.find_one({"_id": CPF})
    
    # Atualizando o Banco de dados
    if resultado:
        if not (nome):
            nome = resultado.get("nome")
        if not (email):
            email = resultado.get("email")
        if not (telefone):
            telefone = resultado.get("telefone")
        colecao.update_one(
            {"_id": CPF},
            {"$set": {
                "nome": nome,
                "email": email,
                "telefone": telefone
            }}
        )
        messagebox.showinfo("Sucesso", "Atualização realizada com sucesso.")
    else:
        messagebox.showerror("Erro", "CPF não encontrado no banco de dados.")

    # Limpa os campos de entrada após confirmar a atualização
    entry_atualizacao_nome.delete(0, tk.END)
    entry_atualizacao_email.delete(0, tk.END)
    entry_atualizacao_telefone.delete(0, tk.END)
    entry_atualizacao_cpf.delete(0, tk.END)

#==========================================================================================================

#EXCLUSÃO
def excluir():
    # Função para realizar a exclusão
    CPF = entry_exclusao.get()
    
    # Verifique se os campos obrigatórios não estão vazios
    if not (CPF):
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos obrigatórios.")
        return
    
    # Verifica se o CPF existe no banco de dados
    resultado = colecao.find_one({"_id": CPF})
    
    # Exclui no Banco de dados
    if resultado:
        colecao.delete_one({"_id": CPF})
        messagebox.showinfo("Sucesso", "Exclusão realizada com sucesso.")
    else:
        messagebox.showerror("Erro", "CPF não encontrado no banco de dados.")

    # Limpa o campo de entrada após confirmar a exclusão
    entry_exclusao.delete(0, tk.END)

#==========================================================================================================

# Criação da interface
app = tk.Tk()
app.title("TRABALHO 1")
app.geometry("300x400")

# Menu principal
menu_principal = tk.Frame(app)
tk.Label(menu_principal, text="MENU PRINCIPAL", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(menu_principal, text="Cadastro", command=exibir_menu_cadastro, **botoes_estilo).pack(pady=5)
tk.Button(menu_principal, text="Consulta", command=exibir_menu_consulta, **botoes_estilo).pack(pady=5)
tk.Button(menu_principal, text="Atualização", command=exibir_menu_atualizacao, **botoes_estilo).pack(pady=5)
tk.Button(menu_principal, text="Exclusão", command=exibir_menu_exclusao, **botoes_estilo).pack(pady=5)
tk.Button(menu_principal, text="Consulta Geral", command=exibir_consulta_geral, **botoes_estilo).pack(pady=5)
tk.Button(menu_principal, text="Sair", command=app.quit, **botoes_estilo_vermelho).pack(pady=5)
menu_principal.pack()

#==========================================================================================================

# Menu de cadastro
menu_cadastro = tk.Toplevel(app)
menu_cadastro.title("CADASTRO")
menu_cadastro.geometry("300x375")
menu_cadastro.withdraw()  # Começa fechado

# Rótulo principal
tk.Label(menu_cadastro, text="CADASTRO:", font=("Arial", 12, "bold")).pack(pady=5)

# Campo de entrada para o nome
tk.Label(menu_cadastro, text="Nome:").pack()
entry_nome = tk.Entry(menu_cadastro, **estilo_entry)
entry_nome.pack(pady=5)

# Campo de entrada para o CPF
tk.Label(menu_cadastro, text="CPF:").pack()
entry_cpf = tk.Entry(menu_cadastro, **estilo_entry)
entry_cpf.pack(pady=5)

# Campo de entrada para o e-mail
tk.Label(menu_cadastro, text="E-mail:").pack()
entry_email = tk.Entry(menu_cadastro, **estilo_entry)
entry_email.pack(pady=5)

# Campo de entrada para o telefone
tk.Label(menu_cadastro, text="Telefone:").pack()
entry_telefone = tk.Entry(menu_cadastro, **estilo_entry)
entry_telefone.pack(pady=5)

# Botão para confirmar o envio
botao_confirmar = tk.Button(menu_cadastro, text="Confirmar Envio", command=confirmar_envio, **botoes_estilo)
botao_confirmar.pack(pady=10)

# Botão para fechar
botao_fechar = tk.Button(menu_cadastro, text="Fechar", command=fechar_menu_cadastro, **botoes_estilo_vermelho)
botao_fechar.pack(pady=5)

#===========================================================================================================

# Menu de consulta
menu_consulta = tk.Toplevel(app)
menu_consulta.title("CONSULTA")
menu_consulta.geometry("300x250")
menu_consulta.withdraw()

# Rótulo Principal
tk.Label(menu_consulta, text="CONSULTA:", font=("Arial", 12, "bold")).pack(pady=5)

# Campo de entrada
tk.Label(menu_consulta, text="Buscar por CPF:").pack()
entry_consulta = tk.Entry(menu_consulta, **estilo_entry)
entry_consulta.pack(pady=5)

# Botão para realizar
botão_buscar = tk.Button(menu_consulta, text="Buscar", command=buscar, **botoes_estilo)
botão_buscar.pack(pady=10)

# Botão para fechar
botão_fechar_consulta = tk.Button(menu_consulta, text="Fechar", command=fechar_menu_consulta, **botoes_estilo_vermelho)
botão_fechar_consulta.pack(pady=5)

#==========================================================================================================

# Menu de atualização
menu_atualizacao = tk.Toplevel(app)
menu_atualizacao.title("ATUALIZAÇÃO")
menu_atualizacao.geometry("300x375")
menu_atualizacao.withdraw()

# Rótulo Principal
tk.Label(menu_atualizacao, text="ATUALIZAÇÃO:", font=("Arial", 12, "bold")).pack(pady=5)

# Campo de entrada para o CPF
tk.Label(menu_atualizacao, text="CPF(ID Unico):").pack()
entry_atualizacao_cpf = tk.Entry(menu_atualizacao, **estilo_entry)
entry_atualizacao_cpf.pack(pady=5)

# Campo de entrada para o nome
tk.Label(menu_atualizacao, text="Nome:").pack()
entry_atualizacao_nome = tk.Entry(menu_atualizacao, **estilo_entry)
entry_atualizacao_nome.pack(pady=5)

# Campo de entrada para o e-mail
tk.Label(menu_atualizacao, text="E-mail:").pack()
entry_atualizacao_email = tk.Entry(menu_atualizacao, **estilo_entry)
entry_atualizacao_email.pack(pady=5)

# Campo de entrada para o telefone
tk.Label(menu_atualizacao, text="Telefone:").pack()
entry_atualizacao_telefone = tk.Entry(menu_atualizacao, **estilo_entry)
entry_atualizacao_telefone.pack(pady=5)

# Botão para confirmar
botão_atualizar = tk.Button(menu_atualizacao, text="Confirmar Atualização", command=atualizar, **botoes_estilo)
botão_atualizar.pack(pady=10)

# Botão para fechar
botão_fechar_atualizacao = tk.Button(menu_atualizacao, text="Fechar", command=fechar_menu_atualizacao, **botoes_estilo_vermelho)
botão_fechar_atualizacao.pack(pady=5)

#==========================================================================================================

# Menu de exclusão
menu_exclusao = tk.Toplevel(app)
menu_exclusao.title("EXCLUSÃO")
menu_exclusao.geometry("300x250")
menu_exclusao.withdraw()  # Começa fechado

# Rótulo principal
tk.Label(menu_exclusao, text="EXCLUSÃO:", font=("Arial", 12, "bold")).pack(pady=5)

# Campo de entrada
tk.Label(menu_exclusao, text="Excluir por CPF:").pack()
entry_exclusao = tk.Entry(menu_exclusao, **estilo_entry)
entry_exclusao.pack(pady=5)

# Botão para confirmar
botão_excluir = tk.Button(menu_exclusao, text="Excluir", command=excluir, **botoes_estilo)
botão_excluir.pack(pady=10)

# Botão para fechar
botão_fechar_exclusao = tk.Button(menu_exclusao, text="Fechar", command=fechar_menu_exclusao, **botoes_estilo_vermelho)
botão_fechar_exclusao.pack(pady=5)

#=========================================================================================================

# Chamada da função de apresentação
imprimir_mensagem_apresentacao()

# Executa o loop principal da aplicação
app.mainloop()