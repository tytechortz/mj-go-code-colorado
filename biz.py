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
                dcc.Markdown('''Map shows markers for locations of 2019 cannabis licenses, the latest year available, color coded by license type. Select license type radio buttons to filter map. Use year slider below map to display number of licensees for given year in bar graph below'''),
                dcc.RadioItems(id='categories', options=[
                {'label':'All', 'value':'all'},
                {'label':'MED Licensed Transporters','value':'MED Licensed Transporters'},
                {'label':'MED Licensed Center','value':'MED Licensed Center'},
                {'label':'MED Licensed Cultivator','value':'MED Licensed Cultivator'},
                {'label':'MED Licensed Infused Product Manufacturer','value':'MED Licensed Infused Product Manufacturer'},
                {'label':'MED Licensed R&D Cultivation','value':'MED Licensed R&D Cultivation'},
                {'label':'MED Licensed Retail Operator','value':'MED Licensed Retail Operator'},
                {'label':'MED Licensed Testing Facility','value':'MED Licensed Testing Facility'},
                {'label':'MED Licensed Retail Marijuana Product Manufacturer','value':'MED Licensed Retail Marijuana Product Manufacturer'},
                {'label':'MED Licensed Retail Cultivator','value':'MED Licensed Retail Cultivator'},
                {'label':'MED Licensed Retail Testing Facility','value':'MED Licensed Retail Testing Facility'},
                {'label':'MED Licensed Retail Transporter','value':'MED Licensed Retail Transporter'},
                {'label':'MED Licensed Retail Marijuana Store','value':'MED Licensed Retail Marijuana Store'},
                ],        
                labelStyle={'display':'block', 'margin': 0, 'padding': 1},
                value = 'all'
                ),
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
                dcc.Graph(id='biz-bar')
            ],
                className='six columns'
            ),
        ],
            className='row'
        ),
    ])

app.layout = biz_App