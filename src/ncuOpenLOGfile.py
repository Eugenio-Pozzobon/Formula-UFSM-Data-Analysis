import time
import zipfile
import os
import shutil
import sys
import gc
from datetime import datetime
import time

import dask.dataframe as dd
import dask.array as da
import csv
import decimal
import src.programTools

def generateCSVfiles(log):
    RPM=',0'
    Gear=',0'
    BatteryVoltage=',0'
    OilPressure=',0'
    Speed=',0'
    TPS=',0'
    SteeringAngle=',0'
    ECU_GForceLat=',0'
    Lambda=',0'
    MAP=',0'
    FuelPressure=',0'
    BrakePressure=',0'
    EngineTemp=',0'
    OilTemp=',0'
    AirTemp=',0'
    RadOutTemp=',0'
    GPSlatHW=',0'
    GPSlatLW=',0'
    GPSlongHW=',0'
    GPSlongLW=',0'
    PneuDianteiroInner=',0.0'
    PneuDianteiroCenter=',0.0'
    PneuDianteiroOuter=',0.0'
    PneuTraseiroInner=',0.0'
    PneuTraseiroCenter=',0.0'
    PneuTraseiroOuter=',0.0'
    cabecalho="time,CAN_ID,CAN_byte[0],CAN_byte[1],CAN_byte[2],CAN_byte[3],CAN_byte[4],CAN_byte[5],CAN_byte[6],CAN_byte[7],,A_1,LVDTFL,LVDTRR,A_4,A_5,A_6,LVDTRL,LVDTFR,A_9,,A_1_map,LVDTFLmap,LVDTRRmap,A_4_map,A_5_map,A_6_map,LVDTRLmap,LVDTFRmap,A_9_map,,O_1,O_2,O_3,,GForceLat,GForceLong,GForceVert,gyro_X,gyro_Y,gyro_z,,ncuTemp,atmelTemp,,sd_bps,fileSize,,max_enable,,TKRR,,TKRL,TKFR,TKFL,,RPM,Gear,BatteryVoltage(V),OilPressure(bar),Speed(Km/h),TPS,SteeringAngle(deg),ECU_GForceLat(G),Lambda,MAP(kpa),FuelPressure(bar),BrakePressure(bar),EngineTemp(C),OilTemp(C),AirTemp(C),RadOutTemp(C),GPSlatHW,GPSlatLW,GPSlongHW,GPSlongLW,PneuDianteiroInner,PneuDianteiroCenter,PneuDianteiroOuter,PneuTraseiroInner,PneuTraseiroCenter,PneuTraseiroOuter,\n"
    rpmflag = False
    csvfile = open(log, 'rb').readlines()
    filename = 0
    maximumline = 80000
    counterline = 0
    j = 1
    f = open('_ncu_cacheFiles_/logFinal_part_' + str(filename) + '.csv', "w")
    f.writelines(cabecalho)
    lineL = ['0', '0']
    print('Starting file:' +str(print(filename)))
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
                if(len(lineS) == 56):
                    lineS[55] = ''
                    if (lineS[0] != 't'):
                        exp1 = True
                        exp2 = True
                        try:
                            for vartry in range(0, len(lineS)):
                                if (vartry != 10) & (vartry != 20) & (vartry != 30) & (vartry != 34) & (vartry != 41)& (vartry != 44)& (vartry != 47)& (vartry != 49)& (vartry != 51)& (vartry != 55):
                                    a=float(lineS[vartry])
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
                                        b=float(lineL[vartry1])
                            except:
                                exp2 = False
                            finally:
                                if exp1 & exp2:
                                    var1 = float(lineS[0])
                                    var2 = float(lineL[0])
                                    if float(lineS[1]) == 1000 :
                                        if (float(lineS[2])*256+float(lineS[3])) > 0:
                                            rpmflag = True
                                        else :
                                            rpmflag = False
                                    if rpmflag:
                                        CAN = decodeCAN(lineS)
                                        if var1 < var2:
                                            filename = filename + 1
                                            counterline = 0
                                            f = open('_ncu_cacheFiles_/logFinal_part_' + str(filename) + '.csv', "w")
                                            f.writelines(cabecalho)
                                            print('Starting file:' +str(filename))
                                        if counterline > maximumline:
                                            filename = filename + 1
                                            counterline = 0
                                            f = open('_ncu_cacheFiles_/logFinal_part_' + str(filename) + '.csv', "w")
                                            f.writelines(cabecalho)
                                            print('Starting file:' +str(filename))

                                        f.writelines(','.join(lineS))
                                        f.writelines(CAN+',\n')
                                        counterline = counterline + 1
                                        lineL = lineS
    return filename


def parseLogFile():

    # datetime object containing current date and time
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.iconbitmap("./projectfolder/icon.ico")
    root.withdraw()

    file_path_string = filedialog.askopenfilename(initialdir = "./logs",title = "Select Original CSV NCU log file",filetypes=[("CSV file","*.csv")])
    print(file_path_string)
    logFileCSV='LOG.CSV'

    #filecounter = generateCSVfiles('logs/' + logFileCSV)
    if(file_path_string != ''):
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")

        if os.path.isdir('./_ncu_cacheFiles_'):
            print('_ncu_cacheFiles_ ok')
        else:
            os.mkdir('_ncu_cacheFiles_')

        if os.path.isdir('./finalReport_ncu'):
            print('finalReport_ncu ok')
        else:
            os.mkdir('./finalReport_ncu')

        path = 'finalReport_ncu/' + dt_string
        os.mkdir(path)

        filecounter = generateCSVfiles(file_path_string)
        for var in range(0,filecounter+1):
            csv_zip = zipfile.ZipFile(path+'/logFinal_part_'+str(var)+'.ncu', 'w')
            csv_zip.write('_ncu_cacheFiles_/logFinal_part_' + str(var) + '.csv', arcname='logFinal_part_' + str(var) + '.csv', compress_type=zipfile.ZIP_DEFLATED)
            csv_zip.close()

        for var in range(0, filecounter+1):
            os.remove(os.path.realpath('_ncu_cacheFiles_/logFinal_part_' + str(var) + '.csv'))

        shutil.move(file_path_string, path + '/' + logFileCSV)
        shutil.rmtree('_ncu_cacheFiles_')
