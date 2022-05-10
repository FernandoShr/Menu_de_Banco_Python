import os
from datetime import datetime

def mensagem(string):    #criei esta função para padronizar as mensagens de aviso no decorrer do código 
    tamanho = len(string)  #nesta linha determino a quantidade de caracteres que terá a mensagem
    print()
    print("-"*tamanho)  #com isso posso padronizar as mensagens, a quantidade de travessões que separam as linhas vai ser a mesma de caracteres da mensagem
    print(string)
    print("-"*tamanho)
    print() 

def nova_conta():  #nesta função há a criação da conta do cliente

    nome = input("Digite seu nome: ")  #determina o nome do cliente

    while True: #criei um while para caso o usuário coloque letras no CPF. Ocorrerá um erro e o usuário poderá escrever novamente o CPF
        cpf = input("Digite seu CPF: ")
        try:
            if isinstance(int(cpf), int):  #verifica se o CPF é uma variável inteira
                if int(cpf) > 0:
                    if os.path.isfile(cpf+".txt"):   #verifica se já existe uma conta com este CPF
                        mensagem("Já existe uma conta com este CPF!")
                    else:
                        break
                else:
                    mensagem("Valor negativo! Por favor, tente novamente.")
        except ValueError:
            mensagem("Formatação do CPF inválida! Por favor, inserir apenas números.")

    while True: #novamente um while para o usuário escolher o tipo de conta, e caso coloque um tipo que não existe aparecerá um erro e o usuário poderá tentar de novo
        tipo = input("Indique o tipo de conta (conta salario, comum ou plus): ")
        if (tipo != "salario") and (tipo != "comum") and (tipo != "plus"):
            mensagem("Tipo de conta inválido! Por favor, tente novamente.")
        else:
            break

    while True: #while para o valor da conta inicial, caso o usuário tente digitar letras ocorrerá um erro e o mesmo poderá tentar novamente
        valor_inicial = input("Valor inicial da conta: ")
        try:
            if isinstance(float(valor_inicial), float): #verifica se o valor é um número
                if float(valor_inicial) >= 0: #verifica se o valor adicionado está no padrão
                    valor_inicial = str(valor_inicial)
                    data = datetime.now() #registra o momento da criação da conta
                    break
                else:
                    mensagem("Valor negativo! Por favor, tente novamente.")
        except ValueError:
            mensagem("Formatação de valor inválida! Por favor inserir apenas números.")

    senha = input("Digite sua senha: ") #definir a senha
    
    tarifa = 0.00 #apenas um valor da tarifa que será impressa quando o usuário exibir o extrato

    arquivo = open(cpf+".txt","w") #criação de um arquivo com as informações do cliente
    arquivo.write("%s\n"%nome)
    arquivo.write("%s\n"%cpf)
    arquivo.write("%s\n"%tipo)
    arquivo.write("%s\n"%valor_inicial)
    arquivo.write("%s\n"%senha)
    arquivo.write(data.strftime("%Y-%m-%d  %H:%M") +";+;" + valor_inicial + ";" + str(tarifa) + ";" + valor_inicial)
    arquivo.close()

    print("\nConta criada com sucesso!")

def apagar_conta(): 
    while True: #while para caso o CPF digitado não existir, o usuário possa tentar novamente
        cpf = input("Digite o CPF da conta a qual deseja deletar: ")
        if os.path.isfile(cpf+".txt"): #verifica se o CPF existe
            senha = 0 #senha e dados aleatórios apenas para entrar no while
            dados = ['','','','','']
            while senha != dados[4]: #enquanto a senha estiver incorreta o usuário pode tentar novamente
                senha = input("Digite sua senha: ")
                arquivo = open(cpf+".txt","r")
                dados = arquivo.read().splitlines() #retorna uma lista em que cada elemento desta é uma linha do arquivo
                arquivo.close()
                if senha == dados[4].strip(): #verifica se a senha está correta
                    os.remove(cpf+".txt") #remove o arquivo
                    print("\nConta excluída com sucesso!")
                    return
                elif senha == "voltar": #caso o usuário tenha digitado o CPF errado e exista uma outra conta este CPF , há uma forma dele retornar e corrigir o CPF
                    break
                else:
                    mensagem("Senha incorreta! Tente novamente ou digite 'voltar' para retornar ao CPF.")
        elif cpf == "sair": #caso o usuário tenha entrado na opção errada, ele possue um meio de voltar ao menu
            return   
        else:
            mensagem("Não existe conta com este CPF. Tente novamente ou digite 'sair' para retornar ao menu.")

