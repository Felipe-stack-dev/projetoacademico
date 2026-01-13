from colorama import Fore, Style
import pyfiglet
import os
from rich.console import Console
from rich.table import Table
from hashlib import sha256
import json
from datetime import datetime
import pwinput

# FUNCOES
def LimparTela():
    os.system('cls')

def CriptografarSenha(senha):
    salt = "6100"
    senha_com_salt = senha+salt
    hash_senha = sha256(senha_com_salt.encode()).hexdigest()
    return hash_senha

def verificar_Senha(senha_digitada, hash_armazenado):
    hash_digitado = CriptografarSenha(senha_digitada)
    return hash_digitado == hash_armazenado

def SalvarMensagem(mensagem):
    try:
        with open("Mensagens.json", "r") as arq:
            mensagens = json.load(arq)
    except FileNotFoundError:
        mensagens = []
    mensagens.append(mensagem)

    with open("Mensagens.json", "w") as arq:
        json.dump(mensagens, arq, indent=4)

def BuscarMensagensParaUsuario(email_usuario):
    try:
        with open("Mensagens.json", "r") as arq:
            mensagens = json.load(arq)
    except FileNotFoundError:
        return []
    
    # Filtrar mensagens para o usuário (já criptografado)
    email_cript = Criptografar(cifra, email_usuario)
    mensagens_usuario = [
        m for m in mensagens if m['destinatario'] == email_cript]
    return mensagens_usuario

def Criptografar(cifra, string):
    a = ""
    for i in string:
        a += cifra.get(i.lower(), i)
    return a

def Decriptografar(cifra, string):
    a = ""
    for i in string:
        for w in cifra:
            if cifra.get(w, "") == i.lower():
                a += w
    return a

# MENU
cifra = {"a": "d", "b": "e", "c": "f", "d": "g", "e": "h", "f": "i", "g": "j", "h": "k", "i": "l",
         "j": "m", "k": "n", "l": "o", "m": "p", "n": "q", "o": "r", "p": "s", "q": "t", "r": "u",
         "s": "v", "t": "w", "u": "x", "v": "y", "w": "z", "x": "a", "y": "b", "z": "c", " ": " ",
         "?": "!", ":": "?", "!": ":", "0": "5", "1": "6", "2": "7", "3": "8", "4": "9", "5": "0",
         "6": "1", "7": "2", "8": "3", "9": "4","/":"*"}
with open("Usuarios.json", "r") as arquivo:
    listaUsuarios = json.load(arquivo)
