from math import cos, pi, sin

from bokeh.io import show, output_notebook
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models import Arc, Circle, ColumnDataSource, Plot, Range1d, Ray, Text
from bokeh.resources import INLINE
from bokeh.util.browser import view

start_angle = pi + pi/4
end_angle = -pi/4

def data(value):
    """Shorthand to override default units with "data", for e.g. `Ray.length`. """
    return dict(value=value, units="data")


def speed_to_angle(speed, units, offset = 0, max_value = 1):
    speed = speed - offset
    max_value = max_value - offset
    speed = min(max(speed, 0), max_value)
    total_angle = start_angle - end_angle
    angle = total_angle * float(speed) / (max_value)
    return start_angle - angle


def add_needle(plot, speed, units, offset = 0, max_value = 1):
    angle = speed_to_angle(speed, units, offset, max_value)
    rmax = Ray(x=0, y=0, length=data(0.75), angle=angle, line_color="black", line_width=3)
    rmin = Ray(x=0, y=0, length=data(0.10), angle=angle - pi, line_color="black", line_width=3)
    plot.add_glyph(rmax)
    plot.add_glyph(rmin)
    return rmax, rmin


def polar_to_cartesian(r, alpha):
    return r * cos(alpha), r * sin(alpha)


def add_gauge(plot, radius, max_value, length, direction, color, major_step, minor_step, offset = 0):
    major_angles, minor_angles = [], []

    total_angle = start_angle - end_angle

    major_angle_step = float(major_step) / max_value * total_angle
    minor_angle_step = float(minor_step) / max_value * total_angle

    major_angle = 0

    while major_angle <= total_angle:
        major_angles.append(start_angle - major_angle)
        major_angle += major_angle_step

    minor_angle = 0

    while minor_angle <= total_angle:
        minor_angles.append(start_angle - minor_angle)
        minor_angle += minor_angle_step

    major_labels = [major_step * i + offset for i, _ in enumerate(major_angles)]

    n = major_step / minor_step
    minor_angles = [x for i, x in enumerate(minor_angles) if i % n != 0]

    glyph = Arc(x=0, y=0, radius=radius, start_angle=start_angle, end_angle=end_angle, direction="clock",
                line_color=color, line_width=2)
    plot.add_glyph(glyph)

    rotation = 0 if direction == 1 else -pi

    x, y = zip(*[polar_to_cartesian(radius, angle) for angle in major_angles])
    angles = [angle + rotation for angle in major_angles]
    source = ColumnDataSource(dict(x=x, y=y, angle=angles))

    glyph = Ray(x="x", y="y", length=data(length), angle="angle", line_color=color, line_width=2)
    plot.add_glyph(source, glyph)

    x, y = zip(*[polar_to_cartesian(radius, angle) for angle in minor_angles])
    angles = [angle + rotation for angle in minor_angles]
    source = ColumnDataSource(dict(x=x, y=y, angle=angles))

    glyph = Ray(x="x", y="y", length=data(length / 2), angle="angle", line_color=color, line_width=1)
    plot.add_glyph(source, glyph)

    x, y = zip(*[polar_to_cartesian(radius + 2 * length * direction, angle) for angle in major_angles])
    text_angles = [angle - pi / 2 for angle in major_angles]
    source = ColumnDataSource(dict(x=x, y=y, angle=text_angles, text=major_labels))

    glyph = Text(x="x", y="y", angle="angle", text="text", text_align="center", text_baseline="middle")
    plot.add_glyph(source, glyph)

def plotGauge(speedvalue, offset = 0, name = '', unit = '', color = '', maxValue = 0, major_step = 2, minor_step = .5):
    maxValue = maxValue - offset
    xdr = Range1d(start=-1.25, end=1.25)
    ydr = Range1d(start=-1.25, end=1.25)

    renderer = 'webgl'
    plt = Plot(x_range=xdr, y_range=ydr, plot_width=300, plot_height=300, output_backend=renderer,)
    plt.toolbar_location = None
    plt.outline_line_color = None

    plt.add_glyph(Circle(x=0, y=0, radius=1.00, fill_color="white", line_color="black"))
    plt.add_glyph(Circle(x=0, y=0, radius=0.05, fill_color="gray", line_color="black"))

    plt.add_glyph(Text(x=0, y=+0.15, text=[unit], text_color=color, text_align="center", text_baseline="bottom",
                        text_font_style="bold"))

    plt.add_glyph(Text(x=0, y=-0.15, text=[name], text_color="black", text_align="center", text_baseline="top",
                        text_font_style="bold"))

    add_gauge(plt, 0.75, maxValue, 0.05, +1, color, major_step, minor_step, offset = offset)

    valueGliph = Text(x=0, y=-0.6, text=["0"], text_color=color, text_align="center", text_baseline="top")

    plt.add_glyph(valueGliph)

    a, b = add_needle(plt, speedvalue, unit, offset = offset, max_value = maxValue)
    return plt, a, b, valueGliph