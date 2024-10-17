import argparse
import sys
import socket
import psutil
import re

class MyArgumentParser(argparse.ArgumentParser):

    def print_help(self, file=None):
        message = f"""Usage: {sys.argv[0]} [OPTIONS] \nOptions:\n-l, --listen     Specify the IP address to bind to. It must be a valid IP address of the machine.\n-p, --port       Specify the port number to bind to. Must be between 1024 and 65535.\n-h, --help       Show this help message and exit."""
        print(message)  
        sys.exit()          

host = '' 
port = 13337 

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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  
s.listen(1)

print("Listenint on port ", port, " with ip ", host)
conn, addr = s.accept()

conn.close()
