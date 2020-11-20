# Authors: Gabriel Bayer, Eugênio Pozzobon
# e-mails: gbayer.formula@gmail.com, eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import socket
import src.settings as settings

ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []

def conectServer():
    ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ser.bind((settings.socketIP, settings.socketPort))
    ser.listen()
    ser.settimeout(0.01)

def i_manage_clients(clients, data):    #Function to manage clients
    try:
        global rm

        for c in clients:
            rm = c
            b = c.send(bytes(data.encode()))

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
