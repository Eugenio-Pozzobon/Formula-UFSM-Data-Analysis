# Author: Eugênio Pozzobon
# e-mail: eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import time
import zipfile
import os
import shutil
import sys
import gc

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog, messagebox

import src.settings as settings

def getuserselection():

    global window

    window = Tk()

    window.title("Formula UFSM Desktop APP")

    window.geometry('1080x720')


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

    btnwcu = Button(window, text='WCU', command=WCUBUTTON, width = 10, height = 3 )
    btnlog = Button(window, text='LOG FILE', command=LOGBUTTON, width=10, height=3)
    btnncu = Button(window, text='NCU', command=NCUBUTTON, width=10, height=3)

    btnwcu.grid(column=0, row=10)
    btnlog.grid(column=335, row=10)
    btnncu.grid(column=720-50, row=10)

    window.mainloop()

    '''
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports(include_links=False)
    portWCU = ports[0].device

    '''

    return question