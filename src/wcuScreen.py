# Author: Eugênio Pozzobon
# e-mail: eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

from bokeh.plotting import figure, output_file
from bokeh.layouts import row, column, layout
from bokeh.io import curdoc
from bokeh.models import Arc, Circle, ColumnDataSource, Plot, Range1d, Ray, Text, ImageURL, Image
from bokeh.io import save, show, curdoc
from bokeh.plotting import figure, output_file
from bokeh.models import ImageURL
from bokeh.models.widgets import Tabs, Panel
from bokeh.themes import built_in_themes
from bokeh.layouts import gridplot
from bokeh.server.server import Server, BaseServer
from bokeh.server.tornado import BokehTornado
from bokeh.models.widgets import Button
from bokeh.models import CustomJS, MultiSelect
from bokeh.models import PreText

from math import cos, pi, sin
import time, threading
import pandas as pd
import os, gc, sys
from datetime import datetime

import src.settings as settings
from src.programGui import *
from src.server_lifecycle import *
from src.wcuSerial import *
from src.gauges import *
from src.graph import *
from src.tabGPS import *

from time import process_time
from functools import partial

def endwculog():
    '''
    end log files in WCU mode, compress to save and clear all cache files
    :return: none
    '''

    #close file
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

    #clean cache files
    try:
        shutil.rmtree('_wcu_cacheFiles_')
    except:
        pass

    global datapoints
    datapoints = settings.telemetry_points

