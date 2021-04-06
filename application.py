import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from homepage import Homepage
from revenue import revenue_App


app = dash.Dash()
application = app.server

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/revenue':
        return revenue_App()
    else:
        return Homepage()


if __name__ == '__main__':
    application.run(debug=True, port=8000)