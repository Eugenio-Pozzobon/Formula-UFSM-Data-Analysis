import sys
import os
import numpy as np

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def bandPassFilter(signal, cutf=5, order = 5):
    from scipy.signal import butter, lfilter, filtfilt
    fs = 200  # sample rate, Hz
    # Filter requirements.
    cutoff = cutf # desired cutoff frequency of the filter, Hz ,      slightly higher than actual 1.2 Hz
    nyq = 1 * fs  # Nyquist Frequency
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a  = butter(order, normal_cutoff, btype='lowpass', analog=False)
    y = filtfilt(b, a , signal, axis=0)
    return y

def mapDouble(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def dbfft(time, y, ref=1):
    """
    Calculate spectrum in dB scale
    Args:
        x: input signal
        fs: sampling frequency
        ref: reference value used for dBFS scale. 32768 for int16 and 1 for float

    Returns:
        freq: frequency vector
        s_db: spectrum in dB scale
    """

    fs=200
    N = len(time)
    fs = len(time)/(time[len(time)-1]-time[1])
    win = np.hanning(N)
    x = y * win  # Take a slice and multiply by a window
    sp = np.fft.rfft(x)  # Calculate real FFT
    s_mag = np.abs(sp) * 2 / np.sum(win)  # Scale the magnitude of FFT by window and factor of 2,
    # because we are using half of FFT spectrum
    s_dbfs = 20 * np.log10(s_mag / ref)  # Convert to dBFS
    freq = np.arange((N / 2) + 1) / (float(N) / fs)  # Frequency axis

    return freq[:-1], s_dbfs

def decodeCAN(lineS):

    RPM=',0'
    Gear=',0'
    BatteryVoltage=',0'
    OilPressure=',0'
    Speed=',0'
    TPS=',0'
    SteeringAngle=',0'
    ECU_GForceLat=',0'
    Lambda=',0'
    MAP=',0'
    FuelPressure=',0'
    BrakePressure=',0'
    EngineTemp=',0'
    OilTemp=',0'
    AirTemp=',0'
    RadOutTemp=',0'
    GPSlatHW=',0'
    GPSlatLW=',0'
    GPSlongHW=',0'
    GPSlongLW=',0'
    PneuDianteiroInner=',0.0'
    PneuDianteiroCenter=',0.0'
    PneuDianteiroOuter=',0.0'
    PneuTraseiroInner=',0.0'
    PneuTraseiroCenter=',0.0'
    PneuTraseiroOuter=',0.0'
    if(len(lineS)>=10):
        if int(lineS[1]) == 1000:
            RPM = ',' + str((float(lineS[2]) * 256 + float(lineS[3])))
            Gear = ',' + str((float(lineS[4]) * 256 + float(lineS[5])))
            BatteryVoltage = ',' + str((float(lineS[6]) * 256 + float(lineS[7])) / 100)
            OilPressure = ',' + str((float(lineS[8]) * 256 + float(lineS[9])) / 1000)
        if int(lineS[1]) == 1001:
            Speed = ',' + str((float(lineS[2]) * 256 + float(lineS[3])) / 10)
            TPS = ',' + str((float(lineS[4]) * 256 + float(lineS[5])) / 10)
            SteeringAngle = ',' + str((float(lineS[6]) * 256 + float(lineS[7])) / 10)
            ECU_GForceLat = ',' + str((float(lineS[8]) * 256 + float(lineS[9])) / 1000)
        if int(lineS[1]) == 1002:
            Lambda = ',' + str((float(lineS[2]) * 256 + float(lineS[3])) / 1000)
            MAP = ',' + str((float(lineS[4]) * 256 + float(lineS[5])) / 10)
            FuelPressure = ',' + str((float(lineS[6]) * 256 + float(lineS[7])) / 1000)
            BrakePressure = ',' + str((float(lineS[8]) * 256 + float(lineS[9])) / 1000)
        if int(lineS[1]) == 1010:
            EngineTemp = ',' + str((float(lineS[2]) * 256 + float(lineS[3])) / 10)
            OilTemp = ',' + str((float(lineS[4]) * 256 + float(lineS[5])) / 10)
            AirTemp = ',' + str((float(lineS[6]) * 256 + float(lineS[7])) / 10)
            RadOutTemp = ',' + str((float(lineS[8]) * 256 + float(lineS[9])) / 10)
        if int(lineS[1]) == 1003:
            GPSlatHW = ',' + str((float(lineS[2]) * 256 + float(lineS[3])))
            GPSlatLW = ',' + str((float(lineS[4]) * 256 + float(lineS[5])))
            GPSlongHW = ',' + str((float(lineS[6]) * 256 + float(lineS[7])))
            GPSlongLW = ',' + str((float(lineS[8]) * 256 + float(lineS[9])))
        if int(lineS[1]) == 10:
            PneuDianteiroInner = ',' + str(float(lineS[2]))
            PneuDianteiroCenter = ',' + str(float(lineS[3]))
            PneuDianteiroOuter = ',' + str(float(lineS[4]))
        if float(lineS[1]) == 11:
            PneuTraseiroInner = ',' + str(float(lineS[2]))
            PneuTraseiroCenter = ',' + str(float(lineS[3]))
            PneuTraseiroOuter = ',' + str(float(lineS[4]))
    CAN = RPM + Gear + BatteryVoltage + OilPressure + Speed + TPS + SteeringAngle + ECU_GForceLat + Lambda + MAP + FuelPressure + BrakePressure + EngineTemp + OilTemp + AirTemp + RadOutTemp + GPSlatHW + GPSlatLW + GPSlongHW + GPSlongLW + PneuDianteiroInner + PneuDianteiroCenter + PneuDianteiroOuter + PneuTraseiroInner + PneuTraseiroCenter + PneuTraseiroOuter

    return CAN