def wcushow(doc):
    '''
    bokeh function server
    :param doc: bokeh document
    :return: updated document
    '''
    doc.theme = settings.colortheme
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

    #set COM port baudrate
    baudrate = settings.boudrateselected
    wcuUpdateTimer = 1/5#second -> 1/FPS

    portWCU = settings.port

    #conect to WDU and clean garbage
    comport = connectSerial(portWCU, baudrate)
    cleanCOMPORT(comport=comport)

    #create csv file for writing WCU data
    global wcufilename
    wcufilename = createCSV(cabecalho)

    time.sleep(2) #to start serial, requires an delay to arduino load data at the buffer
    #get WDU data

    global data, lastupdate
    lastupdate = '0.0'
    for channel in CANconfig['Channel']:
        lastupdate = lastupdate + ',0.0'

    wcufile = open(wcufilename, "at")
    data, lastupdate = updateWCUcsv(seconds = wcuUpdateTimer, wcufile = wcufile, comport = comport, header=cabecalho, canconfig= CANconfig, laststr = lastupdate)
    source = ColumnDataSource(data=data)

    # Start Gauges
    gg = 0

    #start variables for an array of gauges
    plot = []
    linemin = []
    linemax = []
    valueglyph = []

    #for each channel listed in the wcucsv that have an 'true' marked on the display column,
    # there will be a plot
    text_data_s = []
    text_unit_s = []
    text_name_s = []
    text_color_s = []
    texts = []
    texplot = figure()
    for channel in WCUconfig['channel']:
        line = WCUconfig.iloc[gg]
        if(line['display'] == 'gauge'):
            dataValue = pd.to_numeric(data[channel])[len(data[channel]) - 1]
            plt, mx, mi, vg = plotGauge(dataValue, unit = line['unit'], name = channel, color = line['color'], offset = line['minvalue'], maxValue = line['maxvalue'], major_step = line['majorstep'], minor_step = line['minorstep'])
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

        texplot, texts = plot_text_data(text_data_s, unit = text_unit_s, name = text_name_s, color = text_color_s)
        gg = gg + 1


    # Other main plots
    #GPS:
    track, points, livepoint = gps(data, singleplot = True, H = 300, W = 300)
    gpssource = points.data_source
    livesource = livepoint.data_source

    #Steering for steering angle
    steering, steering_image, steering_text = plot_angle_image()

    # line plots: secondary tabs
    renderer = 'webgl'
    p = figure(plot_height=300, plot_width=1000, y_range=(0, 13000), title = 'RPM',
               x_axis_label = 's', y_axis_label = 'rpm', toolbar_location="below",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               )
    g = p.line(x='time', y='RPM', color = 'red', source=source)
    p.toolbar.logo = None

    #function for update all live gauges and graphics
    global wcufileglobal
    try:
        wcufile.close()
        wcufile = open(wcufilename, "at")
    except:
        pass

    def update_data():
        t1_start = process_time()
        global data, lastupdate, lastline
        lastline = data.iloc[[data.ndim - 1]].to_csv(header=False, index=False).strip('\r\n')
        data, lastupdate = updateWCUcsv(seconds=wcuUpdateTimer, wcufile=wcufile, comport=comport, header=cabecalho, canconfig= CANconfig, laststr = lastupdate)
        t1_stop = process_time()
        print("HEY: {:.9f}".format((t1_stop - t1_start)))

    def update_source():
        t1_start = process_time()
        source.data = data
        t1_stop = process_time()
        print("HEYHEYHEYHEYHEYHEY: {:.9f}".format((t1_stop - t1_start)))


    def callback():
        '''
        callback function to update bokeh server
        :return: none
        '''

        #df = source.to_df()
        #lastline = data.iloc[[df.ndim - 1]].to_csv(header=False, index=False).strip('\r\n')
        #lastupdate = ',' + ','.join(lastline.split(',')[(-len(CANconfig['Channel'])):])
        us = partial(update_source)
        doc.add_next_tick_callback(us)

        ud = partial(update_data)
        doc.add_next_tick_callback(ud)


        #wcufile = open(wcufilename, "at")
        global data, lastupdate, lastline
        #wcufile.close()

        #graph_points = 500
        #if(len(data)>(graph_points+5)):
        #    source.data=data.iloc[len(data)-graph_points:]
        #else:
        #    source.data = data

        #alternative method
        #data = source.to_df()
        #lastline = df.iloc[[df.ndim - 1]].to_csv(header=False, index=False).strip('\r\n')
        #lastupdate = ',' + ','.join(lastline.split(',')[(-len(CANconfig['Channel'])):])

        gg = 0
        linectr = 0
        text_values_update = []
        text_unit_s_update = []
        text_name_s_update = []
        for channel in WCUconfig['channel']:
            line = WCUconfig.iloc[gg]
            if (line['display'] == 'gauge'):
                dataValue = pd.to_numeric(data[channel])[len(data[channel])-1]
                angle = speed_to_angle(dataValue, offset = line['minvalue'], max_value = line['maxvalue'])
                linemax[linectr].update(angle = angle)
                linemin[linectr].update(angle = angle - pi)
                valueglyph[linectr].update(text = [str(round(dataValue, 1)) + ' ' + line['unit']])
                linectr = linectr + 1

            if (line['display'] == 'text'):
                text_values_update.append(pd.to_numeric(data[channel])[len(data[channel]) - 1])
                text_unit_s_update.append(line['unit'])
                text_name_s_update.append(channel)
            gg = gg + 1

        for i in range(0, len(texts)):
            texts[i].update(text=[text_name_s_update[i] +': ' + str(text_values_update[i]) + text_unit_s_update[i]])


        steeringangle = pd.to_numeric(data['SteeringAngle'])[len(data['SteeringAngle'])-1]
        #steering_image.update(angle = steeringangle)
        steering_text.update(text=['Steering Angle' + ': ' + str(steeringangle) + 'deg'])

        lat, long = latlong(data)
        gpssource.data.update(x=lat, y=long)
        livesource.data.update(x=lat.iloc[-1:], y=long.iloc[-1:])

    global per_call
    #per_call = doc.add_periodic_callback(update_source, wcuUpdateTimer*1001)
    per_call = doc.add_periodic_callback(callback, wcuUpdateTimer*1000)

    '''
    #Button to stop the server
    
    def exit_callback():
        doc.remove_periodic_callback(per_call)
        endwculog(wcufilename)

     
    button = Button(label="Stop", button_type="success")
    button.on_click(exit_callback)
    doc.add_root(button)
    '''
    #pre = PreText(text="""Select Witch Channels to Watch""",width=500, height=100)

    def addGraph(attrname, old, new):
        '''
        callback function to add graphs figure in the tab area for plotting
        :param attrname:
        :param old: old user selection
        :param new: new user selected channels
        :return: none
        '''

        global old_ch, new_ch
        old_ch = old
        new_ch = new

        uptab = doc.get_model_by_name('graphtab')
        for channel in old:
            tb = doc.get_model_by_name('graphtab')
            if channel != '':
                tb.child.children.remove(tb.child.children[len(tb.child.children) - 1])
        for channel in new:
            plot = figure(plot_height=300, plot_width=1300, title=channel,
                           x_axis_label='s', y_axis_label=channel, toolbar_location="below",
                           tooltips=TOOLTIPS,
                           output_backend=renderer,
                           tools=graphTools,
                           name = channel
                       )
            g = plot.line(x='time', y=channel, color='red', source=source)
            plot.toolbar.logo = None
            uptab.child.children.append(plot)


    OPTIONS = cabecalho.split(',')
    multi_select = MultiSelect(value=[''], options=OPTIONS, title = 'Select Channels', width=300, height=300)
    multi_select.on_change("value", addGraph)

    #make the grid plot of all gauges at the main tab
    Gauges = gridplot([[plot[0], plot[1], plot[4], plot[3]], [plot[6], plot[2], plot[5], plot[7]],[plot[8], plot[9], plot[10], plot[11]]],toolbar_options={'logo': None})

    #addGraph()
    Graphs = (p)
    layoutGraphs = layout(row(Graphs, multi_select))
    layoutGauges = layout(row(Gauges, column(track, steering, texplot)))

    Gauges = Panel(child=layoutGauges, title="Gauges", closable=True)
    Graphs = Panel(child=layoutGraphs, title="Graphs", closable=True, name = 'graphtab')

    def cleanup_session(session_context):
        '''
        This function is called when a session is closed: callback function to end WCU Bokeh server
        :return: none
        '''
        endWCU()

    #activate callback to detect when browser is closed
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
    #curdoc().remove_periodic_callback(per_call)
    endwculog() #end and save log
    sys.exit('Exit')

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

    #check if WCU is ready to run
    if checkall():

        #app = Application(FunctionHandler(wcushow))
        server = Server(
            {'/formulaufsm_dataSoftware': wcushow},
            port = settings.bokehPort,
        )

        server.start()
        server.io_loop.add_callback(server.show, "/")
        server.io_loop.start()
        server.prefix('/formulaufsm_dataSoftware/')

        #alternative form
        #bt = BokehTornado({'/': wcushow})
        #baseserver = BaseServer(server.io_loop, bt, server._http)
        #baseserver.start()
        #baseserver.io_loop.start()

    else:
        sys.exit('CANT START, CHECK ALL')

