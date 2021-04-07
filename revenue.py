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
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph('revenue-map')
                ],
                    className='twelve columns'
                ),
            ],
                className='eight columns'
            ),
            html.Div([
                dcc.Markdown('''Click on counties and use year slider to see annual county
            revenue data displayed in graphs.  Green counties have at
            least one form of legalized cannabis, green circles show 
            relative cannabis revenue for selected year. 
            Select sales radio buttons to display revenue graphically below.''')
            ],
                className='four columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                dcc.Slider(
                    id='year',
                    min=2014,
                    max=2020,
                    step=1,
                    marks={x: '{}'.format(x) for x in range(2014, 2021)},
                    value=2014
                ),
            ],
                className='eight columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                dcc.Slider(
                    id='month',
                    min=1,
                    max=12,
                    step=1,
                    marks={x: '{}'.format(x) for x in range(1, 13)},
                    value=1
                )
            ],
                className='six columns'
            ),
            html.Div([
                dcc.Checklist(
                    id='rev',
                    options=[
                        {'label':'Total Sales', 'value':'TOTAL'},
                        {'label':'Rec Sales','value':'REC'},
                        {'label':'Med Sales','value':'MED'},
                    ],
                    labelStyle={'display':'inline-block', 'margin': 0, 'padding': 1},
                    value = ['TOTAL'],
                    style = {'text-align': 'center'}
                    ),
            ],
                className='six columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='rev-bar')
            ],
                className='six columns'
            ),
            html.Div([
                dcc.Graph(id='rev-scatter')
            ],
                className='six columns'
            ),
        ],
            className='row'
        ),
        html.Div(id='crat', style={'display': 'none'}),
    ])


app.layout = revenue_App