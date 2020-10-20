import time
import zipfile
import os
import shutil
import sys
import gc

import tkinter as tk
from tkinter import filedialog, messagebox

def initializeGui():
    root = tk.Tk()
    root.iconbitmap("./projectfolder/icon.ico")
    root.withdraw()

    question = messagebox.askquestion('Program setup', 'Are you looking for open *.NCU files and display data?')
    if question == 'yes':
        return False

    question2 = messagebox.askquestion('Program setup', 'Are you looking for parses a *.CSV files?')
    if question == 'yes':
        return question2

    exit()