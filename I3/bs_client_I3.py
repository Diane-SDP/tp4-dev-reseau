import re
import socket
import sys

host = '10.1.1.254' 
port = 13337        
      

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((host, port))
    print("Connecté avec succès au serveur " + host + " sur le port " + str(port))
except socket.error:
    print("Error occured")

message = input("Que veux-tu envoyer au serveur : ")

if type(message) is not str:
    raise TypeError("Ici on veut que des strings !")

if not re.search(r".*(meo|waf).*", message) :
    raise ValueError("on veut meo ou waf pas d'humain ici")


s.sendall(str.encode(message))

data = s.recv(1024)

s.close()

if data :
    print(f"Le serveur a répondu {repr(data)}")

sys.exit()