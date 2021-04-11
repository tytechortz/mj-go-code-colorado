import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

def biz_App():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Link('Home', href='/')
                ],
                    className='two columns'
                ),
                html.H4('Businesses',
                className='twelve columns',
                style={'text-align': 'center'}
            ),

            ],
                className='twelve columns'
            ),

        ],
            className='row'
        ),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph('biz-map')
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
            Select sales check boxes to display revenue graphically below.''')
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
                dcc.RangeSlider(
                    id='year2',
                    min=1990,
                    max=2050,
                    step=1,
                    # options=[{'label':x, 'value':x} for x in range(2022, 2050)],
                    value=[2014,2020]
                ),
            ],
                className='eight columns'
            ),
        ],
            className='row'
        ),
        # html.Div([
        #     html.Div([
        #         dcc.Graph(id='per-cap-rev-bar')
        #     ],
        #         className='six columns'
        #     ),
            # html.Div([
            #     dcc.Graph(id='rev-scatter')
            # ],
            #     className='six columns'
            # ),
        # ],
        #     className='row'
        # ),
    ])

app.layout = biz_App