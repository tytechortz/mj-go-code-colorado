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
            html.H2('Revenue'),
            html.P(""" Colorado cannabis total revenue. """),
            dbc.Button("Click for Revenue Page", color="primary", href="/revenue"),
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