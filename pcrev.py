import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

def pcrev_App():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Link('Home', href='/')
                ],
                    className='two columns'
                ),
                html.H4('Per Capita Revenue Data',
                className='twelve columns',
                style={'text-align': 'center'}
            ),

            ],
                className='twelve columns'
            ),

        ],
            className='row'
        ),

    ])

app.layout = pcrev_App