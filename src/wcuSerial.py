import sys
import time, threading
from datetime import datetime
import serial

from src.programTools import *

import pandas as pd

def connectSerial(DEVICE, BAUD_RATE, TIMEOUT = .1):
    print('\nObtendo informacoes sobre a comunicacao serial\n')
    # Iniciando conexao serial
    # comport = serial.Serial(DEVICE, 9600, timeout=1)
    comport = serial.Serial(DEVICE,
                            int(BAUD_RATE),
                            timeout=TIMEOUT)
    return comport

def readSerial(comport, bytelen = 2):
    b = []
    read=True
    try:
        comport.readinto(b)
    except:
        read = False

    l = 0
    if(read):
        l = comport.readline()[:-bytelen]
    return l

def readStringSerial(bytes):
    read = True
    try:
        bytes.decode(errors='strict')
    except:
        read = False

    string = ""
    if(read):
        string = bytes.decode(errors='strict')

    return string

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

def createCSV(header):
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    wcuFileName = "./_wcu_cacheFiles_/"+dt_string+"wcufile.csv"
    wcuFile = open(wcuFileName, "w")
    wcuFile.write(header+'\n')
    wcuFile.close()

    return wcuFileName

def saveCSV(file, comport, header):
    bytes = readSerial(comport, bytelen=2)
    stringbytes = readStringSerial(bytes)
    FloatArray = readFloatArraySerial(stringbytes)
    stringSave = (stringbytes + decodeCAN(FloatArray)).split(',')
    if(len(stringSave) == len(header.split(','))):
        file.write(','.join(stringSave)+'\n')

def updateWCUcsv(seconds, wcufilename, comport, header):
    start_time = time.time()

    wcufile = open(wcufilename, "at")

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            break

        saveCSV(wcufile, comport, header)

    wcufile.close()

    return pd.read_csv(wcufilename)

def cleanCOMPORT(comport):
    for i in range(0, 20):
        bytes = readSerial(comport, bytelen=2)