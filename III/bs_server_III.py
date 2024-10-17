import argparse
import datetime
import sys
import socket
import time
import re
import os       

host = '10.1.1.254' 
port = 13337 
windows = os.name == "nt"

def log_message(level, message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_log = f"{timestamp} {level} {message}"
    if level == "INFO":
        message_log = f"{timestamp} \033[37m{level}\033[0m {message}"
        print(f"{message_log}") 
    elif level == "WARN":
        message_log = f"{timestamp} \033[33m{level}\033[0m {message}"
        print(f"{message_log}") 
    with open('/var/log/bs_server/bs_server.log', 'a') as logfile:
        logfile.write(message_log + ".\n")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  
s.listen(1)
log_message("INFO", f"Le serveur tourne sur {host}:{port}")
last_connection = time.time()
while True:
    elapsed_time = time.time() - last_connection
    if elapsed_time >= 60:
        log_message("WARN", "Aucun client depuis plus de une minute.")
        last_connection = time.time() 
    s.settimeout(60) 
    try:
        conn, addr = s.accept()
        log_message("INFO", f"Un client ({addr}) s'est connecté.")

        while True : 
            try:
                data = conn.recv(1024)
                if not data: break
                log_message("INFO", f"Le client ({addr}) a envoyé \"{data}\".")
                response = eval(data)
                log_message("INFO", f"Réponse envoyée au client {addr}: \"{response}\".")
                conn.sendall(str(response).encode())

            except socket.error:
                print("Error occured")
                print(socket.error)
                break
    except socket.timeout:
            pass  
    except socket.error:
                print("Error occured")
                print(socket.error)
                break

conn.close()
