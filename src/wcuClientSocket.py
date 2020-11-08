# Authors: Gabriel Bayer, Eugênio Pozzobon
# e-mails: gbayer.formula@gmail.com, eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import socket

IP = '127.0.0.1'
PORT = 8000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conectClient():
    client.connect((IP, PORT))

def clientRecieve():
    #lê o server até conseguir uma mensagem confiável
    while True:
        msg = client.recv(1024)

        ##Checa se a mensagem chegou inteira
        splitmsg = msg.decode('utf8').split(',')
        do = True
        for value in splitmsg:
            if value == '':
                vlue = '0'

        #se todos os bytes estão ali:
        if(len(msg.decode('utf8').split(','))==(10+26)) & do:
            print((','.join(splitmsg)).encode())
            return (','.join(splitmsg)).encode()





