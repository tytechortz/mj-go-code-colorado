import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

def plrev_App():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Link('Home', href='/')
                ],
                    className='two columns'
                ),
                html.H4('Per License Revenue',
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
                    dcc.Graph('plrev-map')
                ],
                    className='twelve columns'
                ),
            ],
                className='eight columns'
            ),
            html.Div([
                dcc.Markdown('''Click on counties to show revenue, license count, revenue per license, county ranking, and revenue change from 2019 to 2020. Counties are shaded to indicate realative revenue per license, with darker shades representing higher values. 2019 is the most recent year for license information''')
            ],
                className='four columns'
            ),
        ],
            className='row'
        ),
        # html.Div([
        #     html.Div([
        #         dcc.Slider(
        #             id='year',
        #             min=2014,
        #             max=2020,
        #             step=1,
        #             marks={x: '{}'.format(x) for x in range(2014, 2021)},
        #             value=2014
        #         ),
        #     ],
        #         className='eight columns'
        #     ),
        # ],
        #     className='row'
        # ),
        # html.Div([
        #     html.Div([
        #         dcc.RangeSlider(
        #             id='year2',
        #             min=1990,
        #             max=2050,
        #             step=1,
        #             # options=[{'label':x, 'value':x} for x in range(2022, 2050)],
        #             value=[2014,2020]
        #         ),
        #     ],
        #         className='eight columns'
        #     ),
        # ],
        #     className='row'
        # ),
        html.Div([
            html.Div([
                html.Div(id='pl-info')
            ],
                className='six columns'
            ),
        ],
            className='row'
        ),
        html.Div(id='pl-data', style={'display': 'none'}),
    ])

app.layout = plrev_App