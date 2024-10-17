import socket

host = '10.1.1.254' 
port = 13337 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  

s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
conn.sendall(b'Hi mate !')

while True : 
    try:
        data = conn.recv(1024)

        if not data: break

        print(f"Réponse du client : {data}")

    except socket.error:
        print("Error occured")
        break


conn.close()

