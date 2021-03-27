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

import tkinter as tk

import src.settings as settings

def start_app():
    global window, question
    question = ''

    window = tk.Tk()
    window.title("Formula UFSM Desktop APP")
    window.geometry('1080x720')

def get_update_preference():
    tk.messagebox.askquestion('Update Available!', 'Do you wanna update for the next program version?')

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