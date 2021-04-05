# Author: Eugênio Pozzobon
# e-mail: eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import tkinter as tk


def start_app():
    global window, question
    question = ''

    window = tk.Tk()
    window.title("Formula UFSM Desktop APP")
    window.geometry('1000x500')


def call_lic():
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title='Error', message='LICENSE FILE REQUIRED')
    root.destroy()

def error_1_wcu():
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title='Error', message='CANT START, CHECK COM PORT AND ALL OPTIONS AT PROJECTFOLDER/SETTINGS.TXT.')
    root.destroy()

def error_2_wcu():
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title='Error', message='You cant add more then 5 graphics')
    root.destroy()

def warning_1_wcu():
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title='Error', message='You may have CPU delays with this value')
    root.destroy()

def get_update_preference():
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.askquestion('Update Available!', 'Do you wanna update for the next program version?')
    root.destroy()

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

    filepath = "./projectfolder/settings.txt"
    def open_file():
        """Open a file for editing."""

        if not filepath:
            return
        txt_edit.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            txt_edit.insert(tk.END, text)

    def save_file():
        """Save the current file as a new file."""
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = txt_edit.get(1.0, tk.END)
            output_file.write(text)


    txt_edit = tk.Text(window)
    open_file()
    
    btn_save = tk.Button(window, text="Save Settings", command=save_file)

    btnwcu = tk.Button(window, text='WCU', command=WCUBUTTON, width = 25, height = 3 )
    btnlog = tk.Button(window, text='LOG (.WCU or .NCU FILES)', command=LOGBUTTON, width=25, height=3)
    btnncu = tk.Button(window, text='NCU CAN CSV DATA', command=NCUBUTTON, width=25, height=3)


    btnwcu.grid(column=0, row=10)
    btnlog.grid(column=335, row=10)
    btnncu.grid(column=720-50, row=10)

    btn_save.grid(row=30, column=0, sticky="ew", padx=5)
    txt_edit.grid(row=30, column=335, sticky="nsew")

    #run window
    window.mainloop()

    #TODO: ADD SELECT COM PORT
    #TODO: ADD CONFIGURATION SETTINGS FOR PLOT NCU GRAPHS

    return question