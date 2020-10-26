from src.ncuOpenLOGfile import *
from src.ncuOpenNCUReport import *
from src.programGui import *
from src.wcuSerial import *
from src.wcuScreen import *
from src.gauges import *

import time, threading
import pandas as pd
import os, gc
gc.enable()

wcushow()

#--------

'''
function = initializeGui()

if(function):
    parseLogFile()
else:
    openNcuLog()
'''