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
#from tkinter import *
from tkinter import messagebox
from tkinter import filedialog, messagebox


def getuserselection():
    '''
    window = Tk()

    window.title("Formula UFSM Desktop APP")

    window.geometry('1080x720')

    def clicked():
        messagebox.showinfo('Message title', 'Message content')

    btn = Button(window, text='Click here', command=clicked)

    btn.grid(column=0, row=0)

    window.mainloop()

    root = tk.Tk()
    root.iconbitmap("./projectfolder/icon.ico")
    root.withdraw()
    '''

    #'''
    question = messagebox.askquestion('Program setup', 'Are you looking for telemetry data?')
    if question == 'yes':
        return 'wcu'

    question = messagebox.askquestion('Program setup', 'Are you looking for open files and display data?')
    if question == 'yes':
        return 'log'

    question2 = messagebox.askquestion('Program setup', 'Are you looking for parses a CAN *.CSV files?')
    if question == 'yes':
        return 'ncu'
    '''

    return 'wcu'
    return 'ncu'
    return 'log'
    '''
    #exit()