# Author: Eugênio Pozzobon
# e-mail: eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import pandas as pd
import numpy as np
import time
import zipfile
import os
import shutil
import sys
import gc
import pathlib
import serial
import socket
import tkinter as tk
import re

from bokeh.layouts import row, column, layout, gridplot
from bokeh.plotting import figure
from bokeh.models.widgets import Tabs, Panel, Button
from bokeh.models import ColumnDataSource
from bokeh.server.server import Server
from bokeh.models import RangeSlider
from datetime import datetime
from bokeh.models import Legend, LinearAxis, Range1d
from bokeh.models import Arc, Circle, Plot, Ray, Text
from bokeh.models import MultiSelect
from bokeh.models import Spinner
from bokeh.models import RadioGroup
from math import cos, pi, sin
from functools import partial


# settings.py
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

    global ignore_rpm, telemetry_points
    telemetry_points = 1000
    ignore_rpm = True

def updatesettings():
    '''
    Update some setup settings in the file
    :return: none
    '''
    pass

#programtools

def restart_program():
    '''
    restart the application
    :return: none
    '''
    python = sys.executable
    os.execl(python, python, * sys.argv)

#make a filter
def bandPassFilter(signal, cutf=5, order = 5, type = 'lowpass'):
    '''
    apply an filter
    :param signal: y array values
    :param cutf: cut frequency
    :param order: order
    :param type: filter typt, see scipy.signal.butter filter types
    :return: y array value filtered
    '''
    from scipy.signal import butter, filtfilt
    fs = 200  # sample rate, Hz
    # Filter requirements.
    cutoff = cutf # desired cutoff frequency of the filter, Hz ,      slightly higher than actual 1.2 Hz
    nyq = 1 * fs  # Nyquist Frequency
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    [b, a]  = butter(order, normal_cutoff, btype=type, analog=False)
    y = filtfilt(b, a , signal, axis=0)
    return y

def mapDouble(x, in_min, in_max, out_min, out_max):
    '''
    make the linear transformation for linear calibrations
    :param x: value
    :param in_min: minimun value in the original scale
    :param in_max: maximun value in the original scale
    :param out_min: minimun value in the final scale
    :param out_max: maximun value in the final scale
    :return: converted value
    '''
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def dbfft(time, y, ref=1):
    '''
    Calculate spectrum in dB scale
    :param time: x signal
    :param y: input signal
    :param ref: reference value used for dBFS scale. 32768 for int16 and 1 for float
    :return:  frequency vector,  spectrum in dB scale
    '''

    N = len(time)
    fs = len(time)/(time[len(time)-1]-time[1])
    win = np.hanning(N)
    x = y * win  # Take a slice and multiply by a window
    sp = np.fft.rfft(x)  # Calculate real FFT
    s_mag = np.abs(sp) * 2 / np.sum(win)  # Scale the magnitude of FFT by window and factor of 2

    # because we are using half of FFT spectrum
    s_dbfs = 20 * np.log10(s_mag / ref)  # Convert to dBFS
    freq = np.arange((N / 2) + 1) / (float(N) / fs)  # Frequency axis

    return freq[:-1], s_dbfs

def decodeCAN(CANarray, configtable, lastLine):
    '''
    decode variables by recieving CAN frame.
    :param CANarray: [CANID, CANFRAME0, CANFRAME1, CANFRAME2, CANFRAME3, CANFRAME4, CANFRAME5, CANFRAME6, CANFRAME7]
    :param configtable: table to setup can conversion
    :param lastLine: last line decoded
    :return: CAN Decoded in the final array format
    '''

    # take the last value and pass to final CAN varibles decoded,
    # make this because one CAN frame doesnt update all variables and the variables
    # that isnt update must be the same as the last reanden
    lastlinearray = lastLine.split(',')
    CAN = []
    for value in lastlinearray:
        CAN.append(value)

    CAN.pop(0)

    ctr = 0
    if len(CANarray) == 9 :
        for channel in configtable['Channel']:
            line = configtable.iloc[ctr]
            if float(CANarray[0]) == line['ID']:
                if(line['Bit_Mask'] == 1):
                    CAN[line['Indice']] = str((float(CANarray[1+line['Bytes']]) * 256 + float(CANarray[2+line['Bytes']]))/(pow(10,line['Casas_decimais'])))
                else:
                    CAN[line['Indice']] = str(float(CANarray[1+line['Bytes']])/(pow(10,line['Casas_decimais'])))
            ctr = ctr+1

    candecoded = ',' + ','.join(CAN)
    #print(candecoded)
    return candecoded.replace('\n','')


#userformula
def user_equations(data):
    '''
    Take data and process users equations in the entire database, reducing size poping inused columns.
    :param data: pandas dataframe containing data
    :return: pandas dataframe with updated data
    '''

    data.loc[(data['RPM'] > 2000) & (data['EngineTemp'] > 84), 'HalfFan'] = 1
    data.loc[(data['RPM'] < 2000) | (data['EngineTemp'] < 84), 'HalfFan'] = 0
    data.loc[(data['RPM'] > 2000) & (data['EngineTemp'] > 94), 'FullFan'] = 1
    data.loc[(data['RPM'] < 2000) | (data['EngineTemp'] < 94), 'FullFan'] = 0

    data['A_9_map'] = bandPassFilter(data['A_9_map'])
    '''
    sensor_data_a = data['GPSlatHW']
    sensor_data_b = data['GPSlatLW']
    sensor_data_c = data['GPSlongHW']
    sensor_data_d = data['GPSlongLW']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)

    gpsLat = ((data['GPSlatHW']-65536) * 65536 + data['GPSlatLW'])/10000000
    gpsLong = ((data['GPSlongHW']-65536) * 65536 + data['GPSlongLW'])/10000000
    '''

    data['GPSLat'] = ((data['GPSlatHW']-65536) * 65536 + data['GPSlatLW'])/10000000
    data['GPSLong'] = ((data['GPSlongHW']-65536) * 65536 + data['GPSlongLW'])/10000000

    '''
    sensor_data_a = data['GForceLat']
    sensor_data_b = -data['GForceLong']
    sensor_data_c = -data['gyro_z']
    sensor_data_e = data['Speed']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)
    sensor_data_f = pd.to_numeric(sensor_data_f)
    '''

    sensor_data = pd.to_numeric(data['SteeringAngle'])
    sensor_data.loc[sensor_data > 3276.8] = sensor_data.loc[sensor_data > 3276.8] - 6553.6
    data['SteeringAngle'] = sensor_data

    sensor_data = pd.to_numeric(data['ECU_GForceLat'])
    sensor_data.loc[sensor_data > 32.768] = sensor_data.loc[sensor_data > 32.768] - 65.536
    data['ECU_GForceLat'] = sensor_data

    cutFs = 5
    data['GForceLat'] = bandPassFilter(data['GForceLat'], cutf=cutFs, order=5)
    data['GForceLong'] = bandPassFilter(-data['GForceLong'], cutf=cutFs, order=5)
    cutFs = 1
    data['gyro_z'] = bandPassFilter(-data['gyro_z'], cutf=cutFs, order=5)

    '''
    sensor_data_a = data['LVDTFL']
    sensor_data_b = data['LVDTFR']
    sensor_data_c = data['LVDTRL']
    sensor_data_d = data['LVDTRR']
    sensor_data_e = data['Speed']
    sensor_data_x = -data['GForceLong']
    sensor_data_y = data['GForceLat']
    sensor_data_z = data['GForceVert']
    sensor_data_tps = data['TPS']
    sensor_data_bp = data['BrakePressure']
    sensor_data_sa = data['SteeringAngle']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)
    sensor_data_sa = pd.to_numeric(sensor_data_sa)
    '''

    cutFs = 12

    data['LVDTFL'] = bandPassFilter(data['LVDTFL'], cutf=cutFs, order=5)
    data['LVDTFR'] = bandPassFilter(data['LVDTFR'], cutf=cutFs, order=5)
    data['LVDTRL'] = bandPassFilter(data['LVDTRL'], cutf=cutFs, order=5)
    data['LVDTRR'] = bandPassFilter(data['LVDTRR'], cutf=cutFs, order=5)
    '''    filteredsignal_x = ncuTools.bandPassFilter(sensor_data_x, cutf=5, order=5)
    filteredsignal_y = ncuTools.bandPassFilter(sensor_data_y, cutf=5, order=5)
    filteredsignal_z = ncuTools.bandPassFilter(sensor_data_z, cutf=5, order=5)'''

    data['LVDTFL'] = mapDouble(data['LVDTFL'], 0.59, 0.65, 206, 196)
    data['LVDTFR'] = mapDouble(data['LVDTFR'], 0.9, 0.94, 206, 196)
    data['LVDTRL'] = mapDouble(data['LVDTRL'], 0.92, 1.02, 221, 216)
    data['LVDTRR'] = mapDouble(data['LVDTRR'], 0.76, 0.8, 221, 216)

    '''    
    filteredsignal_a = ncuTools.mapDouble(filteredsignal_a, 0.59, 0.65, 206, 196)
    filteredsignal_b = ncuTools.mapDouble(filteredsignal_b, 0.9, 0.94, 206, 196)
    filteredsignal_c = ncuTools.mapDouble(filteredsignal_c, 0.92, 1.02, 221, 216)
    filteredsignal_d = ncuTools.mapDouble(filteredsignal_d, 0.76, 0.8, 221, 216)'''

    diff1 = np.diff(data['LVDTFL']) / np.diff(data['time'])
    diff2 = np.diff(data['LVDTFR']) / np.diff(data['time'])
    diff3 = np.diff(data['LVDTRL']) / np.diff(data['time'])
    diff4 = np.diff(data['LVDTRR']) / np.diff(data['time'])

    diff1 = np.append(diff1, 0)
    diff2 = np.append(diff2, 0)
    diff3 = np.append(diff3, 0)
    diff4 = np.append(diff4, 0)

    data['diffLVDTFL'] = diff1
    data['diffLVDTFR'] = diff2
    data['diffLVDTRL'] = diff3
    data['diffLVDTRR'] = diff4

    #diffdata_a = ncuTools.bandPassFilter(diffdata_a, cutf=cutFs, order=5)
    #diffdata_b = ncuTools.bandPassFilter(diffdata_b, cutf=cutFs, order=5)
    #diffdata_c = ncuTools.bandPassFilter(diffdata_c, cutf=cutFs, order=5)
    #diffdata_d = ncuTools.bandPassFilter(diffdata_d, cutf=cutFs, order=5)

    altFront = data['LVDTFL'] / 2 + data['LVDTFR'] / 2
    altRear = data['LVDTRL'] / 2 + data['LVDTRR'] / 2
    cutFsAlt = 5
    data['altFront'] = bandPassFilter(altFront, cutf=cutFsAlt, order=2)
    data['altRear'] = bandPassFilter(altRear , cutf=cutFsAlt, order=2)

    data = data.drop(columns = ['GPSlatHW','GPSlongHW','GPSlatLW','GPSlongLW','max_enable','CAN_ID','CAN_byte[0]' ,'CAN_byte[1]' ,'CAN_byte[2]','CAN_byte[3]','CAN_byte[4]','CAN_byte[5]','CAN_byte[6]', 'CAN_byte[7]', 'A_1','A_4','A_5','A_6','A_9', 'A_1_map','A_4_map','A_5_map','A_6_map', 'LVDTFLmap','LVDTFRmap','LVDTRRmap','LVDTRLmap', 'O_1', 'O_2', 'O_3'])
    data = data.dropna(axis = 1, how = 'all')

    return data


