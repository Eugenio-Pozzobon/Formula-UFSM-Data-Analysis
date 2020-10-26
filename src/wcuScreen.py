from bokeh.plotting import figure, output_file
from bokeh.layouts import row, column, layout
from bokeh.io import curdoc
from bokeh.models import Arc, Circle, ColumnDataSource, Plot, Range1d, Ray, Text
from bokeh.io import save, show, curdoc
from bokeh.plotting import figure, output_file
from bokeh.models.widgets import Tabs, Panel
from bokeh.themes import built_in_themes

from math import cos, pi, sin
import time, threading
import pandas as pd
import os, gc

from src.programGui import *
from src.wcuSerial import *
from src.gauges import *

cabecalho="time,CAN_ID,CAN_byte[0],CAN_byte[1],CAN_byte[2],CAN_byte[3],CAN_byte[4],CAN_byte[5],CAN_byte[6],CAN_byte[7],RPM,Gear,BatteryVoltage(V),OilPressure(bar),Speed(Km/h),TPS,SteeringAngle(deg),ECU_GForceLat(G),Lambda,MAP(kpa),FuelPressure(bar),BrakePressure(bar),EngineTemp(C),OilTemp(C),AirTemp(C),RadOutTemp(C),GPSlatHW,GPSlatLW,GPSlongHW,GPSlongLW,PneuDianteiroInner,PneuDianteiroCenter,PneuDianteiroOuter,PneuTraseiroInner,PneuTraseiroCenter,PneuTraseiroOuter"

def wcushow():
    # test temp data folders for wcu
    if os.path.isdir('./_wcu_cacheFiles_'):
        print('./_wcu_cacheFiles_ ok')
    else:
        os.mkdir('./_wcu_cacheFiles_')

    #set COM port baudrate
    baudrate = '115200'
    wcuUpdateTimer = 1 #second

    #list ports in hardware
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports(include_links=False)
    portWCU = ports[0].device
    print(portWCU)

    #conect to WDU and clean garbage
    comport = connectSerial(portWCU, baudrate)
    cleanCOMPORT(comport=comport)

    #create csv file for writing WCU data
    wcufilename = createCSV(cabecalho)

    #get WDU data
    data = updateWCUcsv(seconds = wcuUpdateTimer, wcufilename = wcufilename, comport = comport, header=cabecalho)
    source = ColumnDataSource(data=data)

    #Start plots
    renderer = 'webgl'
    p = figure(plot_height=300, plot_width=1000)
    p.line(x='time', y='RPM', source=source)

    ##COMO AUTOMATIZAR??????????????????????????????
    ##CHECAR VALORES ZERÁVEIS QUE N DEVERIAM ZERAR NA CONVERSÃO CAN
    ## TESTAR CONVERSÃO CAN PELO NCU!
    speed = pd.to_numeric(data['Speed(Km/h)'])[len(data['Speed(Km/h)']) - 1]
    rpm= pd.to_numeric(data['RPM'])[len(data['RPM']) - 1]
    plotspeed, spdlinemax, spdlinemin = plotGauge(speed, unit = 'km/h', name = 'Speed', color = 'blue', maxValue = 150, major_step = 25, minor_step = 5)
    plotrpm, rpmlinemax, rpmlinemin = plotGauge(rpm, unit='rpm', name='RPM', color='red', maxValue=13000,
                                                  major_step=3000, minor_step=500)

    def callback():
        data = updateWCUcsv(seconds=wcuUpdateTimer, wcufilename=wcufilename, comport=comport, header=cabecalho)
        source.data=data

        speed = pd.to_numeric(data['Speed(Km/h)'])[len(data['Speed(Km/h)'])-1]
        angle = speed_to_angle(speed, "kmh", offset = 0, max_value = 150)
        spdlinemax.update(angle = angle)
        spdlinemin.update(angle = angle - pi)


        rpm = pd.to_numeric(data['RPM'])[len(data['RPM'])-1]
        angle = speed_to_angle(rpm, "rpm", offset = 0, max_value = 13000)
        rpmlinemax.update(angle = angle)
        rpmlinemin.update(angle = angle - pi)

        ##COMO AUTOMATIZAR??????????????????????????????

        print(rpm)

    curdoc().add_periodic_callback(callback, 2000)

    layoutGauges = row(plotrpm, plotspeed)
    layoutGraphs = row(p)

    Gauges = Panel(child=layoutGauges, title="Gauges", closable=True)
    Graphs = Panel(child=layoutGraphs, title="Graphs", closable=True)

    tabs = Tabs(tabs=[
                    Gauges,
                    Graphs,
                ], name='WCU TABS')

    curdoc().add_root(tabs)
    curdoc().title = 'WCU SCREEN'