#Bokeh, Numpy, Pandas, Dask, Scipy, Zipfile, shutil, sys, gc, time, tkinter, re
'''
from src.tabPilot import *
from src.tabBAT import *
from src.tabSuspension import *
from src.tabBrakes import *
from src.tabMPU6050 import *
from src.tabSuspFFT import *
from src.tabSuspHisto import *
from src.tabGPS import *
from src.tabNCU import *
from src.tabEngine import *
from src.tabTTSU import *
'''

from src.programTools import *
from src.programGui import *
from src.ncuOpenLOGfile import *

import time
import zipfile
import os
import shutil
import sys
import gc
import pathlib

from bokeh.layouts import row, column, layout, gridplot
from bokeh.io import save, show, curdoc
from bokeh.plotting import figure, output_file
from bokeh.models.widgets import Tabs, Panel, Button
from bokeh.themes import built_in_themes
from bokeh.models import RangeSlider, ColumnDataSource
from bokeh.server.server import Server

import pandas as pd
import re

from bokeh.models import CustomJS, RangeSlider

from src.graph import make_ncu_tabs, plot_layout_tab
from src.userformula import user_equations
import src.settings as settings

def startNCU():
    '''
    start NCU oppening files
    :return: none
    '''
    import tkinter as tk
    from tkinter import filedialog, messagebox

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
    doc.theme = settings.colortheme

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
            tab0 = pilot(data)
            tab7 = gps(data)
            tab9 = engine(data)
            tab10 = tireTemp(data)

            # Join tabs
            tabs = Tabs(tabs=[
                tab0,
                tab9,
                tab7,
                tab10,
            ], name='WCU TABS')

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

    server = Server(
        {'/': openLog},
        port = settings.bokehPort,
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
    if messagebox.askyesno("Question","Do you want to open another file?"):
        restart_program()