import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import plotly.graph_objs as go
import dash_table

## process data
from getData import getOilAssetData, getFireData
from inDangerOilAssets import inDangerAssets


## Data ##
OilAssetsInDanger = inDangerAssets(getOilAssetData(), getFireData()).getAssetFrame()
oilPriceWTI = getOilAssetData()

OilAssetsInDanger = OilAssetsInDanger.sort_values(by='Distance')
OilAssetsInDanger = OilAssetsInDanger[['id', 'Distance', 'Latitude', 'Longitude', 'dangerLevel',]]


app = dash.Dash()
mapBoxToken = "pk.eyJ1IjoiZ2NsYXJrMjgiLCJhIjoiY2pyY252eWU2MGg0NjQ1cDRjNjJ2eTZjbyJ9.ZJd_6OJyyIq7NqAJYK9QgA"

mapbox_access_token = 'pk.eyJ1IjoiZ2NsYXJrMjgiLCJhIjoiY2pyY252eWU2MGg0NjQ1cDRjNjJ2eTZjbyJ9.ZJd_6OJyyIq7NqAJYK9QgA'

app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets'
                                    '/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

legend = {1: "0 to 2 Kilometers", 2: " 2 to 4 Kilometers", 3: "4 to 6 Kilometers", 4: "6-8 Kilometers",
          5: "8 to 10 Kilometers"}



def make_main_figure():
    traces = []
    for asset, df in OilAssetsInDanger.groupby('dangerLevel'):
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
    return figure


def make_main_table(dataFrame):
    return dash_table.DataTable(
        data=dataFrame.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in dataFrame.columns],

        style_as_list_view=True,
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': '#CCCCCC'
        },


        style_table={
            'overflowY': 'scroll',
            'maxHeight': '430'
        },
    )


app.layout = html.Div(
    [

        html.Div(
            [
                html.H1(
                    'Oil Assets At Risk by Forest Fire',
                    className='nine columns',

                style={
                'textAlign': 'center',
                'fontFamily': "Overpass",
                'color': '#CCCCCC'}
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(figure=make_main_figure())
                    ],
                    className='eight columns',
                    style={'margin-top': '20'}
                ),

                html.Div(
                    [
                        make_main_table(OilAssetsInDanger)
                    ],
                    className="four columns"
                )],
            className="row")

    ],
style={'backgroundColor':'black'}
)

if __name__ == '__main__':
    app.run_server()
