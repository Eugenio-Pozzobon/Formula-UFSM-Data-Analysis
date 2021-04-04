#my_first_plot.py
import pandas as pd
from bokeh.layouts import layout
from bokeh.models import Legend
from bokeh.models.widgets import Panel
from bokeh.plotting import figure


def latlong(data):
    '''
    process gps data for ploting map
    :param data:  pandas dataframe with datavalues
    :return: gps lat and long values
    '''

    #start processing
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

    # make conversion
    gpsLat = ((sensor_data_a-65536) * 65536 + sensor_data_b)/10000000
    gpsLong = ((sensor_data_c-65536) * 65536 + sensor_data_d)/10000000

    return gpsLat, gpsLong

def gps(data, singleplot = False, H=550, W=1000):
    '''
    plot GPS tab
    :param data: pandas dataframe with data
    :param singleplot: if True, plot without legend and return only the bokeh figure
    :param H: Height of plot
    :param W: Width of plot
    :return: bokeh figure or figure, circles and actual circle ploted (for streaming)
    '''
    TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
    ]

    renderer = 'webgl'
    graphTools = 'pan,wheel_zoom,box_zoom,zoom_in,zoom_out,hover,crosshair,undo,redo,reset,save'

    #get processed data
    lat, long = latlong(data)

    #possible filter
    cutFs=2
    #gpsLat = ncuTools.bandPassFilter(gpsLat, cutf=cutFs, order = 2)
    #gpsLong = ncuTools.bandPassFilter(gpsLong, cutf=cutFs, order = 2)

    p = figure(plot_width = W, plot_height = H,
               output_backend=renderer, title = "GPS TRACK", #graphTools = graphTools
               )

    g1 = p.circle(x=lat, y=long, size=3, color = 'gray')

    p.toolbar.logo = None
    p.xaxis.visible = False
    p.yaxis.visible = False

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
