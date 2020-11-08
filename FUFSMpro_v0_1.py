# Author: Eugênio Pozzobon
# e-mail: eugeniopp00@gmail.com
# Github: https://github.com/Eugenio-Pozzobon
# Linkedin: https://www.linkedin.com/in/eugeniopozzobon/
# Licensed under the GNU General Public License v3.0

from src.ncuOpenLOGfile import *
from src.ncuOpenReport import *
from src.programGui import *
from src.wcuScreen import *
from src.lic import *

import os, gc

gc.enable()

if checkLicense():

    screen = getuserselection()

    if screen == 'wcu':
        runwcu()
    if screen == 'ncu':
        parseLogFile()
    if screen == 'log':
        openLog()

else:
    sys.exit('LICENSE required')
#--------