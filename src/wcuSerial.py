# !/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import time
import serial

"""
VARIAVEIS GLOBAIS (NESTE EXEMPLO)
"""

DEVICE = '/dev/ttyUSB0'
BAUD_RATE = '9600'
TIMEOUT = '1'
PARITY = 'N'
STOPBITS = '1'
BYTESIZE = '8'


def InfoComSerial():
    print
    '\nObtendo informacoes sobre a comunicacao serial\n'
    # Iniciando conexao serial
    # comport = serial.Serial(DEVICE, 9600, timeout=1)
    comport = serial.Serial(DEVICE,
                            int(BAUD_RATE),
                            timeout=int(TIMEOUT),
                            bytesize=int(BYTESIZE),
                            stopbits=int(STOPBITS),
                            parity=PARITY)
    # Alem das opcoes rtscts=BOOL, xonxoff=BOOL, e dsrdtr=BOOL
    # Link: http://pyserial.sourceforge.net/pyserial_api.html#constants
    time.sleep(1.8)  # Entre 1.5s a 2s
    print
    '\nStatus Porta: %s ' % (comport.isOpen())
    print
    'Device conectado: %s ' % (comport.name)
    print
    'Dump da configuracao:\n %s ' % (comport)

    print
    '\n###############################################\n'

    # Fechando conexao serial
    comport.close()


""" main """
if __name__ == '__main__':
    InfoComSerial()