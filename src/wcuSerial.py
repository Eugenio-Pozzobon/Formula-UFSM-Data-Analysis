# Author: Eugênio Pozzobon
# e-mail: eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import sys
import time, threading
from datetime import datetime
import serial

import src.settings as settings
from src.programTools import *
from src.wcuServerSocket import *
from src.wcuClientSocket import *

import pandas as pd
from time import process_time

#conect to serial selected
def connectSerial(DEVICE, BAUD_RATE = 115200, TIMEOUT = .1):

    if settings.server == True:
        conectServer()

    if settings.client == True:
        conectClient()
    if settings.client == False:
        print('\nObtendo informacoes sobre a comunicacao serial\n')
        # Iniciando conexao serial
        # comport = serial.Serial(DEVICE, 9600, timeout=1)

        try:
            serial.Serial(DEVICE, int(BAUD_RATE), timeout=TIMEOUT)
        except:
            sys.exit('COM PORT ERROR, EXITING')

        comport = serial.Serial(DEVICE,
                                int(BAUD_RATE),
                                timeout=TIMEOUT)
        return comport

#read serial in bytes
def readSerial(comport, bytelen = 2):
    try:
        l = comport.readline()
        #print(l)
        l = l[:-bytelen]
        return l
    except:
        #comport.close()
        return bytes(('0,0,0,0,0,0,0,0,0,0,0,0,0').encode())

#check integrity of bytes read and return it in string
def readStringSerial(bytes):
    string = ''
    try:
        string = ''
        string = bytes.decode(errors='strict')

        return string
    except:
        return string

#check if string readed is parsed to float and return the float array value of the string
def readFloatArraySerial(string):
    splitString = string.split(',')
    fstr = []
    try:
        for i in range(0, len(splitString)):
            fstr.append(float(splitString[i]))
        return fstr
    except:
        return fstr

#creates csv file for save data during communications
def createCSV(header):
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    wcuFileName = "./_wcu_cacheFiles_/"+dt_string+"wcufile.csv"
    wcuFile = open(wcuFileName, "w")
    wcuFile.write(header+'\n')
    wcuFile.close()

    return wcuFileName

#lê os dados, recodificia e salva no arquivo csv
def saveCSV(file, comport, header, canconfig, laststring):

    if(settings.client):
        recieved = clientRecieve().decode().replace('\n','')
        stringSave = recieved.split(',')
        decoded = ',' + ','.join(stringSave[-26:])
    else:
        stringbytes = readStringSerial(readSerial(comport, bytelen=2))
        canStart = 1
        decoded = decodeCAN(readFloatArraySerial(stringbytes)[canStart:(canStart + 9)], canconfig, laststring)
        stringSave = (stringbytes + decoded).split(',')

    if settings.server:
        sendSocket(','.join(stringSave)+'\n')

    if(len(stringSave) == len(header.split(','))):
        file.write(','.join(stringSave)+'\n')
        return decoded, stringSave
    else:
        return laststring, stringSave


#salva o CSV e retorna o arquivo atualizado
def updateWCUcsv(seconds, wcufile, comport, header, canconfig, laststr):

    #entra no loop para ler o buffer da Serial, se for comunicação por socket não entra
    if settings.client == True:
        laststr, totalstr = saveCSV(wcufile, comport, header, canconfig, laststr)
        laststr, totalstr = saveCSV(wcufile, comport, header, canconfig, laststr)

    else:
        t1_start = process_time()
        while (comport.in_waiting > 0):
            laststr, totalstr = saveCSV(wcufile, comport, header, canconfig, laststr)
            laststr, totalstr = saveCSV(wcufile, comport, header, canconfig, laststr)
            #save 2 lines of csv file because if don't, the first time that the funcition is called will et error
        t1_stop = process_time()
        print("Elapsed time during the whole program in seconds: {:.6f}".format((t1_stop - t1_start)))

    return pd.read_csv(wcufile.name), laststr

#read multiples line to dosnt use this
def cleanCOMPORT(comport):
    for i in range(0, 10):
        readSerial(comport, bytelen=2)