while 1:
    LimparTela()
    print(Fore.LIGHTMAGENTA_EX + pyfiglet.figlet_format("Comunicação Criptografada"))
    titulo = "Sistema de Transmissão de Mensagens Criptografadas:"
    print(Fore.BLUE + titulo)
    print(Style.RESET_ALL + '--MENU PRINCIPAL--')
    print("Selecione uma opção:")
    op = int(input("1-Login\n0-Sair\n"))
    LimparTela()
    match op:
        case 1:
            print("Login:")
            login_user = input("Email: ")
            login_senha = pwinput.pwinput(prompt="Senha: ", mask='*')
            i = 0
            for u in listaUsuarios:
                if (u['email']) == login_user:
                    if (verificar_Senha(login_senha, u['password'])):
                       # MENU DE ADMIN
                        if (u['userType'] == "admin"):
                            while(op!=0):
                                LimparTela()
                                print(Style.RESET_ALL + '--MENU ADMINISTRADOR--')
                                print("Selecione uma opção:")
                                op = int(
                                    input("1-Cadastrar novo Usuário\n2-Excluir Usuário\n0-Sair\n"))
                                match op:
                                    # CADASTRO DE USUARIO
                                    case 1:
                                        LimparTela()
                                        print("Cadastro de Novo Usuário: \n")
                                        email = input("Email: ")
                                        v = 0
                                        while v < len(listaUsuarios):
                                            for u in listaUsuarios:
                                                if (u['email'] == email):
                                                    print("email já cadastrado!!")
                                                    print(
                                                        "Insira um email não cadastrado!")
                                                    os.system("pause")
                                                    LimparTela()
                                                    print(
                                                        "Cadastro de Novo Usuário: \n")
                                                    email = input("Email: ")
                                            v += 1
                                        dados_usuario = {"username": input("Nome do usuário: "),
                                                        "password": CriptografarSenha(pwinput.pwinput(prompt="Senha: ", mask='*')),
                                                        "userType": input("Tipo de usuário (admin/user): "),
                                                        "email": email}
                                        listaUsuarios.append(dados_usuario)
                                        json_string = json.dumps(
                                            listaUsuarios, indent=4)
                                        with open("Usuarios.json", "w") as arquivousuarios:
                                            arquivousuarios.write(json_string)
                                            print("dados salvos")
                                            os.system('pause')
                                    case 2:
                                        LimparTela()
                                        print("Tela de Exclusão de Usuário:")
                                        exc_email = input("Email: ")
                                        index = 0
                                        for u in listaUsuarios:
                                            if (u["email"] == exc_email):
                                                op = int(input(
                                                    "Tem certeza que deseja excluir o usuário "+u["username"]+" (1-Sim/0-Não)?\n"))
                                                match op:
                                                    case 1:
                                                        listaUsuarios.pop(index)
                                                        json_string = json.dumps(
                                                            listaUsuarios, indent=4)
                                                        with open("Usuarios.json", "w") as arquivousuarios:
                                                            arquivousuarios.write(
                                                                json_string)
                                                            print(
                                                                "Usuário deletado!")
                                                    case 0:
                                                        break
                                            else:
                                                index += 1
                                    case 0:
                                        print("Saindo...")
                                        break
                        # MENU DE USUARIO
                        elif (u['userType'] == "user"):
                            while(op!=0):
                                LimparTela()
                                print(Style.RESET_ALL + '--MENU USUÁRIO--')
                                print("Selecione uma opção:")
                                op = int(input(
                                    "1-Enviar mensagem\n2-Decriptografar Mensagem\n3-Configurações de criptografia\n4-Alterar senha\n0-Sair\n"))
                                match op:
                                    #Opção para enviar mensagem
                                    case 1:
                                        a = 0
                                        i = 0
                                        while (a != 1):
                                            LimparTela()
                                            print("Envio de Mensagem:\n")

                                            console = Console()
                                            table = Table(title="Usuários")
                                            table.add_column(
                                                "Usuario", justify="left", style="cyan")
                                            table.add_column(
                                                "Email", justify="left", style="cyan")
                                            table.add_column(
                                                "Tipo de Usuario", justify="left", style="cyan")
                                            for i, usuario in enumerate(listaUsuarios, 1):
                                                table.add_row(
                                                    usuario['username'], usuario['email'], usuario['userType'])
                                            console.print(table)
                                            destinatario = input(
                                                "Email do destinatário: ")
                                            for i, usuario in enumerate(listaUsuarios, 1):
                                                if (usuario['email'] == destinatario):
                                                    a += 1
                                                elif (usuario['email'] != destinatario and i > len(listaUsuarios)):
                                                    print(
                                                        "Insira um email válido! \n")
                                                    os.system('pause')
                                                else:
                                                    i += 1
                                            assunto = input("Assunto: ")
                                            mensagem = input("Mensagem: ")
                                            data = datetime.now()
                                            dados_mensagem = {'remetente': Criptografar(cifra, login_user),
                                                            'destinatario': Criptografar(cifra, destinatario),
                                                            'assunto': Criptografar(cifra, assunto),
                                                            'mensagem': Criptografar(cifra, mensagem),
                                                            'data': Criptografar(cifra, data.strftime("%d/%m/%Y"))}
                                            SalvarMensagem(dados_mensagem)
                                            print(
                                                "\nMensagem enviada com sucesso!\n")
                                    #Opção para decriptografar mensagens
                                    case 2:
                                        LimparTela()
                                        print("Mensagens Recebidas:\n")
                                        mensagens = BuscarMensagensParaUsuario(
                                            login_user)

                                        if not mensagens:
                                            print("Nenhuma mensagem encontrada.")
                                        else:
                                            console = Console()
                                            table = Table(
                                                title="Mensagens Recebidas")
                                            table.add_column(
                                                "Remetente", style="cyan")
                                            table.add_column(
                                                "Assunto", style="cyan")
                                            table.add_column(
                                                "Mensagem", style="green")
                                            table.add_column(
                                                "Data", style="magenta")

                                            for msg in mensagens:
                                                remetente = Decriptografar(
                                                    cifra, msg['remetente'])
                                                assunto = Decriptografar(
                                                    cifra, msg['assunto'])
                                                mensagem = Decriptografar(
                                                    cifra, msg['mensagem'])
                                                data = Decriptografar(
                                                    cifra, msg['data'])

                                                table.add_row(
                                                    remetente, assunto, mensagem, data)

                                            console.print(table)
                                        os.system('pause')
                                    #Opção para configurar a criptografia
                                    case 3:
                                        while True:
                                            LimparTela()
                                            print(
                                                "-- CONFIGURAÇÕES DE CRIPTOGRAFIA --\n")
                                            print("Dicionário atual:\n")
                                        
                                            for k, v in cifra.items():
                                                print(f"'{k}' → '{v}'")

                                            print("\nOpções:")
                                            print("1 - Adicionar ou alterar entrada")
                                            print("2 - Remover entrada")
                                            print("0 - Voltar")

                                            opcao_cfg = input(
                                                "\nEscolha uma opção: ")

                                            if opcao_cfg == "1":
                                                chave = input(
                                                    "Letra/símbolo a ser criptografado: ").lower()
                                                valor = input(
                                                    "Substituir por: ").lower()
                                                if chave and valor:
                                                    cifra[chave] = valor
                                                    print(
                                                        f"Par '{chave}' → '{valor}' adicionado/atualizado com sucesso.")
                                                else:
                                                    print("Entrada inválida.")
                                                os.system("pause")

                                            elif opcao_cfg == "2":
                                                chave = input(
                                                    "Letra/símbolo a remover: ").lower()
                                                if chave in cifra:
                                                    del cifra[chave]
                                                    print(
                                                        f"Par '{chave}' removido com sucesso.")
                                                else:
                                                    print("Chave não encontrada.")
                                                os.system("pause")

                                            elif opcao_cfg == "0":
                                                break

                                            else:
                                                print("Opção inválida.")
                                                os.system("pause")
                                        #Opção para alterar a senha
                                    case 4:
                                        LimparTela()
                                        print("Alterar Senha:\n")
                                        senha_atual = pwinput.pwinput(
                                            prompt="Digite sua senha atual: ", mask='*')

                                        # Verifica se a senha atual está correta
                                        if verificar_Senha(senha_atual, u['password']):
                                            nova_senha = pwinput.pwinput(
                                                prompt="Digite a nova senha: ", mask='*')
                                            confirmar_senha = pwinput.pwinput(
                                                prompt="Confirme a nova senha: ", mask='*')

                                            if nova_senha != confirmar_senha:
                                                print("As senhas não coincidem!")
                                            else:
                                                nova_senha_hash = CriptografarSenha(
                                                    nova_senha)
                                                # Atualiza a senha no dicionário do usuário atual
                                                for usuario in listaUsuarios:
                                                    if usuario['email'] == login_user:
                                                        usuario['password'] = nova_senha_hash
                                                        break

                                                # Salva a nova lista de usuários
                                                with open("Usuarios.json", "w") as arquivo_usuarios:
                                                    json.dump(
                                                        listaUsuarios, arquivo_usuarios, indent=4)
                                                print("Senha alterada com sucesso!")
                                        else:
                                            print("Senha atual incorreta!")
                                        os.system('pause')##
                    else:
                        print("Senha Incorreta!")
                        os.system('pause')
                else:
                    i = i+1
                    if (i == len(listaUsuarios)):
                        print("Usuário não encontrado!")
            os.system('pause')
        case 0:
            print("Saindo...")
            break