def debito():
    while True: #while para caso o CPF digitado não existir, o usuário possa tentar novamente
        cpf = input("Digite seu CPF: ")
        if os.path.isfile(cpf+".txt"): #verifica se o CPF existe
            senha = 0
            dados = ['','','','','']
            while senha != dados[4]:
                arquivo = open(cpf+".txt","r")
                dados = arquivo.readlines() #cria uma lista com os dados do arquivo
                senha = input("Digite sua senha: ")
                arquivo.close()
                if senha == dados[4].strip():
                    valor = -1 #valor apenas para entrar no ciclo
                    while valor != 0:
                        valor = input("Digite o valor a ser debitado: ")
                        try: 
                            if isinstance(float(valor), float): #testa se o valor digitado foi realmente um número
                                valor = float(valor) #converte em float a variável para poder realizar as operações
                                if valor >= 0:
                                    
                                    #verifica o tipo de conta do cliente
                                    if dados[2].strip() == "salario": 
                                        tarifa = 0.05*valor
                                        limite = 0.00
                                    elif dados[2].strip() == "comum":
                                        tarifa = 0.03*valor
                                        limite = -500.00
                                    elif dados[2].strip() == "plus":
                                        tarifa = 0.01*valor
                                        limite = -5000.00

                                    valor_final = ((float(dados[3]) - valor) - tarifa) #calcula o saldo final da conta depois da operação

                                    if valor_final <= limite: #verifica se o saldo final respeita a especificidade de cada tipo de conta
                                        print("\nEste valor não pode ser debitado, pois ultrapassa o limite permitido de R$%.2f em seu tipo de conta"%limite)
                                        return

                                    dados[3] = (str(valor_final)+"\n") #redefine os dados da lista e reescreve o arquivo do cliente
                                    arquivo = open(cpf+".txt","w")
                                    arquivo.writelines(dados)
                                    arquivo.close()
                                    arquivo = open(cpf+".txt","a") #adicionar o registro da operação como uma nova linha do arquivo
                                    data = datetime.now() #registra o momento da operação
                                    arquivo.write("\n"+ data.strftime("%Y-%m-%d  %H:%M") +";-;" + str(valor) + ";" + str(tarifa) + ";"+ str(valor_final)) #informações separadas por ; (para depois utilizar o split e assim ficar mais fácil de acessar as informações em uma única linha)
                                    arquivo.close()
                                    print("\nValor debitado com sucesso!")
                                    return
                                else:
                                    mensagem("Número negativo! Por favor, inserir um número positivo.")
                        except ValueError:
                                mensagem("Formatação de valor inválida! Por favor, inserir apenas números.")

                elif senha == "voltar":
                    break
                else:
                    mensagem("Senha incorreta! Por favor, tente novamente ou digite 'voltar' para retornar ao CPF.")
        elif cpf == "sair":
            return
        else:
            mensagem("Não existe uma conta com este CPF. Tente novamente ou digite 'sair' para retornar ao menu.")

def depositar():
    while True:
        cpf = input("Digite seu CPF: ")
        if os.path.isfile(cpf+".txt"): #verifica se existe a conta
            arquivo = open(cpf+".txt","r")
            dados = arquivo.readlines()
            arquivo.close()
            while True:
                print ("(Caso deseje corrigir o CPF, digite 'voltar')")
                valor = input("Digite o valor que deseja depositar: ")
                if valor == "voltar":
                    break
                try: 
                    if isinstance(float(valor), float): #testa se o valor digitado foi realmente um número
                        valor = float(valor) #converte em float a variável para poder realizar as operações
                        if valor >= 0: 
                            tarifa = 0.00
                            valor_final = (float(dados[3]) + valor) #determina o saldo no final da operação
                            dados[3] = (str(valor_final)+"\n") #converter em string para pode ser escrita no arquivo sem alterar as respectivas informações do arquivo
                            arquivo = open(cpf+".txt","w") #reescrever o arquivo
                            arquivo.writelines(dados)
                            arquivo.close()
                            arquivo = open(cpf+".txt","a") #para registrar a operação
                            data = datetime.now() #registra o momento
                            arquivo.write("\n"+ data.strftime("%Y-%m-%d  %H:%M") +";+;" + str(valor) + ";"  + str(tarifa) + ";" + str(valor_final))
                            arquivo.close()
                            print("\nValor depositado com sucesso!")
                            return
                        else:
                            mensagem("Valor negativo! Por favor, tente novamente.")
                except ValueError:
                    mensagem("Formatação de valor inválida! Por favor, inserir apenas números.")                                    
        elif cpf == "sair": #caso o usuário queira retornar ao menu
            return
        else:
            mensagem("Não existe conta com este CPF. Tente novamente ou digite 'sair' para cancelar a ação.")

