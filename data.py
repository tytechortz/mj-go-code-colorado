import pandas as pd
import geopandas as gpd
from sodapy import Socrata
import json

client = Socrata("data.colorado.gov", None)


# initial data fetch
mj_results = client.get("j7a3-jgd3", limit=6000)


# revenue data
df_rev = pd.DataFrame.from_records(mj_results)
df_rev['county'] = df_rev['county'].str.upper()
df_rev.fillna(0, inplace=True)
df_rev['med_sales'] = df_rev['med_sales'].astype(int)
df_rev['rec_sales'] = df_rev['rec_sales'].astype(int)
df_rev['tot_sales'] = df_rev['med_sales'] + df_rev['rec_sales']
# print(df_revenue.head())
# df_cnty_rev = df_rev.groupby(['county', 'year'])
# crat = df_cnty_rev.sum()
# print(crat)
df_revenue = df_rev.groupby(['year', 'county']).agg({'tot_sales': 'sum'})
df_revenue = df_revenue.reset_index()
df_revenue.loc[df_revenue['tot_sales'] > 0, 'color'] = 'red'
df_revenue.loc[df_revenue['tot_sales'] == 0, 'color'] = 'blue'
df_revenue['year'] = df_revenue['year'].astype(int)
# print(df_revenue)

counties = gpd.read_file('./data/Colorado_County_Boundaries.geojson')
# print(counties)
df_lat_lon = counties[['COUNTY', 'CENT_LAT', 'CENT_LONG']]
# merge revenue and county boundaries 
df_revenue = pd.merge(df_revenue, df_lat_lon, how='left', left_on=['county'], right_on=['COUNTY'])

with open('./data/Colorado_County_Boundaries.json') as json_file:
    jdata = json_file.read()
    topoJSON = json.loads(jdata)

sources=[]
for feat in topoJSON['features']: 
        sources.append({"type": "FeatureCollection", 'features': [feat]})

