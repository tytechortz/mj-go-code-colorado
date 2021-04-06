import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

def revenue_App():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Link('Home', href='/')
                ],
                    className='two columns'
                ),

            ],
                className='twelve columns'
            ),

        ],
            className='row'
        ),
        html.Div([
            html.H4(
                'Revenue Data',
                className='twelve columns',
                style={'text-align': 'center'}
            ),
        ],
            className='row'
        ),
    ])


app.layout = revenue_App