def wcu_equations(data):
    '''
    Take data and process users equations in the entire database, reducing size poping inused columns.
    :param data: pandas dataframe containing data
    :return: pandas dataframe with updated data
    '''

    sensor_data = pd.to_numeric(data['SteeringAngle'])
    sensor_data.loc[sensor_data > 3276.8] = sensor_data.loc[sensor_data > 3276.8] - 6553.6
    data['SteeringAngle'] = sensor_data

    sensor_data = pd.to_numeric(data['ECU_GForceLat'])
    sensor_data.loc[sensor_data > 32.768] = sensor_data.loc[sensor_data > 32.768] - 65.536
    data['ECU_GForceLat'] = sensor_data

    data['time'] = data['time']/1000

    return data


#program gui

def start_app():
    global window, question
    question = ''

    window = tk.Tk()
    window.title("Formula UFSM Desktop APP")
    window.geometry('1080x720')


def call_lic():
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title='Error', message='LICENSE FILE REQUIRED')
    root.destroy()

def error_1_wcu():
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title='Error', message='CANT START, CHECK COM PORT AND ALL OPTIONS AT PROJECTFOLDER/SETTINGS.TXT.')
    root.destroy()

def error_2_wcu():
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title='Error', message='You cant add more then 5 graphics')
    root.destroy()

def warning_1_wcu():
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title='Error', message='You may have CPU delays with this value')
    root.destroy()

def get_update_preference():
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.askquestion('Update Available!', 'Do you wanna update for the next program version?')
    root.destroy()

def getuserselection():
    '''
    Create the first screen to select between WCU, LOG, NCU mode for software
    :return: user selection
    '''

    #define buttons functions
    def WCUBUTTON():
        global question
        question = 'wcu'
        window.destroy()

    def LOGBUTTON():
        global question
        question = 'log'
        window.destroy()

    def NCUBUTTON():
        global question
        question = 'ncu'
        window.destroy()

    btnwcu = tk.Button(window, text='WCU', command=WCUBUTTON, width = 25, height = 3 )
    btnlog = tk.Button(window, text='LOG (.WCU or .NCU FILES)', command=LOGBUTTON, width=25, height=3)
    btnncu = tk.Button(window, text='NCU CAN CSV DATA', command=NCUBUTTON, width=25, height=3)

    btnwcu.grid(column=0, row=10)
    btnlog.grid(column=335, row=10)
    btnncu.grid(column=720-50, row=10)

    #run window
    window.mainloop()

    '''
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports(include_links=False)
    portWCU = ports[0].device

    '''

    return question





# serversocket.py

ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []

def conectServer():
    '''
    create server and configure
    :return: none, just update global values
    '''
    ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    global socketIP, socketPort
    ser.bind((socketIP, socketPort))
    ser.listen()
    ser.settimeout(0.01)

def i_manage_clients(clients, data):
    '''
    function to manage clients
    :param clients: clients array
    :param data: data to send
    :return: none
    '''
    try:
        global rm

        for c in clients:
            rm = c
            b = c.send(bytes(data.encode()))

    except ConnectionError:
        clients.remove(rm)
    except:
        exit('Socket Error')

def sendSocket(data):
    '''
    send data
    :param data: data
    :return: none
    '''
    i_manage_clients(clients, data)
    # Call external function whenever necessary
    try:
        # Add client to list on connection
        client_socket, addr = ser.accept()
        clients.append(client_socket)
    except socket.timeout:
        pass
    except:
        exit('Socket Error')
        raise

#clientsocket

cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conectClient():
    '''
    conect to the server based on settings file
    :return: none
    '''
    global socketIP, socketPort
    cli.connect((socketIP, socketPort))

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
            #tk.messagebox.showwarning(title='Connection Warning', message = 'Server disconect. Close the navegator tab to end the aplication')
            #wcuScreen.endWCU()
            sys.exit('Exit')


# wcuserial

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
    global server,client

    if server == True:
        conectServer()

    if client == True:
        conectClient()
    if client == False:
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
    global server, client
    if(client):
        recieved = clientRecieve().decode().replace('\n','')
        stringSave = recieved.split(',')
        decoded = ',' + ','.join(stringSave[-26:])
    else:
        stringbytes = readStringSerial(readSerial(comport, bytelen=2))
        decoded = decodeCAN(readFloatArraySerial(stringbytes)[1:(1 + 9)], canconfig, laststring)
        stringSave = (stringbytes + decoded).split(',')

    if server:
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
    global server, client, telemetry_points
    global maxrow
    datapoints = telemetry_points

    if client == True:
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

# gauge

def plot_angle_image():
    xdr = Range1d(start=-1, end=1)
    ydr = Range1d(start=-1, end=1)
    plt = figure(x_range=xdr, y_range=ydr, plot_width=300, plot_height=300)
    plt.outline_line_color = None

    #img_path_steering = 'formulaufsm_dataSoftware/static/images/steering.png'
    #img_path_steering = join('E:', 'Git', 'formulaufsm_dataSoftware', 'static', 'images', 'steering.png')
    #image = ImageURL(url=[img_path_steering], x=0, y=0, w=2, global_alpha=1, angle=0, angle_units = 'deg', anchor="center")
    #plt.add_glyph(image)
    image = 0

    text = (Text(x=0, y=0, text=['Steering Angle' + ': ' + str(0) + 'deg'], text_color='black',
                      text_align="center", text_baseline="top", text_font_style="bold"))
    plt.add_glyph(text)

    plt.toolbar.logo = None
    plt.toolbar_location = None
    plt.xaxis.visible = False
    plt.yaxis.visible = False
    plt.xgrid.grid_line_color = None
    plt.ygrid.grid_line_color = None

    return plt, image, text

