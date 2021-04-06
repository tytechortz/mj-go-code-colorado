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
])

def Homepage():
    layout = html.Div([
    body
    ])
    return layout