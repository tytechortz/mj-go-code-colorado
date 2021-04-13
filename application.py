import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from homepage import Homepage
from revenue import revenue_App
from pcrev import pcrev_App
from plrev import plrev_App
from biz import biz_App
from data import df_revenue, sources, df_rev, df_pc, df_pop, df_biz, categories_table, text, df_bidness
import os
from dotenv import load_dotenv
import plotly.graph_objs as go

load_dotenv()

app = dash.Dash()
application = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

# print(df_revenue.head())

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/revenue':
        return revenue_App()
    elif pathname == '/pcrev':
        return pcrev_App()
    elif pathname == '/plrev':
        return plrev_App()
    elif pathname == '/biz':
        return biz_App()
    else:
        return Homepage()

##########################################  REVENUE CALLBACKS ###############################
@app.callback(
    Output('crat', 'children'),
    Input('revenue-map', 'clickData'))
def clean_crat(clickData):
    county_revenue_df = df_rev.groupby(['county', 'year'])
    crat = county_revenue_df.sum()
    crat.reset_index(inplace=True)
    # print(crat)
    return crat.to_json()

@app.callback(
    Output('rev-scatter', 'figure'),
    [Input('revenue-map', 'clickData'),
    Input('year','value'),
    Input('rev', 'value')])
def create_rev_scat(clickData,year,rev):
    # print(rev)
    # print(df_rev)
    year_df = df_rev[df_rev['year'] == str(year)]
    # print(year_df)
    filtered_df = year_df[year_df['county'] == clickData['points'][-1]['text']]
    # print(filtered_df.head())
    # filtered_df['month'] = filtered_df['month'].astype(int)
    filtered_df = filtered_df.sort_values('month')
    # print(filtered_df.head())
    labels = ['Feb', 'Apr', 'Jun','Aug','Oct','Dec']
    tickvals = [2,4,6,8,10,12]
    traces = []


    if 'TOTAL' in rev:
            traces.append(go.Scatter(
            x = filtered_df['month'],
            y = filtered_df['tot_sales'],
            name = 'Total Sales',
            line = {'color':'red'} 
            ))
    if 'REC' in rev:  
            traces.append(go.Scatter(
            x = filtered_df['month'],
            y = filtered_df['rec_sales'],
            name = 'Rec Sales',
            line = {'color':'dodgerblue'}
            ))
    if 'MED' in rev:  
            traces.append(go.Scatter(
            x = filtered_df['month'],
            y = filtered_df['med_sales'],
            name = 'Med Sales',
            line = {'color':'black'}
            ))

    return {
            'data': traces,
            'layout': go.Layout(
                xaxis = {'title': 'Month','tickvals':tickvals,'tickmode': 'array','ticktext': labels},
                yaxis = {'title': 'Revenue'},
                hovermode = 'closest',
                title = '{} COUNTY {} REVENUE - {}'.format(clickData['points'][-1]['text'],rev,year),
                height = 350,
                font = {'size': 8}
            )
        }

@app.callback(
    Output('rev-bar', 'figure'),
    [Input('revenue-map', 'clickData'),
    Input('crat', 'children')])         
def create_month_bar(clickData, crat):
    # print(clickData)
    # print(df_revenue.head())
    crat = pd.read_json(crat)
    crat.reset_index(inplace=True)
    # print(crat)
    filtered_county = crat['county'] ==  clickData['points'][-1]['text']
    # # print(filtered_county)
    selected_county = crat[filtered_county]
    # selected_county.reset_index(inplace=True)
    # print(selected_county)

    trace1 = [
        {'x': selected_county['year'], 'y': selected_county['med_sales'], 'type': 'bar', 'name': 'Med Sales' },
        {'x': selected_county['year'], 'y': selected_county['rec_sales'], 'type': 'bar', 'name': 'Rec Sales' },
        {'x': selected_county['year'], 'y': selected_county['tot_sales'], 'type': 'bar', 'name': 'Tot Sales' },
    ]

    
    return {
        'data': trace1,
        'layout': go.Layout(
            height = 350,
            title = '{} COUNTY REVENUE BY YEAR'.format(clickData['points'][-1]['text']),
            font = {'size': 8}
        ),
    }


