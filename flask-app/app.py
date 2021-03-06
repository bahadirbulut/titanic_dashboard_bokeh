from flask import Flask, render_template
import pandas as pd
from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, RangeSlider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop

from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature

app = Flask(__name__)


def modify_doc(doc):
    df = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [4, 4, 4, 5]})  # sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)

    # plot = figure(x_axis_type='datetime', y_range=(0, 25), y_axis_label='Temperature (Celsius)',
    #               title="Sea Surface Temperature at 43.18, -70.43")
    plot = figure(x_range=(0, 10), y_range=(0, 10), y_axis_label='Y', x_axis_label='x',
                  title="Just a test plot")
    plot.line('x', 'y', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
            x_start = 0
        else:
            data = df[df.x >= new]
            x_start = new

        source.data = dict(x=data.x, y=data.y)
        plot.x_range.start = x_start

    slider = Slider(start=0, end=9, value=0, step=1, title="x start")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    # doc.theme = Theme(filename="theme.yaml")


@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("embed.html", script=script, template="Flask")


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["127.0.0.1:8000"])
    server.start()
    server.io_loop.start()


from threading import Thread

Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    app.run(port=8000)
