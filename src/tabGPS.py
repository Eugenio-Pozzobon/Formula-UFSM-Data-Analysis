#my_first_plot.py
from bokeh.plotting import figure, output_file, show
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, BoxSelectTool, Legend, LinearAxis, Range1d
from bokeh.layouts import row, column, layout
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.models.layouts import Box

import json

from bokeh.models import GeoJSONDataSource
from bokeh.sampledata.sample_geojson import geojson

from scipy.signal import sosfiltfilt
import numpy as np
import pandas as pd
import dask.dataframe as dd

import src.programTools as ncuTools

def latlong(data):
    sensor_data_a = data['GPSlatHW']
    sensor_data_b = data['GPSlatLW']
    sensor_data_c = data['GPSlongHW']
    sensor_data_d = data['GPSlongLW']

    sensor_data_a = pd.to_numeric(sensor_data_a)
    sensor_data_b = pd.to_numeric(sensor_data_b)
    sensor_data_c = pd.to_numeric(sensor_data_c)
    sensor_data_d = pd.to_numeric(sensor_data_d)

    sensor_time = data['time']
    sensor_time = pd.to_numeric(sensor_time)
    sensor_time = sensor_time/1000

    gpsLat = ((sensor_data_a-65536) * 65536 + sensor_data_b)/10000000
    gpsLong = ((sensor_data_c-65536) * 65536 + sensor_data_d)/10000000

    return gpsLat, gpsLong

def gps(data, singleplot = False, H=550, W=1000):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'

    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    lat, long = latlong(data)

    cutFs=2

    #gpsLat = ncuTools.bandPassFilter(gpsLat, cutf=cutFs, order = 2)
    #gpsLong = ncuTools.bandPassFilter(gpsLong, cutf=cutFs, order = 2)

    p = figure(plot_width = W, plot_height = H,
               output_backend=renderer, title = "GPS TRACK"
               )

    g1 = p.circle(x=lat, y=long, size=3, color = 'gray')

    p.toolbar.logo = None
    #p.toolbar_location = None
    p.xaxis.visible = None
    p.yaxis.visible = None

    if singleplot:
        g2 = p.circle(x=lat.iloc[-1:], y=long.iloc[-1:], size=5, color='red')
        return p, g1, g2
    else:
        legend = Legend(items=[
            ('35Hz GPS @MOTEC', [g1]),
        ], location=(0, 0))

        p.add_layout(legend, 'right')

        p.legend.click_policy = 'hide'

        l1 = layout([p])
        tab = Panel(child=l1, title="GPS Tracking", closable=True)
        return tab
