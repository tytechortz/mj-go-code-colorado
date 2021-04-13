import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

body = dbc.Container([
    html.Div([
        html.H2('Colorado Cannabis')

    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.H4('Revenue'),
            html.P(""" Colorado cannabis total revenue. """),
            dbc.Button("Click for Revenue Page", color="primary", href="/revenue"),
        ],
            className='twelve columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.H4('Per Capita Revenue'),
            html.P(""" Colorado cannabis per capita revenue. """),
            dbc.Button("Click for Per Capita Revenue Page", color="primary", href="/pcrev"),
        ],
            className='twelve columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.H4('Per License Revenue'),
            html.P(""" Colorado cannabis per license revenue. """),
            dbc.Button("Click for Per License Revenue Page", color="primary", href="/plrev"),
        ],
            className='twelve columns'
        ),
    ],
        className='row'
    ),
    html.Div([
        html.Div([
            html.H4('Businesses'),
            html.P(""" Colorado cannabis licensee locations. """),
            dbc.Button("Click for Cannabis Businesses Page", color="primary", href="/biz"),
        ],
            className='twelve columns'
        ),
    ],
        className='row'
    ),

])

def Homepage():
    layout = html.Div([
    body
    ])
    return layout