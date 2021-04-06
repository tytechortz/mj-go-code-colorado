import pandas as pd
from sodapy import Socrata

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