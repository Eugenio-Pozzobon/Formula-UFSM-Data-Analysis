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
from bokeh.models.widgets import Tabs, Panel
from bokeh.themes import built_in_themes
from bokeh.layouts import gridplot
from bokeh.server.server import Server
from bokeh.models.widgets import Button
from bokeh.models import CustomJS, MultiSelect
from bokeh.models import PreText

from math import cos, pi, sin
import time, threading
import pandas as pd
import os, gc, sys
from datetime import datetime

from src.programGui import *
from src.wcuSerial import *
from src.gauges import *
from src.tabGPS import *
from src.server_lifecycle import *

def endwculog(filename):
    nowsave = datetime.now()
    dt_string = nowsave.strftime("%Y%m%d")

    dt_string2 = nowsave.strftime("%Y%m%d%H%M%S")

    if os.path.isdir('./finalReport_wcu'):
        pass
    else:
        os.mkdir('./finalReport_wcu')

    path = './finalReport_wcu/' + dt_string

    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)

    wcu_zip = zipfile.ZipFile(path + '/' + dt_string2 + '.wcu', 'w')
    wcu_zip.write(filename, arcname=dt_string2 + '.csv',
                  compress_type=zipfile.ZIP_DEFLATED)
    wcu_zip.close()

    shutil.rmtree('_wcu_cacheFiles_')

def wcushow(doc):

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
    baudrate = '115200'
    wcuUpdateTimer = 1/5 #second -> 1/FPS

    #list ports in hardware
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports(include_links=False)
    portWCU = ports[0].device

    #conect to WDU and clean garbage
    comport = connectSerial(portWCU, baudrate)
    cleanCOMPORT(comport=comport)

    #create csv file for writing WCU data
    wcufilename = createCSV(cabecalho)

    time.sleep(2) #to start serial, requires an delay to arduino load data at the buffer
    #get WDU data

    lastupdate = '0.0'
    for channel in CANconfig['Channel']:
        lastupdate = lastupdate + ',0.0'

    wcufile = open(wcufilename, "at")
    data, lastupdate, cdc = updateWCUcsv(seconds = wcuUpdateTimer, wcufile = wcufile, comport = comport, header=cabecalho, canconfig= CANconfig, laststring = lastupdate)
    source = ColumnDataSource(data=data)

    # Start Gauges

    #start variables for an array of gauges
    plot = []
    linemin = []
    linemax = []
    valueglyph = []

    gg=0
    #for each channel listed in the wcucsv that have an 'true' marked on the display column,
    # there will be a plot
    for channel in WCUconfig['channel']:
        line = WCUconfig.iloc[gg]
        if(line['display']):
            dataValue = pd.to_numeric(data[channel])[len(data[channel]) - 1]
            plt, mx, mi, vg = plotGauge(dataValue, unit = line['unit'], name = channel, color = line['color'], offset = line['minvalue'], maxValue = line['maxvalue'], major_step = line['majorstep'], minor_step = line['minorstep'])
            plot.append(plt)
            linemax.append(mx)
            linemin.append(mi)
            valueglyph.append(vg)
        gg = gg + 1


    # Other main plots
    #GPS:
    track, points, livepoint = gps(data, singleplot = True, H = 300, W = 300)
    gpssource = points.data_source
    livesource = livepoint.data_source

    #Steering for steering angle
    sangle = figure(plot_height=300, plot_width=300, x_range=(0, 300), y_range=(0, 300))
    #sangle.add_glyph(image)

    #FormulaUFSM with WCU icon!
    wcuIcon = figure(plot_height=300, plot_width=300, x_range=(0, 300), y_range=(0, 300))
    #wcuIcon.image_url(url = [wcuIconUrl], x=150, y=150, w=290, h=290, anchor='center')

    sangle.toolbar.logo = None
    sangle.toolbar_location = None
    sangle.xaxis.visible = None
    sangle.yaxis.visible = None
    sangle.xgrid.grid_line_color = None
    sangle.ygrid.grid_line_color = None

    wcuIcon.toolbar.logo = None
    wcuIcon.toolbar_location = None
    wcuIcon.xaxis.visible = None
    wcuIcon.yaxis.visible = None
    wcuIcon.xgrid.grid_line_color = None
    wcuIcon.ygrid.grid_line_color = None

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
    def callback():
        wcufile = open(wcufilename, "r")
        lastline = (wcufile.readlines()[len(wcufile.readlines())-1])
        lastupdate = ',' + ','.join(lastline.split(',')[(-len(CANconfig['Channel'])):])
        wcufile.close()

        #alternative method
        #df = source.to_df()
        #lastline = df.iloc[[df.ndim - 1]].to_csv(header=False, index=False).strip('\r\n')
        #lastupdate = ',' + ','.join(lastline.split(',')[(-len(CANconfig['Channel'])):])

        wcufile = open(wcufilename, "at")
        data, lastupdate, cdc = updateWCUcsv(seconds=wcuUpdateTimer, wcufile=wcufile, comport=comport, header=cabecalho, canconfig= CANconfig, laststring = lastupdate)

        source.data=data
        # alternative method
        #source.stream(cdc)

        gg = 0
        linectr = 0
        for channel in WCUconfig['channel']:
            line = WCUconfig.iloc[gg]
            if (line['display']):
                dataValue = pd.to_numeric(data[channel])[len(data[channel])-1]
                angle = speed_to_angle(dataValue, line['unit'], offset = line['minvalue'], max_value = line['maxvalue'])
                linemax[linectr].update(angle = angle)
                linemin[linectr].update(angle = angle - pi)
                valueglyph[linectr].update(text = [str(round(dataValue, 1)) + ' ' + line['unit']])
                linectr = linectr + 1
            gg = gg + 1

        steeringangle = pd.to_numeric(data['SteeringAngle'])[len(data['SteeringAngle'])-1]
        #image.update(angle = steeringangle)

        lat, long = latlong(data)
        gpssource.data.update(x=lat, y=long)
        livesource.data.update(x=lat.iloc[-1:], y=long.iloc[-1:])

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
        uptab = curdoc().get_model_by_name('graphtab')
        for channel in old:
            tb = curdoc().get_model_by_name('graphtab')
            if channel != '':
                print(channel)
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
    layoutGauges = layout(row(Gauges, column(track, sangle, wcuIcon)))

    Gauges = Panel(child=layoutGauges, title="Gauges", closable=True)
    Graphs = Panel(child=layoutGraphs, title="Graphs", closable=True, name = 'graphtab')

    tabs = Tabs(tabs=[
                    Gauges,
                    Graphs,
                ], name='WCU TABS')

    doc.add_root(tabs)
    doc.title = 'WCU SCREEN'

    def cleanup_session(session_context):
        ''' This function is called when a session is closed. '''
        doc.remove_periodic_callback(per_call)
        endwculog(wcufilename)
        sys.exit('Exit')

    doc.on_session_destroyed(cleanup_session)

def checkall():
    try:
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports(include_links=False)
        test = ports[0].device
    except:
        return False

    return True


def runwcu():

    if checkall():

        server = Server(
            {'/': wcushow},
            port = 5006,
        )

        server.start()
        server.io_loop.add_callback(server.show, "/")
        server.io_loop.start()

    else:
        sys.exit('CANT START, CHECK ALL')

    # bt = BokehTornado({'/': wcushow})
    # baseserver = BaseServer(server.io_loop,bt,server._http)
    # baseserver.start()
    # baseserver.io_loop.start()

