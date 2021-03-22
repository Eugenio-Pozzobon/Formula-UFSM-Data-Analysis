# Authors: Gabriel Bayer, Eugênio Pozzobon
# e-mails: gbayer.formula@gmail.com, eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import pandas as pd

def str_to_bool(s):
    '''
    Check if string is an boolean flag.
    :param s: string for test
    :return: boolean
    '''
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError

def init():
    '''
    Read the settings file to configure all software
    :return: none
    '''
    global server, client, bokehPort, socketPort, socketIP, port, boudrateselected, channels_config_propertise,colortheme
    setfile = open('./projectfolder/settings.txt')
    settings = setfile.readlines()
    server = str_to_bool(settings[0].split(sep = ':')[1])
    client = str_to_bool(settings[1].split(sep = ':')[1])
    bokehPort = int(settings[2].split(sep = ':')[1])
    socketPort = int(settings[3].split(sep = ':')[1])
    socketIP = settings[4].split(sep = ':')[1]
    port = settings[5].split(sep = ':')[1]
    boudrateselected = settings[6].split(sep = ':')[1]
    colortheme = settings[7].split(sep=':')[1]

    setfile.close()
    channels_config_propertise = pd.read_csv('./projectfolder/configuration/channels.csv', sep = ';', index_col = 'Channel')

    global ignore_rpm
    ignore_rpm = True

def updatesettings():
    '''
    Update some setup settings in the file
    :return: none
    '''
    pass