def saldo(): #função que exibe o saldo
    while True: 
        cpf = input("Digite seu CPF: ")
        if os.path.isfile(cpf+".txt"):
            senha = 0
            dados = ['','','','','']
            while senha != dados[4].strip():
                arquivo = open(cpf+".txt","r")
                dados = arquivo.read().splitlines()
                arquivo.close()
                senha = input("Digite sua senha: ")
                if senha == dados[4]:
                    print("\nSeu saldo é de: R$%.2f"% float(dados[3]))
                    return
                elif senha == "voltar":
                    break
                else:
                    mensagem("Senha incorreta! Por favor, tente novamente ou digite 'voltar' para retornar ao CPF.")
        elif cpf == "sair":
            return
        else:
            mensagem("Não existe conta com este CPF. Tente novamente ou digite 'sair' para retornar ao menu.")

def extrato():
    while True:
        cpf = input("Digite seu CPF: ") 
        if os.path.isfile(cpf+".txt"):
            senha = 0
            dados = ['','','','','']
            while senha != dados[4]:
                arquivo = open(cpf+".txt","r")
                dados = arquivo.read().splitlines()
                arquivo.close()
                senha = input("Digite sua senha: ")
                if senha == dados[4].strip():
                    print("\n                <------------Extrato------------>")
                    #acessa as respectivas informações do arquivo
                    print("Nome:", dados[0]) 
                    print("CPF:", dados[1])
                    print("Conta:", dados[2])
                    #criei essas variáveis para definir a quantidade de caracteres que será reservada para as informações das operações
                    #assim o usuário pode realizar uma operação com qualquer quantia e o extrato vai se manter alinhado
                    tamanho_valor = 0
                    tamanho_tarifa = 0
                    tamanho_saldo = 0 
                    for linha in range(5,len(dados)): #acessa apenas as operações da conta do cliente
                        transacoes = dados[linha].split(";") #separa as informações
    
                        if len(str(round(float(transacoes[2]),2))) + 1 > tamanho_valor: #acessa o tamanho da string das operações(valores de deposito/debito) no arquivo e salva a que tiver maior quantidade de caracteres
                            tamanho_valor = len(str(round(float(transacoes[2]),2))) + 1  

                        if len(str(round(float(transacoes[3]),2))) + 1 > tamanho_tarifa: #acessa o tamanho da string da "tarifa" no arquivo e salva a que tiver maior quantidade de caracteres
                            tamanho_tarifa = len(str(round(float(transacoes[3]),2))) + 1

                        if len(str(round(float(transacoes[4]),2))) + 1 > tamanho_saldo: #acessa o tamanho da string do "saldo" no arquivo e salva a que tiver maior quantidade de caracteres
                            tamanho_saldo = len(str(round(float(transacoes[4]),2))) + 1  
                    
                    formato = "Data: %s   %s %" + str(tamanho_valor) + ".2f  Tarifa: %" + str(tamanho_tarifa) + ".2f" +  "  Saldo: %" + str(tamanho_saldo) + ".2f"; #estrutura da linha a ser printada

                    for linha in range(5,len(dados)): #separa as informações e depois as imprime, acessando apenas da linha 5 em diante do arquivo. Pois, é onde esta registrado a ocorrência das transações
                        transacoes = dados[linha].split(";") 
                        print( formato % (transacoes[0], transacoes[1], float(transacoes[2]), float(transacoes[3]), float(transacoes[4])))    

                    espera = input("\nPressione enter para continuar.") #esperar a ação do usuário
                             
                    return

                elif senha == "voltar":
                    break
                else:
                    mensagem("Senha incorreta! Por favor, tente novamente ou digite 'voltar' para retornar ao CPF.")
                    
        elif cpf=="sair":
            return
        else:
            mensagem("Não existe conta com este CPF. Tente novamente ou digite 'sair' para retornar ao menu.")

def main(): #função principal que insere o menu
    while True:
        print()
        print("---- Menu ----")
        print("Selecione a opção desejada:")
        print()
        print("1 - Cria conta nova")
        print("2 - Apagar conta")
        print("3 - Debitar")
        print("4 - Depositar")
        print("5 - Saldo")
        print("6 - Extrato")
        print()
        print("0 - Sair")
        opcao = input("") #usuário escolhe a opção

        if opcao == "1":
            nova_conta();
        elif opcao == "2":
            apagar_conta()
        elif opcao == "3":
            debito()
        elif opcao == "4":
            depositar()
        elif opcao == "5":
            saldo()
        elif opcao == "6":
            extrato()
        elif opcao == "0":
            return
main()