import argparse
import datetime
import sys
import socket
import time
import re
import os

class MyArgumentParser(argparse.ArgumentParser):

    def print_help(self, file=None):
        message = f"""Usage: {sys.argv[0]} [OPTIONS] \nOptions:\n-l, --listen     Specify the IP address to bind to. It must be a valid IP address of the machine.\n-p, --port       Specify the port number to bind to. Must be between 1024 and 65535.\n-h, --help       Show this help message and exit."""
        print(message)  
        sys.exit()          

host = '10.1.1.254' 
port = 13337 
windows = os.name == "nt"

parser = MyArgumentParser()

parser.add_argument("-l", "--listen", action="store")
parser.add_argument("-p", "--port", action="store")

args = parser.parse_args()

if args.port != None :
    if int(args.port) > 65535 or int(args.port) < 0 :
        print("ERROR -p argument invalide. Le port spécifié ", args.port," n'est pas un port valide (de 0 à 65535).")
        sys.exit(1)
    elif int(args.port) <= 1024 :
        print("ERROR -p argument invalide. Le port spécifié ", args.port," est un port privilégié. Spécifiez un port au dessus de 1024.")
        sys.exit(2)
    port = int(args.port)

if args.listen != None :
    if not re.search("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", args.listen) :
        print("ERROR -l argument invalide. L'adresse ", args.listen," n'est pas une adresse IP valide.")
        sys.exit(3)
    if args.listen not in str(psutil.net_if_addrs()) :
        print("ERROR -l argument invalide. L'adresse ", args.listen," n'est pas l'une des adresses IP de cette machine.")
        sys.exit(4)
    host = args.listen

def log_message(level, message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_log = f"{timestamp} {level} {message}"
    if level == "INFO":
        message_log = f"{timestamp} \033[37m{level}\033[0m {message}"
        print(f"{message_log}") 
    elif level == "WARN":
        message_log = f"{timestamp} \033[33m{level}\033[0m kip {message}"
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
                response = None

                if str.encode("meo") in data :
                    response = str.encode("Meo à toi confrère.")
                elif str.encode("waf") in data :
                    response = str.encode("ptdr t ki")
                else :
                    response = str.encode("Mes respects humble humain.")
                
                if response != None: 
                    log_message("INFO", f"Réponse envoyée au client {addr}: \"{response}\".")
                    conn.sendall(response)

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
