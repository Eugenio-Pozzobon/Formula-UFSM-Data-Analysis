# Authors: Gabriel Bayer, Eugênio Pozzobon
# e-mails: gbayer.formula@gmail.com, eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import socket
import src.settings as settings
from tkinter import messagebox
import src.wcuScreen as wcuScreen

cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conectClient():
    '''
    conect to the server based on settings file
    :return: none
    '''
    cli.connect((settings.socketIP, settings.socketPort))

def clientRecieve():
    '''
    read server until get an aceptable message
    :return: none
    '''
    while True:
        try:
            msg = cli.recv(1024)

            # check message integrity
            splitmsg = msg.decode('utf8').split(',')
            do = True
            for value in splitmsg:
                if value == '':
                    value = '0'

            # if all bytes get recieved
            if(len(msg.decode('utf8').split(','))==(10+26)) & do:
                print((','.join(splitmsg)).encode())
                return (','.join(splitmsg)).encode()
        except:
            # if server disconect, end program
            messagebox.showwarning(title='Connection Warning', message = 'Server disconect. Close the navegator tab to end the aplication')
            wcuScreen.endWCU()
            sys.exit('Exit')





