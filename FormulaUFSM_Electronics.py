# Author: Eugênio Pozzobon
# e-mail: eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

from update_check import isUpToDate, update

import src.ncuOpenLOGfile as ncuOpenLOGfile
import src.ncuOpenReport as ncuOpenReport
import src.programGui as programGui
import src.wcuScreen as wcuScreen
import src.lic as lic

import src.settings as settings

programGui.start_app()

program_version = '3.2'

'''
if isUpToDate('./README.MD', "https://raw.githubusercontent.com/Eugenio-Pozzobon/Formula-UFSM-Data-Analysis/master/README.MD") == False:
   if programGui.get_update_preference():
       update('./README.MD', "https://raw.githubusercontent.com/Eugenio-Pozzobon/Formula-UFSM-Data-Analysis/master/README.MD")

'''
import gc, sys

# enable RAM cleaner
gc.enable()

# get program settings
settings.init()

# check if user has license
if lic.checkLicense():

    # get user mode selection
    screen = programGui.getuserselection()

    # run
    if screen == 'wcu':
        wcuScreen.runwcu()
    if screen == 'ncu':
        ncuOpenLOGfile.parseLogFile()
    if screen == 'log':
        ncuOpenReport.startNCU() # file selection and descompression
        ncuOpenReport.runLogAnalysis() # file analysis

else:
    #System out message
    #input('LICENSE FILE REQUIRED\n\nPress Enter to Exit')
    programGui.call_lic()
    sys.exit()
#--------