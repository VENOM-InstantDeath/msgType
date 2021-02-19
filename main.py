import amino
from modules import color
from os import listdir, system, _exit
from json import dumps, load
from getpass import getpass
from time import sleep

client = amino.Client()  # Global class

def join(subclient: object, *params) -> tuple:
    """
    Une el bot a un chat
    :param subclient: amino.SubClient()
    :param params: link hacia el chat
    :rtype: tuple
    """
    try:
        X = subclient.get_from_code(params[0][0]).objectId
        subclient.join_chat(X)
        return True, X
    except:
        return False, 0

# Inicia sesión
while True:
    if "data" not in listdir():
        print("\t\tInicia sesión\n\n")
        DATA = {'CREDS': {"email": input("Correo electrónico: "), "password": getpass("Contraseña: ")}}
        try:
            client.login(**DATA['CREDS'])
        except amino.exceptions.InvalidAccountOrPassword:
            print("\nCorreo o contraseña incorrectos")
            print("Presiona enter para continuar.")
            input()
            system("clear")
            continue
        F = open("data", "w+")
        F.write(dumps(DATA, indent=4))
        F.close()
        print("\033[2J")
    else:
        F = open("data", "r")
        DATA = load(F)
        F.close()
        client.login(**DATA['CREDS'])
        print("\033[2J")
    break

print(client.profile.nickname)
print("\nlogged in...")

# Ingresa a comunidad
while True:
    if "COMM" not in DATA:
        print(f"{color.red}\t\t¿En qué comunidad deseas iniciar el programa?{color.nm}\n\n")
        DATA['COMM'] = input("aminoId: ")
        try:
            DATA['COMM'] = client.search_community(DATA['COMM']).comId[0]
            client.join_community(DATA['COMM'])
        except amino.exceptions.CommunityNotFound:
            print("Comunidad inexistente.")
            sleep(1)
            print("\033[2J")
            continue
        F = open("data", "w+")
        F.write(dumps(DATA, indent=4))
        F.close()
        break
    else:
        client.join_community(DATA['COMM'])
        break

subclient = amino.SubClient(DATA['COMM'], profile=client.profile)  # Operation with community
print("\nJoined Community...")

CHAT = ["", ""]

while True:
    cmd = input(">>")
    if cmd == "enter":
        link = input("\nEnter chat link: ")
        r = join(subclient, [link])
        if not r[0]:
            print("Ocurrió un error durante la operación.")
            continue
        CHAT[0] = r[1]
        CHAT[1] = subclient.get_chat_thread(r[1]).title
    if cmd == "send":
        while True:
            msg = input(f"{CHAT[1]}>> ")
            if msg == ".":
                break
            try:
                subclient.send_message(CHAT[0], msg, 100)
            except:
                pass
    if cmd == "exit":
        _exit(0)
