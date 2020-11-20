# Authors: Gabriel Bayer, Eugênio Pozzobon
# e-mails: gbayer.formula@gmail.com, eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError

def init():
    #define server and client
    global server, client, bokehPort, socketPort, socketIP, port, boudrateselected
    server = str_to_bool('False')
    client = str_to_bool('True')
    bokehPort = int('5006')
    socketPort = int('8080')
    socketIP = '127.0.0.1'
    port = 'COM5'
    boudrateselected = int('115200')

def updatesettings():
    pass