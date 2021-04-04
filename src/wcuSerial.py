# Author: Eugênio Pozzobon
# e-mail: eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import sys
from datetime import datetime

import pandas as pd
import serial
import src.settings as settings
from src.programTools import *
from src.wcuClientSocket import *
from src.wcuServerSocket import *


class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i + 1]
            self.buf = self.buf[i + 1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i + 1]
                self.buf[0:] = data[i + 1:]
                return r
            else:
                self.buf.extend(data)

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
            comport = serial.Serial(DEVICE,
                                    int(BAUD_RATE),
                                    timeout=TIMEOUT)
            global rl
            rl = ReadLine(comport)
            return comport
        except:
            sys.exit('COM PORT ERROR, EXITING')


#read serial in bytes
def readSerial(comport, bytelen = 2):
    try:
        global rl
        l = rl.readline()
        l = l[:-bytelen]
        return l
    except:
        #comport.close()
        return bytes(('0,0,0,0,0,0,0,0,0,0,0,0,0').encode())

#check integrity of bytes read and return it in string
def readStringSerial(bytes):
    string = ''
    try:
        string = bytes.decode(errors='strict')
        return string
    except:
        return string

#check if string readed is parsed to float and return the float array value of the string
def readFloatArraySerial(string):
    fstr = []
    try:
        splitString = string.split(',')
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
    global maxrow
    maxrow = 0
    return wcuFileName

#lê os dados, recodificia e salva no arquivo csv
def saveCSV(file, comport, header, canconfig, laststring):

    if(settings.client):
        recieved = clientRecieve().decode().replace('\n','')
        stringSave = recieved.split(',')
        decoded = ',' + ','.join(stringSave[-26:])
    else:
        stringbytes = readStringSerial(readSerial(comport, bytelen=2))
        decoded = decodeCAN(readFloatArraySerial(stringbytes)[1:(1 + 9)], canconfig, laststring)
        stringSave = (stringbytes + decoded).split(',')

    if settings.server:
        sendSocket(','.join(stringSave)+'\n')

    if(len(stringSave) == len(header.split(','))):
        file.write(','.join(stringSave)+'\n')
        global maxrow
        maxrow += 1
        return decoded, stringSave
    else:
        return laststring, stringSave


#salva o CSV e retorna o arquivo atualizado
def updateWCUcsv(seconds, wcufile, comport, header, canconfig, laststr):

    #entra no loop para ler o buffer da Serial, se for comunicação por socket não entra
    global maxrow
    datapoints = settings.telemetry_points

    if settings.client == True:
        laststr, totalstr = saveCSV(wcufile, comport, header, canconfig, laststr)
        laststr, totalstr = saveCSV(wcufile, comport, header, canconfig, laststr)

    else:
        while (comport.in_waiting > 0):
            laststr, totalstr = saveCSV(wcufile, comport, header, canconfig, laststr)
            laststr, totalstr = saveCSV(wcufile, comport, header, canconfig, laststr)
            #save 2 lines of csv file because if don't, the first time that the funcition is called will et error

    if maxrow < (datapoints+10):
        return pd.read_csv(wcufile.name, engine = 'c'), laststr
    else:
        read_just_few_lines = []
        for i in range(1, maxrow-(datapoints+1)):
            read_just_few_lines.append(i)
        dfr = pd.read_csv(wcufile.name, engine = 'c', skiprows=read_just_few_lines, nrows=datapoints)
        return dfr, laststr


#read multiples line to dosnt use this
def cleanCOMPORT(comport):
    for i in range(0, 10):
        readSerial(comport, bytelen=2)