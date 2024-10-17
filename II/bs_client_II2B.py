import datetime
import re
import socket
import sys

host = '10.1.1.254' 
port = 13337        
      
def log_message(level, message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_log = f"{timestamp} {level} {message}"
    if level == "INFO":
        message_log = f"{timestamp} \033[37m{level}\033[0m {message}"
    elif level == "ERROR":
        message_log = f"{timestamp} \033[31m{level}\033[0m {message}"
        message_console = f"\033[31m{level}\033[0m {message}"
        print(f"{message_console}") 
    with open('/var/log/bs_client/bs_client.log', 'a') as logfile:
        logfile.write(message_log + ".\n")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True :
    try:
        s.connect((host, port))
        log_message("INFO", f"Connexion réussie à {host}:{port}.")
    except socket.error:
        log_message("ERROR", f"Impossible de se connecter au serveur {host} sur le port {port}.")
        break

    message = input("Que veux-tu envoyer au serveur : ")

    if type(message) is not str:
        raise TypeError("Ici on veut que des strings !")

    if not re.search(r".*(meo|waf).*", message) :
        raise ValueError("on veut meo ou waf pas d'humain ici")

    s.sendall(str.encode(message))
    log_message("INFO", f"Message envoyé au serveur {host}:{port}.")

    data = s.recv(1024)


    if data :
        print(f"Le serveur a répondu {repr(data)}")
        log_message("INFO", f"Réponse reçue du serveur {host}: {repr(data)}.")

s.close()
sys.exit()