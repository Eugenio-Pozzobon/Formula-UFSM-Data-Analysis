# Authors: Gabriel Bayer, Eugênio Pozzobon
# e-mails: gbayer.formula@gmail.com, eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import socket

IP = '127.0.0.1'
PORT = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))
s.listen()
s.settimeout(0.01)
# s.setblocking(False)
clients = []

def i_manage_clients(clients, data):    #Function to manage clients
    try:
        global rm
        print(clients)
        for client in clients:
            rm = client
            b = client.send(bytes(data.encode()))
            print(client)
    except ConnectionError:
        pass
        clients.remove(rm)
    except:
        exit('Socket Error')

def sendSocket(data):
    i_manage_clients(clients, data)       #Call external function whenever necessary
    try:
        client_socket, addr = s.accept()
        clients.append(client_socket)  # Add client to list on connection
    except socket.timeout:
        pass
    except:
        exit('Socket Error')
        raise