def plot_text_data(data, unit, name, color):
    xdr = Range1d(start=-1, end=1)
    ydr = Range1d(start=-1, end=1)
    texts = []
    plt = figure(x_range=xdr, y_range=ydr, plot_width=300, plot_height=300)
    plt.outline_line_color = None


    #img_path = join(dirname(__file__), 'static','images','wcu.png')
    #img_path = join('E:','Git', 'formulaufsm_dataSoftware', 'static', 'images', 'wcu.png')
    #print(img_path)
    #image  = ImageURL(url=[img_path], x=0, y=0, w=2, global_alpha=.1, angle=0, angle_units = 'deg', anchor="center")
    #plt.add_glyph(image)

    for i in range(0,len(name)):
        texts.append(Text(x=-1+0.5, y=-0.2*i+0.5, text=[name[i] +': ' + str(data[i]) + unit[i]], text_color=color[i], text_align="left", text_baseline="top", text_font_style="bold"))
        plt.add_glyph(texts[i])

    plt.toolbar.logo = None
    plt.toolbar_location = None
    plt.xaxis.visible = False
    plt.yaxis.visible = False
    plt.xgrid.grid_line_color = None
    plt.ygrid.grid_line_color = None

    return plt, texts

def dt(value):
    """
    Shorthand to override default units with "data", for e.g. `Ray.length`.
    """
    return dict(value=value, units="data")


def speed_to_angle(speed, offset = 0, max_value = 1):
    '''
    Transform values in angle for pointers
    :param speed: data value
    :param offset: minimum possible value for the channel
    :param max_value: maximum possible value for the channel
    :return: angle
    '''
    start_angle = pi + pi / 4
    end_angle = -pi / 4
    speed = speed - offset
    max_value = max_value - offset
    speed = min(max(speed, 0), max_value)
    total_angle = start_angle - end_angle
    angle = total_angle * float(speed) / (max_value)
    return start_angle - angle


def add_needle(plot, speed, offset = 0, max_value = 1):
    angle = speed_to_angle(speed, offset, max_value)
    rmax = Ray(x=0, y=0, length=dt(0.75), angle=angle, line_color="black", line_width=3)
    rmin = Ray(x=0, y=0, length=dt(0.10), angle=angle - pi, line_color="black", line_width=3)
    plot.add_glyph(rmax)
    plot.add_glyph(rmin)
    return rmax, rmin


def polar_to_cartesian(r, alpha):
    return r * cos(alpha), r * sin(alpha)


def add_gauge(plot, radius, max_value, length, direction, color, major_step, minor_step, offset = 0):
    '''
    draw the gauge in plot area
    :param plot:
    :param radius:
    :param max_value:
    :param length:
    :param direction:
    :param color:
    :param major_step:
    :param minor_step:
    :param offset:
    :return:
    '''

    start_angle = pi + pi / 4
    end_angle = -pi / 4

    major_angles, minor_angles = [], []

    total_angle = start_angle - end_angle

    major_angle_step = float(major_step) / max_value * total_angle
    minor_angle_step = float(minor_step) / max_value * total_angle

    major_angle = 0

    while major_angle <= total_angle:
        major_angles.append(start_angle - major_angle)
        major_angle += major_angle_step

    minor_angle = 0

    while minor_angle <= total_angle:
        minor_angles.append(start_angle - minor_angle)
        minor_angle += minor_angle_step

    major_labels = [major_step * i + offset for i, _ in enumerate(major_angles)]

    n = major_step / minor_step
    minor_angles = [x for i, x in enumerate(minor_angles) if i % n != 0]

    glyph = Arc(x=0, y=0, radius=radius, start_angle=start_angle, end_angle=end_angle, direction="clock",
                line_color=color, line_width=2)
    plot.add_glyph(glyph)

    rotation = 0 if direction == 1 else -pi

    x, y = zip(*[polar_to_cartesian(radius, angle) for angle in major_angles])
    angles = [angle + rotation for angle in major_angles]
    source = ColumnDataSource(dict(x=x, y=y, angle=angles))

    glyph = Ray(x="x", y="y", length=dt(length), angle="angle", line_color=color, line_width=2)
    plot.add_glyph(source, glyph)

    x, y = zip(*[polar_to_cartesian(radius, angle) for angle in minor_angles])
    angles = [angle + rotation for angle in minor_angles]
    source = ColumnDataSource(dict(x=x, y=y, angle=angles))

    glyph = Ray(x="x", y="y", length=dt(length / 2), angle="angle", line_color=color, line_width=1)
    plot.add_glyph(source, glyph)

    x, y = zip(*[polar_to_cartesian(radius + 2 * length * direction, angle) for angle in major_angles])
    text_angles = [angle - pi / 2 for angle in major_angles]
    source = ColumnDataSource(dict(x=x, y=y, angle=text_angles, text=major_labels))

    glyph = Text(x="x", y="y", angle="angle", text="text", text_align="center", text_baseline="middle")
    plot.add_glyph(source, glyph)

def plotGauge(speedvalue, offset = 0,
              name = '', unit = '', color = '', maxValue = 0,
              major_step = 2, minor_step = .5):
    '''
    draw a gauge for show online data
    :param speedvalue: data value for a especific channel
    :param offset: offset is the minimum value of the channel
    :param name: name of the channel
    :param unit: units of the data value
    :param color: color of the gauge
    :param maxValue: max value of the chaneel
    :param major_step: step for points inside the gauge
    :param minor_step: step for points inside the gauge
    :return: figure plot in bokeh engine
    '''

    maxValue = maxValue - offset
    xdr = Range1d(start=-1.25, end=1.25)
    ydr = Range1d(start=-1.25, end=1.25)

    renderer = 'webgl'
    plt = Plot(x_range=xdr, y_range=ydr, plot_width=300, plot_height=300, output_backend=renderer,)
    plt.toolbar_location = None
    plt.outline_line_color = None

    plt.add_glyph(Circle(x=0, y=0, radius=1.00, fill_color="white", line_color="black"))
    plt.add_glyph(Circle(x=0, y=0, radius=0.05, fill_color="gray", line_color="black"))

    plt.add_glyph(Text(x=0, y=+0.15, text=[unit], text_color=color, text_align="center", text_baseline="bottom",
                        text_font_style="bold"))

    plt.add_glyph(Text(x=0, y=-0.15, text=[name], text_color="black", text_align="center", text_baseline="top",
                        text_font_style="bold"))

    add_gauge(plt, 0.75, maxValue, 0.05, +1, color, major_step, minor_step, offset = offset)

    valueGliph = Text(x=0, y=-0.6, text=["0"], text_color=color, text_align="center", text_baseline="top")

    plt.add_glyph(valueGliph)

    a, b = add_needle(plt, speedvalue, offset = offset, max_value = maxValue)
    return plt, a, b, valueGliph

# graph

def plot_ncu_graph(title, labels, renderer, graphtools,
                   figure_plots,
                   source,
                   ):
    '''
    create plots customized by programed and users files
    :param title: plot title
    :param labels: plot label in sequence [x,y,y2], can be just [x,y]
    :param renderer: webgl, svg or canvas
    :param graphtools: tools for user analysis the graph
    :param figure_plots: dataframe containing all data for make the plot
    :param source: ColumnDatSource object for bokeh struct
    :return: plot
    '''

    #try:
    global channels_config_propertise
    lines = []
    secondary_axis = False
    for ax_ch in figure_plots['axis']:
        if ax_ch == 'b':
            secondary_axis = True

    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    p = figure(title = title,
               x_axis_label = labels[0],
               y_axis_label = labels[1],
               plot_width = 1400, plot_height = 300,
               toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphtools,
               )

    y_overlimit = 0.05  # show y axis below and above y min and max value
    # FIRST AXIS

    min_all = []
    max_all = []
    for index, figure_plot in figure_plots.iterrows():
        min_all.append(source.data[figure_plot['channel']].min())
        max_all.append(source.data[figure_plot['channel']].max())


    if secondary_axis:

        p.extra_y_ranges = {"b": Range1d( # 0,140
            source.data[figure_plots.iloc[-1, 1]].min() * (1 - y_overlimit),
            source.data[figure_plots.iloc[-1, 1]].max() * (1 + y_overlimit)
        )}
        p.add_layout(LinearAxis(y_range_name='b', axis_label=labels[2]), 'right')

    i=0
    for index, figure_plot in figure_plots.iterrows():

        ch_max = ' | Max: '+ str(int(pd.to_numeric(source.data[figure_plot['channel']]).max()))
        ch_min = ' -- Min: '+ str(int(pd.to_numeric(source.data[figure_plot['channel']]).min()))
        ch_ave = ' | Average: '+ str(int(np.average(pd.to_numeric(source.data[figure_plot['channel']]))))

        leg = figure_plot['legend'] #+ ch_min + ch_ave + ch_max
        color = channels_config_propertise.loc[figure_plot['channel'], 'Color']
        if figure_plot['axis'] == 'b':

            gli = p.line(x=figure_plot['x'], y=figure_plot['channel'], color=color, line_width=figure_plot['line_w'],
                   alpha=figure_plot['alpha'], y_range_name=figure_plot['axis'],
                   source=source,
                         legend_label = leg)
            #lines.append() #, y_range_name=figure_plot['axis']
        else:
            gli = p.line(x=figure_plot['x'], y=figure_plot['channel'], color=color, line_width=figure_plot['line_w'],alpha=figure_plot['alpha'], source=source, legend_label = leg)

    p.toolbar.logo = None
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = '10pt'

    return p

