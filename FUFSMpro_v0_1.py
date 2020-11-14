# Author: Eugênio Pozzobon
# e-mail: eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

import src.ncuOpenLOGfile as ncuOpenLOGfile
import src.ncuOpenReport as ncuOpenReport
import src.programGui as programGui
import src.wcuScreen as wcuScreen
import src.lic as lic

import src.settings as settings

import os, gc, sys

gc.enable()

settings.init()

if lic.checkLicense():

    screen = programGui.getuserselection()

    if screen == 'wcu':
        wcuScreen.runwcu()
    if screen == 'ncu':
        ncuOpenLOGfile.parseLogFile()
    if screen == 'log':
        ncuOpenReport.openLog()

else:
    sys.exit('LICENSE required')
#--------