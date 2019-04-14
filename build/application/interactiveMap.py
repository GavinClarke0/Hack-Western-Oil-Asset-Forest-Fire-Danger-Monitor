import plotly.dashboard_objs as dashboard

my_dboard = dashboard.Dashboard()
my_dboard.get_preview()

import plotly.graph_objs as go

import plotly.plotly as py
import pandas as pd

from OilAssets import *
from forestFires import *
from inDangerOilAssets import *

df = inDangerAssets(getOilAssetData(), getFireData()).getAssetFrame()

mapBoxToken = "pk.eyJ1IjoiZ2NsYXJrMjgiLCJhIjoiY2pyY252eWU2MGg0NjQ1cDRjNjJ2eTZjbyJ9.ZJd_6OJyyIq7NqAJYK9QgA"

legend = {1: "0 to 2 Kilometers", 2: " 2 to 4 Kilometers", 3: "4 to 6 Kilometers", 4: "6-8 Kilometers",
          5: "8 to 10 Kilometers"}

traces = []
for asset, df in df.groupby('dangerLevel'):
    trace = dict(
        type='scattermapbox',
        lon=df['Longitude'],
        lat=df['Latitude'],
        text=df['id'],
        name=legend[asset],
        marker=dict(
            size=4,
            opacity=0.6,
        )
    )
    traces.append(trace)

layout = go.Layout(

    title="Satellite Over View at Risk Oil Asssets by Forest Fire ",

    # COLOR THEME
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",

    font=dict(
        family="Overpass",
        size=20,
        color='#CCCCCC',
    ),
    margin=dict(
        t=80,
        l=40,
        b=40,
        r=120,
        pad=0,
    ),
    # LEGEND
    legend=dict(
        x=1.02,
        y=1,
        font=dict(size=10),
    ),

    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapBoxToken,
        style="dark",
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=48.35,
            lon=-99.99,

        ),
        pitch=0,


    ),
)

figure = dict(data=traces, layout=layout)
py.plot(figure, filename='Oil Assset Map')