def make_ncu_tabs(source, number_tabs):
    '''

    :param source: ColumnDataSource bokeh object
    :param number_tabs: number of tabs to create in the folder config file, string or int
    :return: array of pannels objects
    '''

    setup_pannel = []
    titles_pannel = []
    numbers_figures_pannel = []



    for i in range(0, int(number_tabs)):
        filetabs = open('projectfolder/configuration/tabs/tab' + str(i) + '/tabSetup.txt')
        setup_pannel.append(filetabs.readlines())
        title_pannel = setup_pannel[i][0].split(':')[1]
        title_pannel = (title_pannel.encode()[:-1]).decode()
        titles_pannel.append(title_pannel)

        number_figures_pannel = setup_pannel[i][1].split(':')[1]
        number_figures_pannel = (number_figures_pannel.encode()[:-1]).decode()
        numbers_figures_pannel.append(number_figures_pannel)
        filetabs.close()

    tabs = []
    for j in range(0, int(number_tabs)):
        gd = []
        for i in range(0, int(numbers_figures_pannel[j])):
            setup = open('projectfolder/configuration/tabs/tab' + str(j) + '/figure' + str(i) + 'Setup.txt')
            setupFigure = setup.readlines()

            setupPlots = pd.read_csv(
                'projectfolder/configuration/tabs/tab' + str(j) + '/figure' + str(i) + 'Plots.csv', sep=';')

            title = setupFigure[0].split(':')[1]
            title = (title.encode()[:-1]).decode()

            labels = setupFigure[1].split(':')[1]
            labels = (labels.encode()[:-1]).decode().split(sep=',')

            renderer = setupFigure[2].split(':')[1]
            renderer = (renderer.encode()[:-1]).decode()
            # Set the Graphic tools for user, this is write in the same order as is showed

            graphtools = setupFigure[3].split(':')[1]
            graphtools = (graphtools.encode()[:-1]).decode()

            # create the figures. set axis, tools and title

            p = plot_ncu_graph(title, labels, renderer, graphtools, setupPlots, source)
            gd.append([p])
            setup.close()

            # create a Gridplot, that allow to combine the plot tools and make a more aligned strcuture of plots
        grid = gridplot(gd, plot_width=1400, plot_height=300, merge_tools=True, toolbar_location='left',
                            sizing_mode='scale_width')
            # , [p1], [p2]

        tabs.append(Panel(child=layout(grid), title=titles_pannel[j], closable=True))
    return tabs

def plot_layout_tab(source, index):
    '''

    :param source: ColumnDataSource bokeh object
    :param number_tabs: number of tabs to create in the folder config file, string or int
    :return: array of pannels objects
    '''

    setup_pannel = ''

    filetabs = open('projectfolder/configuration/tabs/tab' + str(index) + '/tabSetup.txt')
    setup_pannel = filetabs.readlines()
    number_figures_pannel = setup_pannel[1].split(':')[1]
    number_figures_pannel = (number_figures_pannel.encode()[:-1]).decode()
    filetabs.close()

    gd = []
    for i in range(0, int(number_figures_pannel)):
        setup = open('projectfolder/configuration/tabs/tab' + str(index) + '/figure' + str(i) + 'Setup.txt')
        setupFigure = setup.readlines()

        setupPlots = pd.read_csv(
            'projectfolder/configuration/tabs/tab' + str(index) + '/figure' + str(i) + 'Plots.csv', sep=';')

        title = setupFigure[0].split(':')[1]
        title = (title.encode()[:-1]).decode()

        labels = setupFigure[1].split(':')[1]
        labels = (labels.encode()[:-1]).decode().split(sep=',')

        renderer = setupFigure[2].split(':')[1]
        renderer = (renderer.encode()[:-1]).decode()
        # Set the Graphic tools for user, this is write in the same order as is showed

        graphtools = setupFigure[3].split(':')[1]
        graphtools = (graphtools.encode()[:-1]).decode()

        # create the figures. set axis, tools and title

        p = plot_ncu_graph(title, labels, renderer, graphtools, setupPlots, source)
        gd.append([p])
        setup.close()

    for i in range(1, int(number_figures_pannel)):
        gd[i][0].x_range=gd[0][0].x_range

    # create a Gridplot, that allow to combine the plot tools and make a more aligned strcuture of plots
    grid = gridplot(gd, plot_width=1400, plot_height=300, merge_tools=True, toolbar_location='left',
                        sizing_mode='scale_width')
        # , [p1], [p2]
    return layout(grid)



#gps.py


def latlong(data):
    '''
    process gps data for ploting map
    :param data:  pandas dataframe with datavalues
    :return: gps lat and long values
    '''

    #start processing
    sensor_data_a = data['GPSlatHW']
    sensor_data_b = data['GPSlatLW']
    sensor_data_c = data['GPSlongHW']
    sensor_data_d = data['GPSlongLW']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    # make conversion
    gpsLat = ((sensor_data_a-65536) * 65536 + sensor_data_b)/10000000
    gpsLong = ((sensor_data_c-65536) * 65536 + sensor_data_d)/10000000

    return gpsLat, gpsLong

def gps(data, singleplot = False, H=550, W=1000):
    '''
    plot GPS tab
    :param data: pandas dataframe with data
    :param singleplot: if True, plot without legend and return only the bokeh figure
    :param H: Height of plot
    :param W: Width of plot
    :return: bokeh figure or figure, circles and actual circle ploted (for streaming)
    '''
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'
    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    #get processed data
    lat, long = latlong(data)

    #possible filter
    cutFs=2
    #gpsLat = ncuTools.bandPassFilter(gpsLat, cutf=cutFs, order = 2)
    #gpsLong = ncuTools.bandPassFilter(gpsLong, cutf=cutFs, order = 2)

    p = figure(plot_width = W, plot_height = H,
               output_backend=renderer, title = "GPS TRACK", #graphTools = graphTools
               )

    g1 = p.circle(x=lat, y=long, size=3, color = 'gray')

    p.toolbar.logo = None
    p.xaxis.visible = False
    p.yaxis.visible = False

    if singleplot:
        g2 = p.circle(x=lat.iloc[-1:], y=long.iloc[-1:], size=5, color='red')
        return p, g1, g2
    else:
        legend = Legend(items=[
            ('35Hz GPS @MOTEC', [g1]),
        ], location=(0, 0))

        p.add_layout(legend, 'right')

        p.legend.click_policy = 'hide'

        l1 = layout([p])
        tab = Panel(child=l1, title="GPS Tracking", closable=True)
        return tab

#wcuscreen

def endwculog():
    '''
    end log files in WCU mode, compress to save and clear all cache files
    :return: none
    '''

    # close file
    try:
        wcufileglobal.close()
    except:
        pass

    nowsave = datetime.now()

    dt_string = nowsave.strftime("%Y%m%d")

    dt_string2 = nowsave.strftime("%Y%m%d%H%M%S")

    # make save directory
    if os.path.isdir('./finalReport_wcu'):
        pass
    else:
        os.mkdir('./finalReport_wcu')

    path = './finalReport_wcu/' + dt_string

    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)

    # compress log file
    wcu_zip = zipfile.ZipFile(path + '/' + dt_string2 + '.wcu', 'w')
    wcu_zip.write(wcufilename, arcname=dt_string2 + '.csv',
                  compress_type=zipfile.ZIP_DEFLATED)
    wcu_zip.close()

    # clean cache files
    try:
        shutil.rmtree('_wcu_cacheFiles_')
    except:
        pass

    global datapoints, telemetry_points
    datapoints = telemetry_points


