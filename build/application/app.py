import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import dash_table_experiments as dt
import plotly
import flask
import pandas as pd
import numpy as np

## process data
from inDangerOilAssets import inDangerAssets
from getData import getFireData, getOilAssetData

app = dash.Dash()

df = inDangerAssets(getOilAssetData(), getFireData()).getAssetFrame() ## generates in danger oil assets

mapbox_access_token = 'pk.eyJ1IjoiZ2NsYXJrMjgiLCJhIjoiY2pyY252eWU2MGg0NjQ1cDRjNjJ2eTZjbyJ9.ZJd_6OJyyIq7NqAJYK9QgA'

app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets'
                                    '/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})


app.layout = html.Div(
    [
    ]
)






scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

layout = dict(
    autosize=True,
    height=500,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="dark",
        center=dict(
            lon=-78.05,
            lat=42.54
        ),
        zoom=7,
    )
)


data = [dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df['Longitude'],
        lat = df['Latitude'],
        text = df['id'],
        mode = 'markers',
        marker = dict(
            size = 4,
            opacity = 0.7,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = scl,
            cmin = 0,
            color = 'rgb(231, 99, 250)',
            colorbar=dict(
                title="Oil Assets"
            )
        ))]


fig = dict(data=data, layout=layout )

app.layout  = html.Div([
    dcc.Graph(id='graph', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
