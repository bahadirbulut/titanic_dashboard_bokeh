from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from flask import Flask, render_template
from bokeh.models import ColumnDataSource, Slider, RangeSlider, HoverTool
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route('/')
def bokeh():

    df = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [4, 4, 4, 5]})  # sea_surface_temperature.copy()
    df2 = df.copy()
    df2.y = np.sin(df2.y)

    source1 = ColumnDataSource(data=df)
    source2 = ColumnDataSource(data=df2)

    hover_tool1 = HoverTool(
        tooltips=[('X', '@x'), ('Y', '@y')]
    )

    hover_tool2 = HoverTool(
        tooltips=[('X', '@x'), ('Y', '@y')]
    )

    p1 = figure(tools=[hover_tool1],
                #x_range=(0, 10), y_range=(0, 10),
                y_axis_label='Y', x_axis_label='x',
                title="Plot 1")
    p1.line('x', 'y', source=source1)

    p2 = figure(tools=[hover_tool2],
                # plot_height=400,
                # plot_width=800,
                #x_range=(0, 10), #y_range=(0, 10),
                y_axis_label='Y', x_axis_label='x',
                title="Plot 2")
    p2.line('x', 'y', source=source2)

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(p1)
    script2, div2 = components(p2)
    html = render_template(
        'embed2.html',
        plot_script=script,
        plot_script2=script2,
        plot_div=div,
        plot_div2=div2,
        js_resources=js_resources,
        css_resources=css_resources,
    )

    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    # fig = figure(plot_width=600, plot_height=600, title='Plot 1')
    # fig.vbar(
    #     x=[1, 2, 3, 4],
    #     width=0.5,
    #     bottom=0,
    #     top=[1.7, 2.2, 4.6, 3.9],
    #     color='navy'
    # )
    #
    # plot = figure(x_range=(0, 10), y_range=(0, 10), y_axis_label='Y', x_axis_label='x',
    #               title="Plot 2")
    # plot.line(
    #     x=[1, 2, 3, 4],
    #     y=[1, 2, 3, 4]
    # )

    # # grab the static resources
    # js_resources = INLINE.render_js()
    # css_resources = INLINE.render_css()
    #
    # # render template
    # script, div = components(fig)
    # script2, div2 = components(plot)
    # html = render_template(
    #     'embed2.html',
    #     plot_script=script,
    #     plot_script2=script2,
    #     plot_div=div,
    #     plot_div2=div2,
    #     js_resources=js_resources,
    #     css_resources=css_resources,
    # )

    return html


if __name__ == '__main__':
    app.run(debug=True)