def wcushow(doc):
    '''
    bokeh function server
    :param doc: bokeh document
    :return: updated document
    '''
    global colortheme
    doc.theme = colortheme
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'
    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    cabecalho = ''
    channelCounter = 0
    WCUconfig = pd.read_csv('./projectfolder/configuration/dataWCU.csv', sep=';', index_col=False)
    CANconfig = pd.read_csv('./projectfolder/configuration/configCAN.csv', sep=';', index_col=False)

    for channel in WCUconfig['channel']:
        channelCounter = channelCounter + 1
        if (len(WCUconfig) > channelCounter):
            cabecalho = cabecalho + channel + ','
        else:
            cabecalho = cabecalho + channel

    # test temp data folders for wcu
    if os.path.isdir('./_wcu_cacheFiles_'):
        print('./_wcu_cacheFiles_ ok')
    else:
        os.mkdir('./_wcu_cacheFiles_')

    # set COM port baudrate
    global boudrateselected
    baudrate = boudrateselected
    wcuUpdateTimer = 1 / 5  # second -> 1/FPS

    global port
    portWCU = port

    # conect to WDU and clean garbage
    comport = connectSerial(portWCU, baudrate)
    cleanCOMPORT(comport=comport)

    # create csv file for writing WCU data
    global wcufilename
    wcufilename = createCSV(cabecalho)

    time.sleep(2)  # to start serial, requires an delay to arduino load data at the buffer
    # get WDU data

    global data, lastupdate
    lastupdate = '0.0'
    for channel in CANconfig['Channel']:
        lastupdate = lastupdate + ',0.0'

    wcufile = open(wcufilename, "at")
    data, lastupdate = updateWCUcsv(seconds=wcuUpdateTimer, wcufile=wcufile, comport=comport, header=cabecalho,
                                    canconfig=CANconfig, laststr=lastupdate)
    source = ColumnDataSource(data=data)

    # Start Gauges
    gg = 0

    # start variables for an array of gauges
    plot = []
    linemin = []
    linemax = []
    valueglyph = []

    # for each channel listed in the wcucsv that have an 'true' marked on the display column,
    # there will be a plot
    text_data_s = []
    text_unit_s = []
    text_name_s = []
    text_color_s = []
    texts = []
    texplot = figure()
    for channel in WCUconfig['channel']:
        if (len(data[channel]) > 3):  # remove errors
            line = WCUconfig.iloc[gg]
            if (line['display'] == 'gauge'):
                dataValue = pd.to_numeric(data[channel])[len(data[channel]) - 1]
                plt, mx, mi, vg = plotGauge(dataValue, unit=line['unit'], name=channel, color=line['color'],
                                            offset=line['minvalue'], maxValue=line['maxvalue'],
                                            major_step=line['majorstep'], minor_step=line['minorstep'])
                plot.append(plt)
                linemax.append(mx)
                linemin.append(mi)
                valueglyph.append(vg)
            if (line['display'] == 'text'):
                dataValue = pd.to_numeric(data[channel])[len(data[channel]) - 1]
                text_data_s.append(dataValue)
                text_unit_s.append(line['unit'])
                text_name_s.append(channel)
                text_color_s.append(line['color'])

        texplot, texts = plot_text_data(text_data_s, unit=text_unit_s, name=text_name_s, color=text_color_s)
        gg = gg + 1

    # Other main plots
    # GPS:
    track, points, livepoint = gps(data, singleplot=True, H=300, W=300)
    gpssource = points.data_source
    livesource = livepoint.data_source

    # Steering for steering angle
    steering, steering_image, steering_text = plot_angle_image()

    # line plots: secondary tabs
    renderer = 'webgl'
    p = figure(plot_height=300, plot_width=1000, y_range=(0, 13000), title='RPM',
               x_axis_label='s', y_axis_label='rpm', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               )
    g = p.line(x='time', y='RPM', color='red', source=source)
    p.toolbar.logo = None

    # function for update all live gauges and graphics
    global wcufileglobal
    try:
        wcufile.close()
        wcufile = open(wcufilename, "at")
    except:
        pass

    def update_data():
        # t1_start = process_time()
        global data, lastupdate, lastline
        lastline = data.iloc[[data.ndim - 1]].to_csv(header=False, index=False).strip('\r\n')
        data, lastupdate = updateWCUcsv(seconds=wcuUpdateTimer, wcufile=wcufile, comport=comport, header=cabecalho,
                                        canconfig=CANconfig, laststr=lastupdate)

        # t1_stop = process_time()
        # print("HEY: {:.9f}".format((t1_stop - t1_start)))

    def update_source():
        # t1_start = process_time()
        global data
        data = wcu_equations(data)
        source.data = data
        # t1_stop = process_time()
        # print("HEYHEYHEYHEYHEYHEY: {:.9f}".format((t1_stop - t1_start)))

    def callback():
        '''
        callback function to update bokeh server
        :return: none
        '''

        # df = source.to_df()
        # lastline = data.iloc[[df.ndim - 1]].to_csv(header=False, index=False).strip('\r\n')
        # lastupdate = ',' + ','.join(lastline.split(',')[(-len(CANconfig['Channel'])):])

        us = partial(update_source)
        doc.add_next_tick_callback(us)

        ud = partial(update_data)
        doc.add_next_tick_callback(ud)

        global data, lastupdate, lastline

        # alternative method
        # data = source.to_df()
        # lastline = df.iloc[[df.ndim - 1]].to_csv(header=False, index=False).strip('\r\n')
        # lastupdate = ',' + ','.join(lastline.split(',')[(-len(CANconfig['Channel'])):])

        gg = 0
        linectr = 0
        text_values_update = []
        text_unit_s_update = []
        text_name_s_update = []
        for channel in WCUconfig['channel']:
            line = WCUconfig.iloc[gg]
            if (line['display'] == 'gauge'):
                dataValue = pd.to_numeric(data[channel])[len(data[channel]) - 1]
                angle = speed_to_angle(dataValue, offset=line['minvalue'], max_value=line['maxvalue'])
                linemax[linectr].update(angle=angle)
                linemin[linectr].update(angle=angle - pi)
                valueglyph[linectr].update(text=[str(round(dataValue, 1)) + ' ' + line['unit']])
                linectr = linectr + 1

            if (line['display'] == 'text'):
                text_values_update.append(pd.to_numeric(data[channel])[len(data[channel]) - 1])
                text_unit_s_update.append(line['unit'])
                text_name_s_update.append(channel)
            gg = gg + 1

        for i in range(0, len(texts)):
            texts[i].update(text=[text_name_s_update[i] + ': ' + str(text_values_update[i]) + text_unit_s_update[i]])

        steeringangle = pd.to_numeric(data['SteeringAngle'])[len(data['SteeringAngle']) - 1]
        # steering_image.update(angle = steeringangle)
        steering_text.update(text=['Steering Angle' + ': ' + str(steeringangle) + 'deg'])

        lat, long = latlong(data)
        gpssource.data.update(x=lat, y=long)
        livesource.data.update(x=lat.iloc[-1:], y=long.iloc[-1:])

    global per_call
    # per_call = doc.add_periodic_callback(update_source, wcuUpdateTimer*1001)
    per_call = doc.add_periodic_callback(callback, wcuUpdateTimer * 1000)

    '''
    #Button to stop the server

    def exit_callback():
        doc.remove_periodic_callback(per_call)
        endwculog(wcufilename)


    button = Button(label="Stop", button_type="success")
    button.on_click(exit_callback)
    doc.add_root(button)
    '''
    # pre = PreText(text="""Select Witch Channels to Watch""",width=500, height=100)

    global type_graph_option, graph_points_size
    graph_points_size = 2
    type_graph_option = 0

    def addGraph(attrname, old, new):
        '''
        callback function to add graphs figure in the tab area for plotting
        :param attrname:
        :param old: old user selection
        :param new: new user selected channels
        :return: none
        '''

        global old_ch, new_ch
        if len(old) < 5:
            old_ch = old
            new_ch = new
        else:
            new_ch = new

        if len(new) < 5:
            uptab = doc.get_model_by_name('graphtab')
            for channel in old_ch:
                tb = doc.get_model_by_name('graphtab')
                if channel != '':
                    tb.child.children.remove(tb.child.children[len(tb.child.children) - 1])
            for channel in new_ch:
                plot = figure(plot_height=300, plot_width=1300, title=channel,
                              x_axis_label='s', y_axis_label=channel, toolbar_location="below",
                              tooltips=TOOLTIPS,
                              output_backend=renderer,
                              tools=graphTools,
                              name=channel
                              )
                global type_graph_option, graph_points_size

                if type_graph_option == 0:
                    plot.line(x='time', y=channel, color='red', source=source)
                if type_graph_option == 1:
                    plot.circle(x='time', y=channel, color='red', source=source, size=graph_points_size)
                plot.toolbar.logo = None
                uptab.child.children.append(plot)
        else:
            error_2_wcu()

    def radio_group_options(attrname, old, new):
        global type_graph_option
        type_graph_option = new

    OPTIONS_LABEL = ["Line Graph", "Circle Points"]
    radio_group = RadioGroup(labels=OPTIONS_LABEL, active=0)
    radio_group.on_change("active", radio_group_options)

    OPTIONS = cabecalho.split(',')
    multi_select = MultiSelect(value=[''], options=OPTIONS, title='Select Channels', width=300, height=300)
    multi_select.on_change("value", addGraph)

    def update_datapoints(attrname, old, new):
        global telemetry_points
        telemetry_points = new
        if (new > 5000):
            warning_1_wcu()

    datasize_spinner = Spinner(title="Data Points Size", low=1000, high=10000, step=1000, value=1000, width=80)
    datasize_spinner.on_change("value", update_datapoints)

    def update_graph_points_size(attrname, old, new):
        global graph_points_size
        graph_points_size = new

    graph_points_size_spinner = Spinner(title="Circle Size", low=1, high=10, step=1, value=graph_points_size, width=80)
    datasize_spinner.on_change("value", update_graph_points_size)

    # make the grid plot of all gauges at the main tab
    Gauges = gridplot([[plot[0], plot[1], plot[4], plot[3]], [plot[6], plot[2], plot[5], plot[7]],
                       [plot[8], plot[9], plot[10], plot[11]]], toolbar_options={'logo': None})

    # addGraph()
    Graphs = (p)
    layoutGraphs = layout(row(Graphs, multi_select, column(datasize_spinner, radio_group, graph_points_size_spinner)))
    layoutGauges = layout(row(Gauges, column(track, steering, texplot)))

    Gauges = Panel(child=layoutGauges, title="Gauges", closable=True)
    Graphs = Panel(child=layoutGraphs, title="Graphs", closable=True, name='graphtab')

    def cleanup_session(session_context):
        '''
        This function is called when a session is closed: callback function to end WCU Bokeh server
        :return: none
        '''
        endWCU()

    # activate callback to detect when browser is closed
    doc.on_session_destroyed(cleanup_session)

    tabs = Tabs(tabs=[
        Gauges,
        Graphs,
    ], name='WCU TABS')

    doc.add_root(tabs)
    doc.title = 'WCU SCREEN'
    return doc


