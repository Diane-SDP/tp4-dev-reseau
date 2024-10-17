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

def validate_input(message):
    pattern = r'^(-?\d{1,6})\s*([+\-*])\s*(-?\d{1,6})$'
    match = re.match(pattern, message)
    
    if match:
        num1, operator, num2 = int(match.group(1)), match.group(2), int(match.group(3))
        if -100000 <= num1 <= 100000 and -100000 <= num2 <= 100000:
            return True
    return False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True :
    try:
        s.connect((host, port))
        log_message("INFO", f"Connexion réussie à {host}:{port}.")
    except socket.error:
        log_message("ERROR", f"Impossible de se connecter au serveur {host} sur le port {port}.")
        break

    message = input("Calcul : ")
    while not validate_input(message):
        message = input("On accepte que les additions, soustractions, multiplications avec des nombres entiers de -100000 à 100000: ")
    s.sendall(str.encode(message))
    log_message("INFO", f"Message envoyé au serveur {host}:{port}.")

    data = s.recv(1024)

    if data :
        print(f"Résultat : {repr(data)}")
        log_message("INFO", f"Réponse reçue du serveur {host}: {repr(data)}.")

s.close()
sys.exit()