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

def gps(data):
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'

    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

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

    cutFs=2

    #gpsLat = ncuTools.bandPassFilter(gpsLat, cutf=cutFs, order = 2)
    #gpsLong = ncuTools.bandPassFilter(gpsLong, cutf=cutFs, order = 2)

    p = figure(plot_width = 1000, plot_height = 550,
               title = 'GPS',
               x_axis_label = 'Long', y_axis_label = 'Lat', toolbar_location="left",
               tooltips=TOOLTIPS,
               output_backend=renderer,
               tools=graphTools,
               )

    g1 = p.circle(x=gpsLat, y=gpsLong, size=1)

    legend = Legend(items=[
        ('35Hz GPS @MOTEC', [g1]),
    ], location=(0,0))

    p.add_layout(legend, 'right')

    p.legend.click_policy='hide'
    p.toolbar.logo = None

    l1 = layout([p])
    tab = Panel(child=l1, title="GPS Tracking", closable=True)
    return tab