def endWCU():
    '''
    end WCU server and software
    :return: none
    '''
    # curdoc().remove_periodic_callback(per_call)
    endwculog()  # end and save log
    sys.exit()


def checkall():
    '''
    check if COM Port is conected to run WCU
    :return: boolean
    '''

    try:
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports(include_links=False)
        test = ports[0].device
    except:
        return False

    return True


def runwcu():
    '''
    run WCU Bokeh server
    :return: none
    '''
    global bokehPort
    # check if WCU is ready to run
    if checkall():

        # app = Application(FunctionHandler(wcushow))
        server = Server(
            {'/formulaufsm_dataSoftware': wcushow},

            port=bokehPort,
        )

        server.start()
        server.io_loop.add_callback(server.show, "/")
        server.io_loop.start()
        server.prefix('/formulaufsm_dataSoftware/')

        # alternative form
        # bt = BokehTornado({'/': wcushow})
        # baseserver = BaseServer(server.io_loop, bt, server._http)
        # baseserver.start()
        # baseserver.io_loop.start()

    else:
        # input('CANT START, CHECK COM PORT AND ALL OPTIONS AT PROJECTFOLDER/SETTINGS.TXT.\n\nPress Enter to Exit')
        error_1_wcu()
        sys.exit()

#susphisto
def suspHisto(data):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'

    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    FrontMotionRatio = 1.05
    RearMotionRatio = 0.98

    sensor_data_a = data['LVDTFL']
    sensor_data_b = data['LVDTFR']
    sensor_data_c = data['LVDTRL']
    sensor_data_d = data['LVDTRR']
    sensor_data_e = data['Speed']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)
    sensor_data_e = pd.to_numeric(sensor_data_e)

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    cutFs=1/0.08

    filteredsignal_a = bandPassFilter(sensor_data_a, cutf=int(cutFs), order = 5)
    filteredsignal_b = bandPassFilter(sensor_data_b, cutf=int(cutFs), order = 5)
    filteredsignal_c = bandPassFilter(sensor_data_c, cutf=int(cutFs), order = 5)
    filteredsignal_d = bandPassFilter(sensor_data_d, cutf=int(cutFs), order = 5)

    sensor_data_a = mapDouble(sensor_data_a, 0.59, 0.65, 206, 196)   * FrontMotionRatio
    sensor_data_b = mapDouble(sensor_data_b, 0.9, 0.94, 206, 196)    * FrontMotionRatio
    sensor_data_c = mapDouble(sensor_data_c, 0.92, 1.02, 221, 216)   * RearMotionRatio
    sensor_data_d = mapDouble(sensor_data_d, 0.76, 0.8, 221, 216)    * RearMotionRatio

    #filteredsignal_a = ncuTools.mapDouble(filteredsignal_a, 0.59, 0.65, 206, 196)
    #filteredsignal_b = ncuTools.mapDouble(filteredsignal_b, 0.9, 0.94, 206, 196)
    #filteredsignal_c = ncuTools.mapDouble(filteredsignal_c, 0.92, 1.02, 221, 216)
    #filteredsignal_d = ncuTools.mapDouble(filteredsignal_d, 0.76, 0.8, 221, 216)

    diffdata_a = np.diff(sensor_data_a) / np.diff(sensor_time)
    diffdata_b = np.diff(sensor_data_b) / np.diff(sensor_time)
    diffdata_c = np.diff(sensor_data_c) / np.diff(sensor_time)
    diffdata_d = np.diff(sensor_data_d) / np.diff(sensor_time)

    diffdata_a = bandPassFilter(diffdata_a, cutf=int(cutFs), order=5)
    diffdata_b = bandPassFilter(diffdata_b, cutf=int(cutFs), order=5)
    diffdata_c = bandPassFilter(diffdata_c, cutf=int(cutFs), order=5)
    diffdata_d = bandPassFilter(diffdata_d, cutf=int(cutFs), order=5)

    p1 = figure(title = 'LVDT FL DUMPER HISTOGRAM',output_backend=renderer,tools=graphTools,
               tooltips=TOOLTIPS)
    p2 = figure(title = 'LVDT FR DUMPER HISTOGRAM',output_backend=renderer,tools=graphTools,
               tooltips=TOOLTIPS)
    p3 = figure(title = 'LVDT RL DUMPER HISTOGRAM',output_backend=renderer,tools=graphTools,
               tooltips=TOOLTIPS)
    p4 = figure(title = 'LVDT RR DUMPER HISTOGRAM',output_backend=renderer,tools=graphTools,
               tooltips=TOOLTIPS)

    # Normal Distribution
    hist_a, edges_a = np.histogram(diffdata_a, density=True, bins='auto')
    hist_b, edges_b = np.histogram(diffdata_b, density=True, bins='auto')
    hist_c, edges_c = np.histogram(diffdata_c, density=True, bins='auto')
    hist_d, edges_d = np.histogram(diffdata_d, density=True, bins='auto')

    p1.quad(top=hist_a, bottom=0, left=edges_a[:-1], right=edges_a[1:], fill_color="blue", line_color="blue")
    p2.quad(top=hist_b, bottom=0, left=edges_b[:-1], right=edges_b[1:], fill_color="red", line_color="red")
    p3.quad(top=hist_c, bottom=0, left=edges_c[:-1], right=edges_c[1:], fill_color="orange", line_color="orange")
    p4.quad(top=hist_d, bottom=0, left=edges_d[:-1], right=edges_d[1:], fill_color="green", line_color="green")

    #p1.x_range= Range1d(-300, 300)
    #p2.x_range = Range1d(-300, 300)
    #p3.x_range = Range1d(-300, 300)
    #p4.x_range = Range1d(-300, 300)

    p1.y_range.start = 0
    p2.y_range.start = 0
    p3.y_range.start = 0
    p4.y_range.start = 0

    grid = gridplot([[p1, p2], [p3, p4]], plot_width=700, plot_height=325, merge_tools = True, toolbar_location  = 'left')

    l1 = layout(grid)

    tab = Panel(child=l1, title="Suspension Histogram", closable=True)

    return tab

