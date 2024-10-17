# TP4 : socquettes youpi

## I. Simple bs program

### 1. First steps

🌞 bs_server_I1.py

🌞 bs_client_I1.py

🌞 Commandes...


```powershell
# sur les 2 machines
[diane@localhost ~]$ sudo dnf install python -y

# sur le server
[diane@localhost ~]$ sudo firewall-cmd --add-port=13337/tcp --permanent
success
[diane@localhost ~]$ sudo firewall-cmd --reload
success
[diane@localhost tp4-dev-reseau]$ python bs_server_I1.py
Réponse du client : b'Meoooooo !'
[diane@localhost ~]$ ss -lnpt | grep 13337
LISTEN 0      1         10.1.1.254:13337      0.0.0.0:*    users:(("python",pid=1417,fd=3))

# sur le client
[diane@localhost tp4-dev-reseau]$ python bs_client_I1.py
Le serveur a répondu b'Hi mate !'
```

### 2. User friendly

🌞 bs_client_I2.py

🌞 bs_server_I2.py

### 3. You say client I hear control

🌞 bs_client_I3.py

## II. You say dev I say good practices

### 1. Args

🌞 bs_server_II1.py

### 2. Logs

```powershell
[diane@localhost ~]$ sudo mkdir /var/log/bs_server/
[diane@localhost ~]$ sudo touch /var/log/bs_server/bs_server.log
[diane@localhost ~]$ sudo chmod -R 755 /var/log/bs_server
```
