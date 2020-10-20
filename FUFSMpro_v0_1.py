from src.ncuOpenLOGfile import *
from src.ncuOpenNCUReport import *
from src.programGui import *

if __name__ == "__main__":

    function = initializeGui()

    if(function):
        parseLogFile()
    else:
        openNcuLog()