#logfile

def generateCSVfiles(log, configcan):
    lastupdate = '0'
    for channel in configcan['Channel']:
        lastupdate = lastupdate + ',0'

    cabecalho = ''
    channelCounter = 0
    global channels_config_propertise, ignore_rpm
    for channel in channels_config_propertise['Name']:
        channelCounter = channelCounter + 1
        if (len(channels_config_propertise) > channelCounter):
            cabecalho = cabecalho + channel + ','
        else:
            cabecalho = cabecalho + channel

    print(cabecalho)

    # checkar as virgulas dobradas
    # #cabecalho="time,CAN_ID,CAN_byte[0],CAN_byte[1],CAN_byte[2],CAN_byte[3],CAN_byte[4],CAN_byte[5],CAN_byte[6],CAN_byte[7],,A_1,LVDTFL,LVDTRR,A_4,A_5,A_6,LVDTRL,LVDTFR,A_9,,A_1_map,LVDTFLmap,LVDTRRmap,A_4_map,A_5_map,A_6_map,LVDTRLmap,LVDTFRmap,A_9_map,,O_1,O_2,O_3,,GForceLat,GForceLong,GForceVert,gyro_X,gyro_Y,gyro_z,,ncuTemp,atmelTemp,,sd_bps,fileSize,,max_enable,,TKRR,TKFL,TKRL,TKFR,,,RPM,Gear,BatteryVoltage,OilPressure,Speed,TPS,SteeringAngle,ECU_GForceLat,Lambda,MAP,FuelPressure,BrakePressure,EngineTemp,OilTemp,AirTemp,RadOutTemp,GPSlatHW,GPSlatLW,GPSlongHW,GPSlongLW,PneuDianteiroInner,PneuDianteiroCenter,PneuDianteiroOuter,PneuTraseiroInner,PneuTraseiroCenter,PneuTraseiroOuter,\n"

    rpmflag = False
    csvfile = open(log, 'rb').readlines()
    filename = 0
    maximumline = 80000
    counterline = 0
    j = 1
    f = open('_ncu_cacheFiles_/logFinal_part_' + str(filename) + '.csv', "w")
    f.writelines(cabecalho)
    lineL = ['0', '0']
    print('Starting file:' + str(filename))
    for i in range(len(csvfile)):
        exp = True
        try:
            line = csvfile[i].decode("utf-8")
        except:
            exp = False
            print('Exception')
        finally:
            if exp and (i > 2):
                line = csvfile[i].decode("utf-8")
                lineS = line.split(',')
                if (len(lineS) == 56):
                    lineS[55] = ''
                    if (lineS[0] != 't'):
                        exp1 = True
                        exp2 = True
                        try:
                            for vartry in range(0, len(lineS)):
                                if (vartry != 10) & (vartry != 20) & (vartry != 30) & (vartry != 34) & (
                                        vartry != 41) & (vartry != 44) & (vartry != 47) & (vartry != 49) & (
                                        vartry != 51) & (vartry != 55):
                                    a = float(lineS[vartry])
                        except:
                            exp1 = False
                            print('exeption')
                            print(lineS)
                        finally:
                            try:
                                for vartry1 in range(0, len(lineL)):
                                    if (vartry1 != 10) & (vartry1 != 20) & (vartry1 != 30) & (vartry1 != 34) & (
                                            vartry1 != 41) & (vartry1 != 44) & (vartry1 != 47) & (vartry1 != 49) & (
                                            vartry1 != 51) & (vartry1 != 55):
                                        b = float(lineL[vartry1])
                            except:
                                exp2 = False
                            finally:
                                if exp1 & exp2:
                                    var1 = float(lineS[0])
                                    var2 = float(lineL[0])
                                    if float(lineS[1]) == 1000:
                                        if (float(lineS[2]) * 256 + float(lineS[3])) > 0:
                                            rpmflag = True
                                        else:
                                            rpmflag = False
                                    if rpmflag | ignore_rpm:
                                        CAN = decodeCAN(lineS[1:10], configcan, lastupdate)
                                        lastupdate = CAN
                                        if var1 < var2:
                                            filename = filename + 1
                                            counterline = 0
                                            f = open('_ncu_cacheFiles_/logFinal_part_' + str(filename) + '.csv', "w")
                                            f.writelines(cabecalho)
                                            print('Starting file:' + str(filename))
                                        if counterline > maximumline:
                                            filename = filename + 1
                                            counterline = 0
                                            f = open('_ncu_cacheFiles_/logFinal_part_' + str(filename) + '.csv', "w")
                                            f.writelines(cabecalho)
                                            print('Starting file:' + str(filename))

                                        f.writelines(','.join(lineS))
                                        f.writelines(CAN + ',\n')
                                        counterline = counterline + 1
                                        lineL = lineS
    return filename


def parseLogFile():
    CANconfig = pd.read_csv('./projectfolder/configuration/configCAN.csv', sep=';', index_col=False)
    # datetime object containing current date and time
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.iconbitmap("./projectfolder/icon.ico")
    root.withdraw()

    file_path_string = filedialog.askopenfilename(initialdir="./logs", title="Select Original CSV NCU log file",
                                                  filetypes=[("CSV file", "*.csv")])
    logFileCSV = 'LOG.CSV'

    # filecounter = generateCSVfiles('logs/' + logFileCSV)
    if (file_path_string != ''):
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")

        if os.path.isdir('./_ncu_cacheFiles_'):
            # print('_ncu_cacheFiles_ ok')
            pass
        else:
            os.mkdir('_ncu_cacheFiles_')

        if os.path.isdir('./finalReport_ncu'):
            # print('finalReport_ncu ok')
            pass
        else:
            os.mkdir('./finalReport_ncu')

        path = 'finalReport_ncu/' + dt_string
        os.mkdir(path)

        filecounter = generateCSVfiles(file_path_string, CANconfig)
        for var in range(0, filecounter + 1):
            csv_zip = zipfile.ZipFile(path + '/logFinal_part_' + str(var) + '.ncu', 'w')
            csv_zip.write('_ncu_cacheFiles_/logFinal_part_' + str(var) + '.csv',
                          arcname='logFinal_part_' + str(var) + '.csv', compress_type=zipfile.ZIP_DEFLATED)
            csv_zip.close()

        for var in range(0, filecounter + 1):
            os.remove(os.path.realpath('_ncu_cacheFiles_/logFinal_part_' + str(var) + '.csv'))

        shutil.move(file_path_string, path + '/' + logFileCSV)
        shutil.rmtree('_ncu_cacheFiles_')


#ncuopenreport

def startNCU():
    '''
    start NCU oppening files
    :return: none
    '''
    import tkinter as tk
    from tkinter import filedialog

    # Allows the program to clean memory in the program

    gc.enable()

    root = tk.Tk()
    root.iconbitmap("./projectfolder/icon.ico")
    root.withdraw()

    # Get the NCU file to start descompression
    file_path_string_s = filedialog.askopenfilenames(initialdir="./finalReport_ncu", title="Select NCU Log file",
                                                     filetypes=[("NCU file @Formula UFSM", "*.ncu"),
                                                                ("WCU file @Formula UFSM", "*.wcu"),
                                                                ("csv file", "*.csv")])
    # names to get multiples archive
    # If someone file is selected, then:
    all_data = []
    for file_path_string in file_path_string_s:

        # Get the ID of the log File. ID is the number on the file name.
        print(file_path_string)
        num = re.findall(r'\d+', file_path_string)
        l = num[len(num) - 1]

        # Check if the correct directory exists inside the root folder, if not, create new folders.

        if os.path.isdir('./_ncu_cacheFiles_'):
            pass #print('_ncu_cacheFiles_ ok')
        else:
            #print('creating directory...')
            os.mkdir('./_ncu_cacheFiles_')

        if os.path.isdir('./finalReport_ncu'):
            pass #print('finalReport_ncu ok')
        else:
            #print('creating directory...')
            os.mkdir('./finalReport_ncu')

        logFileCSV = 'logFinal_part_' + str(l) + '.csv'

        logFileCSVrar = 'logFinal_part_' + str(l) + '.ncu'

        file_suffix = pathlib.Path(file_path_string).suffix

        global go
        go = False
        if (file_suffix == '.ncu'):

            ziplog = zipfile.ZipFile(file_path_string)

            # Try descompressing NCU file to get the CSV file

            go = False
            for file in ziplog.namelist():
                if ziplog.getinfo(file).filename == logFileCSV:
                    all_data.append(pd.read_csv(ziplog.extract(file, '_ncu_cacheFiles_/' + logFileCSV)))
                    go = True
                else:
                    print('error descompressing csv file')

        if (file_suffix == '.wcu'):

            ziplog = zipfile.ZipFile(file_path_string)

            # Try descompressing NCU file to get the CSV file

            go = False
            for file in ziplog.namelist():
                all_data.append(pd.read_csv(ziplog.extract(file, '_ncu_cacheFiles_/' + logFileCSV)))
                go = True

        if (file_suffix == '.csv'):
            all_data.append(pd.read_csv(file_path_string))

            go = True

    lasttime = 0
    dts = []
    for dt in all_data:
        dt['time'] = dt['time'] - dt.iloc[0, 0] + lasttime
        lasttime = dt.iloc[-1, 0]
        dts.append(dt)

    global data
    data = pd.concat(dts, ignore_index=True)
    #remove the temporary folder
    shutil.rmtree('_ncu_cacheFiles_')

