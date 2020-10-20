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