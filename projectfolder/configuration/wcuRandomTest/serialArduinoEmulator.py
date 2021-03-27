import socket

IP = "127.0.0.1"
PORT = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))
s.listen(20)
s.settimeout(0.1)
clients = []

def i_manage_clients(clients, data):    #Function to manage clients
    try:
        global rm
        for client in clients:
            rm = client
            client.send(bytes(data))
    except ConnectionError:
        pass
        clients.remove(rm)

def sendSocket(data):
    i_manage_clients(clients, data)       #Call external function whenever necessary
    try:
        client_socket, addr = s.accept()
        clients.append(client_socket)  # Add client to list on connection
    except socket.timeout:
        pass
    except:
        raise

file = open('log.csv', 'r')

counter = 0
for line in file.readlines():
    counter = counter + 1
    if((counter > 40) & (line.split(',')[1] != 0)):
        sendSocket(line.encode()[:-3])
        counter = 0