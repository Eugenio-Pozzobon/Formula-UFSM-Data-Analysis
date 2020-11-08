# Author: Eugênio Pozzobon
# e-mail: eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import sys
import time, threading
from datetime import datetime
import serial

from src.programTools import *
from src.wcuServerSocket import *
from src.wcuClientSocket import *

import pandas as pd

#define server and client
server = False
client = True

#conect to serial selected
def connectSerial(DEVICE, BAUD_RATE = 115200, TIMEOUT = .1):
    if client == True:
        conectClient()
    if client == False:
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


    read=True
    try:
        l = comport.readline()[:-bytelen]
        print(l)
    except:
        read = False
        #comport.close()
        return bytes(('0,0,0,0,0,0,0,0,0,0').encode())

    return l

#check integrity of bytes read and return it string
def readStringSerial(bytes):
    read = True
    try:
        bytes.decode(errors='strict')
    except:
        read = False

    string = ''
    if(read):
        string = bytes.decode(errors='strict')

    return string

#check if string readed is parsed to float and return the float array value of the string
def readFloatArraySerial(string):
    splitString = string.split(',')
    read = True
    try:
        for i in range(0, len(splitString)):
            fstr = float(splitString[i])
    except:
        read = False

    fstr = []
    if read:
        for i in range(0, len(splitString)):
            fstr.append(float(splitString[i]))
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
    if(client):
        recieved = clientRecieve().decode().replace('\n','')
        stringSave = recieved.split(',')
        decoded = ',' + ','.join(stringSave[-26:])
    else:
        bytes = readSerial(comport, bytelen=2)
        stringbytes = readStringSerial(bytes)
        FloatArray = readFloatArraySerial(stringbytes)
        decoded = decodeCAN(FloatArray, canconfig, laststring)
        stringSave = (stringbytes + decoded).split(',')

    if server:
        sendSocket(','.join(stringSave)+'\n')

    if(len(stringSave) == len(header.split(','))):
        file.write(','.join(stringSave)+'\n')
        return decoded, stringSave
    else:
        return laststring, stringSave


#salva o CSV e retorna o arquivo atualizado
def updateWCUcsv(seconds, wcufile, comport, header, canconfig, laststring):
    start_time = time.time()

    cdc = pd.DataFrame(columns=header.split(','))

    laststr = laststring
    #entra no loop para ler o buffer da Serial, se for comunicação por socket não entra
    if client == True:
        laststr, totalstr = saveCSV(wcufile, comport, header, canconfig, laststr)
        # cdc = pd.DataFrame(data=[totalstr], columns=header.split(','))

        laststr, totalstr = saveCSV(wcufile, comport, header, canconfig, laststr)
        # cdc.append(totalstr)

    else:
        while (comport.in_waiting > 0):
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > seconds:
                break

            laststr, totalstr= saveCSV(wcufile, comport, header, canconfig, laststr)
            #cdc = pd.DataFrame(data=[totalstr], columns=header.split(','))

            laststr, totalstr = saveCSV(wcufile, comport, header, canconfig, laststr)
            #cdc.append(totalstr)

            #save 2 lines of csv file because if don't, the first time that the funcition is called will et error
            #if client:
            #    laststr = saveCSV(wcufile, comport, header, canconfig, laststr)
            #    laststr = saveCSV(wcufile, comport, header, canconfig, laststr)

    wcufile.close()

    return pd.read_csv(wcufile.name), laststr, cdc

#read multiples line to dosnt use this
def cleanCOMPORT(comport):
    for i in range(0, 10):
        bytes = readSerial(comport, bytelen=2)