import socket

host = '10.1.1.254' 
port = 13337 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  

s.listen(1)
conn, addr = s.accept()
print('Un client vient de se co et son IP c\'est.', addr, '.')

while True : 
    try:
        data = conn.recv(1024)

        if not data: break

        if str.encode("meo") in data :
            conn.sendall(str.encode("Meo à toi confrère."))
        elif str.encode("waf") in data :
            conn.sendall(str.encode("ptdr t ki"))
        else :
            conn.sendall(str.encode("Mes respects humble humain."))

    except socket.error:
        print("Error occured")
        print(socket.error)
        break


conn.close()