@app.callback(
     Output('revenue-map', 'figure'),
     Input('year', 'value'))         
def update_rev_map(selected_year):
   
    year1 = selected_year
  
     
    df_year = df_revenue.loc[df_revenue['year'] == selected_year]
    df_smr = pd.DataFrame({'county': df_year['county'], 'year': df_year.year, 'total revenue': df_year.tot_sales,'CENT_LAT':df_year.CENT_LAT,
                    'CENT_LON':df_year.CENT_LONG, 'marker_size':(df_year.tot_sales)*(.35**14)})

    df_smr_filtered = df_smr.loc[df_year['color'] == 'red']

    color_counties = df_smr_filtered['county'].unique().tolist()
     
    def fill_color():
        for k in range(len(sources)):
            if sources[k]['features'][0]['properties']['COUNTY'] in color_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'lightgreen'
            else: sources[k]['features'][0]['properties']['COLOR'] = 'white'                 
    fill_color()
    
    layers=[dict(sourcetype = 'json',
        source =sources[k],
        below="water", 
        type = 'fill',
        color = sources[k]['features'][0]['properties']['COLOR'],
        opacity = 0.5
        ) for k in range(len(sources))]
    data = [dict(
        lat = df_smr['CENT_LAT'],
        lon = df_smr['CENT_LON'],
        text = df_smr['county'],
        hoverinfo = 'text',
        type = 'scattermapbox',
        #    customdata = df['uid'],
        marker = dict(size=df_smr['marker_size'],color='forestgreen',opacity=.5),
        )]
    layout = dict(
            mapbox = dict(
                accesstoken = os.environ.get("mapbox_token"),
                center = dict(lat=39.05, lon=-105.5),
                zoom = 5.85,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 450,
            margin = dict(r=0, l=0, t=0, b=0)
            )
    fig = dict(data=data, layout=layout)
    return fig

######################### Per Cap Revenue #################

@app.callback(
     Output('pcrev-map', 'figure'),
     Input('year', 'value'))         
def update_rev_map(selected_year):
   
    year1 = selected_year
    
    df_year = df_pc.loc[df_pc['year'] == selected_year]
    df_smr = pd.DataFrame({'county': df_year['county'], 'year': df_year.year, 'revenue per cap.': df_year.pc_rev,'CENT_LAT':df_year.CENT_LAT,
                         'CENT_LON':df_year.CENT_LONG, 'marker_size':(df_year.pc_rev)*(.5**4)})

    df_smr_filtered = df_smr.loc[df_year['color'] == 'red']

    color_counties = df_smr_filtered['county'].unique().tolist()
     
    def fill_color():
        for k in range(len(sources)):
            if sources[k]['features'][0]['properties']['COUNTY'] in color_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'lightgreen'
            else: sources[k]['features'][0]['properties']['COLOR'] = 'white'                 
    fill_color()
    
    layers=[dict(sourcetype = 'json',
        source =sources[k],
        below="water", 
        type = 'fill',
        color = sources[k]['features'][0]['properties']['COLOR'],
        opacity = 0.5
        ) for k in range(len(sources))]
    data = [dict(
        lat = df_smr['CENT_LAT'],
        lon = df_smr['CENT_LON'],
        text = df_smr['county'],
        hoverinfo = 'text',
        type = 'scattermapbox',
        #    customdata = df['uid'],
        marker = dict(size=df_smr['marker_size'],color='forestgreen',opacity=.5),
        )]
    layout = dict(
            mapbox = dict(
                accesstoken = os.environ.get("mapbox_token"),
                center = dict(lat=39.05, lon=-105.5),
                zoom = 5.85,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 450,
            margin = dict(r=0, l=0, t=0, b=0)
            )
    fig = dict(data=data, layout=layout)
    return fig


@app.callback(
     Output('per-cap-rev-bar', 'figure'),
     [Input('pcrev-map', 'clickData'),
     Input('year2', 'value')])
def display_cnty_pop(clickData, selected_year):
    county = clickData['points'][-1]['text']
    df_rev = df_revenue[df_revenue['county'] == county]
    df_rev = df_rev[df_rev['year'] < 2021]
    # print(df_pc)
    df_pcrev = df_pc[df_pc['county'] == county]

    df_county_pop = df_pop[df_pop['county'] == county]
    df_county_pop = df_county_pop[(df_county_pop['year'] >= selected_year[0]) & (df_county_pop['year'] <= selected_year[1])]


    fig = go.Figure(
        data=[
        #    go.Bar(
        #         name='Annual Revenue',
        #         x=df_rev['year'],
        #         y=df_rev['tot_sales'],
        #         yaxis='y',
        #         # offsetgroup=1
        #    ),
            go.Scatter(
                name='Population',
                x=df_county_pop['year'],
                y=df_county_pop['totalpopulation'],
                yaxis='y2',
                # offsetgroup=2
            ),
            go.Bar(
                name='Per Cap Revenue',
                x=df_pcrev['year'],
                y=df_pcrev['pc_rev'],
                yaxis='y',
                # offsetgroup=1
            ),
        #    go.Bar(
        #         name='Business Count',
        #         x=df_biz_count['year'],
        #         y=df_biz_count['licensee'],
        #         yaxis='y2',
        #         offsetgroup=2
        #    ),
        ],
        layout={
            'yaxis': {'title': 'Revenue'},
            'yaxis2': {'title': 'Population', 'overlaying': 'y', 'side': 'right'},
            'height': 450,
        }
    )
    
    fig.update_layout(
        barmode='group',
        title={
            'text':'{} COUNTY'.format(county),
            'x':0.5,
            'xanchor':'center'
        }
    )
   
    return fig

# License Rev Callbacks ###############################
@app.callback(
     Output('plrev-map', 'figure'),
     Input('year', 'value'))         
def update_lic_map(selected_year):
   
    year1 = selected_year
    
    df_year = df_pc.loc[df_pc['year'] == 2019]
    df_smr = pd.DataFrame({'county': df_year['county'], 'year': df_year.year, 'revenue per cap.': df_year.pc_rev,'CENT_LAT':df_year.CENT_LAT,
                         'CENT_LON':df_year.CENT_LONG, 'marker_size':.5})

    df_smr_filtered = df_smr.loc[df_year['color'] == 'red']

    # color_counties = df_smr_filtered['county'].unique().tolist()

    # df_bpc = df_biz[df_biz['County'] == county]
    # biz_count  = len(df_bpc.index)
    df_cbc = df_biz.groupby(['County'], as_index=False)['License_No'].count()
    df_cbc = df_cbc.rename(columns={'License_No':'lic_count'})
    print(df_cbc)

    df_combo = pd.merge(df_year, df_cbc, how='left', left_on=['county'], right_on=['County'])
    print(df_combo.columns)
    df_combo['rpl'] = df_combo['tot_sales'] / df_combo['lic_count']
    df_combo.fillna(0, inplace=True)
    print(df_combo)
    rev_max = df_combo['rpl'].max()
    rev_min = 0
    print(rev_max)

    # def discrete_colorscale(bvals, colors):
    #     if len(bvals) != len(colors)+1:
    #         raise ValueError('len(boundary values) should be equal to  len(colors)+1')
    #     bvals = sorted(bvals)     
    #     nvals = [(v-bvals[0])/(bvals[-1]-bvals[0]) for v in bvals]  #normalized values
    
    #     dcolorscale = [] #discrete colorscale
    #     for k in range(len(colors)):
    #         dcolorscale.extend([[nvals[k], colors[k]], [nvals[k+1], colors[k]]])
    #     return dcolorscale    

    # bvals = [1, 250000, 500000, 750000, 1000000, 1250000, 1500000]
    # colors = ['#98FB98', '#00FF7F', '#7CFC00', '#32CD32', '#228B22', '#006400']

    # dcolorsc = discrete_colorscale(bvals, colors)

    # print(dcolorsc)
    def get_color(x):
        if x == 0:
            return 'white'
        elif 0 < x <= 250000 :
            return 'palegreen'
        elif 250000 < x <= 500000:
            return 'lightgreen'
        elif 500000 < x <= 1000000:
            return 'limegreen'
        elif 1000000 < x <= 1500000:
            return 'forestgreen'
        else:
            return 'darkgreen'

    
    
    df_combo['color'] = df_combo['rpl'].map(get_color)
    print(df_combo)

    df_white_counties = df_combo.loc[df_combo['color'] == 'white']
    # print(df_white_counties)
    white_counties = df_white_counties['county'].unique().tolist()
    # print(white_counties)
    df_pg_counties = df_combo.loc[df_combo['color'] == 'palegreen']
    pg_counties = df_pg_counties['county'].unique().tolist()
    df_lg_counties = df_combo.loc[df_combo['color'] == 'lightgreen']
    lg_counties = df_pg_counties['county'].unique().tolist()
    df_lime_counties = df_combo.loc[df_combo['color'] == 'limegreen']
    lime_counties = df_lime_counties['county'].unique().tolist()
    df_forest_counties = df_combo.loc[df_combo['color'] == 'forestgreen']
    forest_counties = df_forest_counties['county'].unique().tolist()
    df_dark_counties = df_combo.loc[df_combo['color'] == 'darkgreen']
    dark_counties = df_dark_counties['county'].unique().tolist()
    print(lime_counties)


     
    def fill_color():
        for k in range(len(sources)):
            if sources[k]['features'][0]['properties']['COUNTY'] in white_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'white'
            elif sources[k]['features'][0]['properties']['COUNTY'] in pg_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'palegreen'
            elif sources[k]['features'][0]['properties']['COUNTY'] in lg_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'lightgreen'
            elif sources[k]['features'][0]['properties']['COUNTY'] in lime_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'limegreen'
            elif sources[k]['features'][0]['properties']['COUNTY'] in forest_counties:
                sources[k]['features'][0]['properties']['COLOR'] = 'forestgreen'  
            else:
                sources[k]['features'][0]['properties']['COLOR'] = 'darkgreen'              
    fill_color()
    
    layers=[dict(sourcetype = 'json',
        source =sources[k],
        below="water", 
        type = 'fill',
        color = sources[k]['features'][0]['properties']['COLOR'],
        opacity = 0.5
        ) for k in range(len(sources))]
    data = [dict(
        lat = df_smr['CENT_LAT'],
        lon = df_smr['CENT_LON'],
        text = df_smr['county'],
        hoverinfo = 'text',
        type = 'scattermapbox',
        #    customdata = df['uid'],
        marker = dict(size=df_smr['marker_size'],color='forestgreen',opacity=.5),
        )]
    layout = dict(
            mapbox = dict(
                accesstoken = os.environ.get("mapbox_token"),
                center = dict(lat=39.05, lon=-105.5),
                zoom = 5.85,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 450,
            margin = dict(r=0, l=0, t=0, b=0)
            )
    fig = dict(data=data, layout=layout)
    return fig

# @app.callback(
#      Output('per-lic-rev-bar', 'figure'),
#      [Input('plrev-map', 'clickData'),
#      Input('year2', 'value')])
# def display_cnty_pop(clickData, selected_year):
#     county = clickData['points'][-1]['text']
#     df_rev = df_revenue[df_revenue['county'] == county]
#     df_rev = df_rev[df_rev['year'] < 2021]
#     # print(df_pc)
#     df_pcrev = df_pc[df_pc['county'] == county]
#     print(df_pcrev)
#     # buisinesses per county
#     df_bpc = df_biz[df_biz['County'] == county]
#     biz_count  = len(df_bpc.index)
#     print(biz_count)
#     # df_bpc = df_bpc.drop(['geometry', 'color', 'lat', 'long', 'Certification', 'source_geo', 'Month', 'Year', 'Street_Address', 'ZIP', 'DBA'], axis=1)
#     # print(df_bpc.columns)
#     # print(df_bpc)

#     # df_county_pop = df_pop[df_pop['county'] == county]
#     # df_county_pop = df_county_pop[(df_county_pop['year'] >= selected_year[0]) & (df_county_pop['year'] <= selected_year[1])]


#     fig = go.Figure(
#         data=[
#         #    go.Bar(
#         #         name='Annual Revenue',
#         #         x=df_rev['year'],
#         #         y=df_rev['tot_sales'],
#         #         yaxis='y',
#         #         # offsetgroup=1
#         #    ),
#             go.Scatter(
#                 name='Population',
#                 x=df_county_pop['year'],
#                 y=df_county_pop['totalpopulation'],
#                 yaxis='y2',
#                 # offsetgroup=2
#             ),
#             go.Bar(
#                 name='Per Cap Revenue',
#                 x=df_pcrev['year'],
#                 y=df_pcrev['pc_rev'],
#                 yaxis='y',
#                 # offsetgroup=1
#             ),
#         #    go.Bar(
#         #         name='Business Count',
#         #         x=df_biz_count['year'],
#         #         y=df_biz_count['licensee'],
#         #         yaxis='y2',
#         #         offsetgroup=2
#         #    ),
#         ],
#         layout={
#             'yaxis': {'title': 'Revenue'},
#             'yaxis2': {'title': 'Population', 'overlaying': 'y', 'side': 'right'},
#             'height': 450,
#         }
#     )
    
#     fig.update_layout(
#         barmode='group',
#         title={
#             'text':'{} COUNTY'.format(county),
#             'x':0.5,
#             'xanchor':'center'
#         }
#     )
   
#     return fig

# Businesses Callbacks #####################################################

@app.callback(
    Output('biz-map', 'figure'),
    Input('categories', 'value'))
def update_biz_map(selected_values):
    print(df_biz)
    print(df_biz.columns)
    print(df_biz['License_No'])
    # rpd_s = rpd.sort_values(by=['RId2'])
  
    # rpd_s = rpd_s.apply(pd.to_numeric, errors='ignore')
    # rpd_s = rpd_s.fillna(0)

    # data = [dict(
    #         type = 'scattermapbox',
    #     )]

    # print(df_biz)
    # df1 = pd.DataFrame(df.loc[df['Category'] == selected_values])
    # if selected_values == 'all':
    # filtered_df = df
    def fill_color():
        for k in range(len(sources)):
            sources[k]['features'][0]['properties']['COLOR'] = 'white'                 
    fill_color()

    layers=[dict(sourcetype = 'json',
        source =sources[k],
        below="water", 
        type = 'fill',
        color = sources[k]['features'][0]['properties']['COLOR'],
        opacity = 0.5
        ) for k in range(len(sources))]

    data = [dict(
        lat = df_biz['lat'],
        lon = df_biz['long'],
        text = text,
        hoverinfo = 'text',
        type = 'scattermapbox',
        customdata = df_biz['uid'],
        marker = dict(size=10,color=df_biz['color'],opacity=.6)
    )]
    # else: 
    #         filtered_df = df1
    #         data = [dict(
    #             lat = filtered_df['lat'],
    #             lon = filtered_df['long'],
    #             text = text,
    #             hoverinfo = 'text',
    #             type = 'scattermapbox',
    #             customdata = df1['uid'],
    #             marker = dict(size=7,color=df1['color'],opacity=.6)
    #         )]
    
    layout = dict(
            mapbox = dict(
                accesstoken = os.environ.get("mapbox_token"),
                center = dict(lat=39, lon=-105.5),
                # zoom = 5.6,
                zoom = 6,
                style = 'light',
                layers = layers
            ),
            hovermode = 'closest',
            height = 500,
            margin = dict(r=0, l=0, t=0, b=0),
            clickmode = 'event+select'
        )  
  
    fig = dict(data=data, layout=layout)
    return fig



if __name__ == '__main__':
    app.run_server(port=8000, debug=True)