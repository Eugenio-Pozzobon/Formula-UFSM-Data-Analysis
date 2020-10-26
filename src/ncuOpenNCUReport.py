#Bokeh, Numpy, Pandas, Dask, Scipy, Zipfile, shutil, sys, gc, time, tkinter, re

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

from src.programTools import *
from src.programGui import *
from src.ncuOpenLOGfile import *

import time
import zipfile
import os
import shutil
import sys
import gc

from bokeh.io import save, show, curdoc
from bokeh.plotting import figure, output_file
from bokeh.models.widgets import Tabs, Panel
from bokeh.themes import built_in_themes

import pandas as pd
import re

import tkinter as tk
from tkinter import filedialog, messagebox

def openNcuLog():
    #Allows the program to clean memory in the program
    gc.enable()

    root = tk.Tk()
    root.iconbitmap("./projectfolder/icon.ico")
    root.withdraw()

    #Get the NCU file to start descompression
    file_path_string_s = filedialog.askopenfilenames(initialdir = "./output/finalReport_ncu/",title = "Select NCU Log file", filetypes=[("NCU file @Formula UFSM","*.ncu")])
                                            #names to get multiples archive
    # If someone file is selected, then:
    for file_path_string in file_path_string_s:

        # Get the ID of the log File. ID is the numper on the file name.
        print(file_path_string)
        num=re.findall(r'\d+',file_path_string)
        l=num[len(num)-1]

        #Check if the correct directory exists inside the root folder, if not, create new folders.

        if os.path.isdir('./_ncu_cacheFiles_'):
            print('_ncu_cacheFiles_ ok')
        else:
            print('creating directory...')
            os.mkdir('./_ncu_cacheFiles_')

        if os.path.isdir('./finalReport_ncu'):
            print('finalReport_ncu ok')
        else:
            print('creating directory...')
            os.mkdir('./finalReport_ncu')

        logFileCSV = 'logFinal_part_' + str(l) + '.csv'

        logFileCSVrar = 'logFinal_part_' + str(l) + '.ncu'

        ziplog = zipfile.ZipFile(file_path_string)

        #Try descompressing NCU file to get the CSV file
        go=False
        for file in ziplog.namelist():
            if ziplog.getinfo(file).filename == logFileCSV:
                data = pd.read_csv(ziplog.extract(file, '_ncu_cacheFiles_/' + logFileCSV))
                go=True
            else:
                print('error descompressing csv file')

        #Check if descompressed file have an CSV named correctly inside
        if go:

            #Configure the HTML final to the output graphics
            logHTMLFile = 'finalReport_ncu/logFinal_part_' + str(l) + '.html'

            output_file(logHTMLFile, title='NCU LOG ' + str(l) + ' | FORMULA UFSM')

            #curdoc().theme = 'dark_minimal'

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

            # Join tabs
            tabs = Tabs(tabs=[
                tab0,
                tab9,
                tab1,
                tab8,
                tab7,
                tab3,
                tab4,
                tab10,
                tab2,
                tab6,
                tab5,
            ], name='NCU TABS')

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

        #remove the temporary folder
        shutil.rmtree('_ncu_cacheFiles_')

    #chck if the user want to open another log file
    if messagebox.askyesno("Question","Do you want to open another file?"):
        restart_program();
