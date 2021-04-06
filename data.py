import pandas as pd
import geopandas as gpd
from sodapy import Socrata
import json

client = Socrata("data.colorado.gov", None)


# initial data fetch
mj_results = client.get("j7a3-jgd3", limit=6000)


# revenue data
df_revenue = pd.DataFrame.from_records(mj_results)
df_revenue['county'] = df_revenue['county'].str.upper()
df_revenue.fillna(0, inplace=True)
df_revenue['med_sales'] = df_revenue['med_sales'].astype(int)
df_revenue['rec_sales'] = df_revenue['rec_sales'].astype(int)
df_revenue['tot_sales'] = df_revenue['med_sales'] + df_revenue['rec_sales']
df_revenue = df_revenue.groupby(['year', 'county']).agg({'tot_sales': 'sum'})
df_revenue = df_revenue.reset_index()
df_revenue.loc[df_revenue['tot_sales'] > 0, 'color'] = 'red'
df_revenue.loc[df_revenue['tot_sales'] == 0, 'color'] = 'blue'
df_revenue['year'] = df_revenue['year'].astype(int)

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