def openLog(doc):
    '''

    :param doc:
    :return: document
    '''
    global colortheme
    doc.theme = colortheme

    global data
    try:
        data = user_equations(data)
    except:
        print("Bad user equations, contact developer for erro code #03")
    #with pd.option_context('display.max_columns', None):  # more options can be specified also
    #    print(data)

    #atention to not overflow bokeh server starting
    maxSizeArray = 80000

    if maxSizeArray > len(data['time']):
        maxSizeArray = len(data['time'])-1

    last_t = 0
    for index, df in data.iterrows():
        t=df['time']
        if t-last_t>150:
            remove_time = t-last_t
            print('Developer note: difftime: ' + str((t-last_t)/1000) + ' on data point time: ' + str(t/1000) + '. Index: ' + str(index))
            data.iloc[index:,data.columns.get_loc("time")] -= remove_time
        last_t = t


    data['time'] = data['time']/1000
    source = ColumnDataSource(data=data.iloc[0:maxSizeArray,:])

    ##################### TIMER SLIDER GLOBAL ######################
    def update(event):
        '''
        callback for button to upgrade plots
        :param event: handler
        :return: none
        '''
        new = time_slider.value
        min_index = 0
        max_index = len(data['time'])
        for j in range(0, int(len(data['time'])/1000)):
            if data['time'].iloc[j*1000] > new[0]:
                min_index = j*1000
                break

        for j in range(0, int(len(data['time'])/1000)):
            if data['time'].iloc[j*1000] > new[1]:
                max_index = j*1000
                break

        #to block max size of source
        #if max_index-min_index > maxSizeArray:
        #    max_index = min_index + maxSizeArray
        #    time_slider.value = [data['time'].iloc[min_index], data['time'].iloc[maxSizeArray]]
        try:
            source.data = ColumnDataSource.from_df(data.iloc[min_index:max_index, :])
        except:
            print("Cotact developer: Error code #2")

    btn_update = Button(label = 'Update', button_type="success", width_policy='min')#, width_policy='min', button_type='primary')
    btn_update.on_click(update)
    time_slider = RangeSlider(value=(data['time'].min(), data['time'].iloc[maxSizeArray]), start=data['time'].min(), end=data['time'].max(), step=10, title="Timing Data", default_size = 1300)

    def end(event):
        '''
        callback function button for end program
        :param event:
        :return: none
        '''
        sys.exit()

    btn_end = Button(label='Exit', button_type="success", width_policy='min')  # , width_policy='min', button_type='primary')
    btn_end.on_click(end)

    doc.add_root(row(btn_update, time_slider, btn_end))
    #Check if descompressed file have an CSV named correctly inside

    setup_tabs = open('projectfolder/configuration/tabs/globalSetup.txt').readlines()
    title_tabs = setup_tabs[0].split(':')[1]
    #title_tabs = (title_tabs.encode()[:-2]).decode()

    number_tabs = setup_tabs[1].split(':')[1]
    #number_tabs = (number_tabs.encode()[:-2]).decode()

    global go
    if go:

        #if (len(data.columns) == 83):
        if (True):
            '''
            #Configure the HTML final to the output graphics
            logHTMLFile = 'finalReport_ncu/logFinal_part_' + str(l) + '.html'

            output_file(logHTMLFile, title='NCU LOG ' + str(l) + ' | FORMULA UFSM')

            curdoc().theme = 'dark_minimal'

            #Get each tab pannel to render the HTML file

            tab0 = pilot(data)
            tab1 = BAT(data)
            tab2 = LVDT(data)
            tab3 = TK(data)
            tab4 = mpu6050(data)
            tab5 = suspFFT(data)
            tab6 = suspHisto(data)
            tab7 = gps(data)
            tab8 = ncu(data)
            tab9 = engine(data)
            tab10 = tireTemp(data)
            '''

            # Join tabs
            tabs = Tabs(tabs=make_ncu_tabs(source, number_tabs), name=title_tabs)

            '''
            #for ensure the program, try to save the file with the tabs.
            canShow = True
            try:
                save(tabs)
            except:
                print("Error... contact developer for error code #01")
                canShow = False

            #if not get exception, display the HTML
            if(canShow):
                show(tabs)

                #remove the full HTML archive to clean disk space, HTML files is higher
                time.sleep(10)
                os.remove(logHTMLFile)
            '''
            doc.add_root(tabs)

            doc.title = 'NCU LOG'

        wculogcol = pd.read_csv('./projectfolder/configuration/dataWCU.csv').shape[0] #number of lines indicates the number of collumn in a log file
        if ((data.shape[1]) == wculogcol):
            # Configure the HTML final to the output graphics
            #logHTMLFile = 'finalReport_ncu/logWCU.html'

            #output_file(logHTMLFile, title='LOG WCU | FORMULA UFSM')

            # curdoc().theme = 'dark_minimal'

            # Get each tab pannel to render the HTML file
            #tab0 = pilot(data)
            #tab7 = gps(data)
            #tab9 = engine(data)
            #tab10 = tireTemp(data)

            # Join tabs
            #tabs = Tabs(tabs=[
            #    tab0,
            #    tab9,
            #    tab7,
            #    tab10,
            #], name='WCU TABS')

            '''
            # for ensure the program, try to save the file with the tabs.
            canShow = True
            try:
                save(tabs)
            except:
                print("Error... contact developer for error code #01")
                canShow = False

            # if not get exception, display the HTML
            if (canShow):
                show(tabs)

                # remove the full HTML archive to clean disk space, HTML files is higher
                time.sleep(10)
                os.remove(logHTMLFile)
            '''

            doc.add_root(tabs)
            doc.title = 'WCU LOG'

    return doc

def runLogAnalysis():
    global bokehPort
    server = Server(
        {'/': openLog},
        port = bokehPort,
    )
    server.start()
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()


    # alternative bokeh server form
    # bt = BokehTornado({'/': wcushow})
    # baseserver = BaseServer(server.io_loop,bt,server._http)
    # baseserver.start()
    # baseserver.io_loop.start()

    # chck if the user want to open another log file
    if tk.messagebox.askyesno("Question","Do you want to open another file?"):
        restart_program()


#lic.py
def checkLicense():
    '''
    check if licese file is saved with aplication folder to alow user run the app
    :return: boolean
    '''
    try:
        file = open('./LICENSE', 'r')
    except:
        return False

    return True


# main file
if True:
    start_app()

    program_version = '3.2'

    '''
    from update_check import isUpToDate, update
    if isUpToDate('./README.MD', "https://raw.githubusercontent.com/Eugenio-Pozzobon/Formula-UFSM-Data-Analysis/master/README.MD") == False:
       if programGui.get_update_preference():
           update('./README.MD', "https://raw.githubusercontent.com/Eugenio-Pozzobon/Formula-UFSM-Data-Analysis/master/README.MD")
    
    '''

    # enable RAM cleaner
    gc.enable()

    # get program settings
    init()

    # check if user has license
    if checkLicense():

        # get user mode selection
        screen = getuserselection()

        # run
        if screen == 'wcu':
            runwcu()
        if screen == 'ncu':
            parseLogFile()
        if screen == 'log':
            startNCU() # file selection and descompression
            runLogAnalysis() # file analysis

    else:
        #System out message
        #input('LICENSE FILE REQUIRED\n\nPress Enter to Exit')
        call_lic()
        sys.exit()
#--------