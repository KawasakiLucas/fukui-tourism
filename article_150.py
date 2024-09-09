# Article150 Population Map by Prefecture v00.py

'''
References

https://www.e-stat.go.jp/

https://plotly.com/python/choropleth-maps/

https://plotly.com/python/colorscales/

https://www.mapbox.com/

https://plotly.com/python/mapbox-county-choropleth/

https://plotly.com/python/mapbox-layers/
'''

# %%

import json
import urllib.request
import numpy as np
import math
import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go


# %%

### 0: Prepare geojason / census data for analysis by cleaning and transforming the data

### 0-1: Read a GeoJson file

url = r'https://money-or-ikigai.com/Menu/Python/Article/data/map/prefectures.json'
response = urllib.request.urlopen(url)
geo_data = response.read().decode('utf-8')
japan_prefectures = json.loads(geo_data)
# json_file = 'data/json/prefectures.json'
# japan_prefectures = json.load(open(json_file, 'r'))
japan_prefectures


# %%

### 0-2: Load a prefecture id map dictionary from the geojson data
# Create an empty dictionary to store prefecture IDs
prefecture_id_map = {}

# Loop through the "features" list in the "japan_prefectures" dictionary
for feature in japan_prefectures['features']:
    feature['id'] = feature['properties']['pref']
    prefecture_id_map[feature['properties']['name']] = feature['id']

prefecture_id_map


# %%

### 0-3: Load Japan census data from a csv file

csv_file = r'https://money-or-ikigai.com/Menu/Python/Article/data/map/japan_census_all.csv'
# csv_file = 'data/csv/japan_census_all.csv'
df = pd.read_csv(csv_file)
# df.info()
# df
dfx = df.query("year == 2021")
dfx.shape   # (47, 5)


# %%

### 0-4: Load Japan geo data from a csv file

geo_csv = r'https://money-or-ikigai.com/Menu/Python/Article/data/map/japan_geo.csv'
# geo_csv = 'data/csv/japan_geo.csv'
geo_df = pd.read_csv(geo_csv)
geo_df


# %%

### 0-5: Filter columns from the pandas dataframe.

geo_df = geo_df[['region_en','region_jp','prefecture_en','prefecture_jp']]
geo_df


# %%

### 0-6: Concatenate the Japan census and geojason data horizontally based on the 'prefecture_jp' column

# Set the "prefecture_jp" column as the index for the "dfx" DataFrame
dfx.set_index('prefecture_jp', inplace=True)

# Set the "prefecture_jp" column as the index for the "geo_df" DataFrame
geo_df.set_index('prefecture_jp', inplace=True)

# Concatenate the "dfx" and "geo_df" DataFrames
# along the columns axis (axis=1) and store the result in "dfy"
dfy = pd.concat([dfx, geo_df], axis=1)
dfy


# %%

### 0-7: Add a new column 'id' into the dataframe.

# Create a new column named "id" in the "dfy" DataFrame
# by applying a lambda function to the "prefecture_en" column.
# The lambda function maps each prefecture name in the "prefecture_en" column
# to its corresponding ID in the "prefecture_id_map" dictionary.
# The resulting IDs are assigned to the "id" column
dfy['id'] = dfy['prefecture_en'].apply(lambda x: prefecture_id_map[x])
dfy


# %%

### 0-8: Calculate male/female ratios.

dfy.reset_index(inplace=True)

raw_df = dfy.copy()

raw_df['male_ratio'] = raw_df.apply(lambda row: round(row['male'] / row['population'],2), axis=1)
raw_df['female_ratio'] = raw_df.apply(lambda row: round(row['female'] / row['population'],2), axis=1)
raw_df['male_ratio_scale'] = np.log10(raw_df['male_ratio'])
raw_df


# %%

### 1: Map population

# set a defulat template
pio.templates.default = 'plotly_dark'

# Default template: 'plotly_dark'
# Available templates:
#     ['ggplot2', 'seaborn', 'simple_white', 'plotly',
#         'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
#         'ygridoff', 'gridon', 'none']

### 1-1: map population by prefecture

df = raw_df.copy()

fig = px.choropleth(
    df,
    locations='id',
    geojson=japan_prefectures,
    color='population',
    hover_name='prefecture_jp',
    hover_data=['male_ratio', 'female_ratio'],
    labels=dict(
                prefecture_jp='都道府県',
                population='人口',
                male_ratio='男性比率',
                female_ratio='女性比率',
                ),
    title='都道府県別人口 (2021年度)',
)

fig.update_geos(fitbounds='locations', visible=False)

fig.show()


# %%

### 1-2: Map population by prefecture
# add a color_continuous_scale, color_continuous_midpoint

df = raw_df.copy()

fig = px.choropleth(
    df,
    locations='id',
    geojson=japan_prefectures,
    color='population',
    hover_name='prefecture_jp',
    hover_data=['male_ratio', 'female_ratio'],
    color_continuous_scale=px.colors.diverging.BrBG,
    color_continuous_midpoint=0,
    labels=dict(
                prefecture_jp='都道府県',
                population='人口',
                male_ratio='男性比率',
                female_ratio='女性比率',
                ),
    title='都道府県別人口 (2021年度)',
)

fig.update_geos(fitbounds='locations', visible=False)

fig.show()


# %%

### 1-3: Map population by prefecture
# draw a map using choropleth_mapbox()

df = raw_df.copy()

fig = px.choropleth_mapbox(
    df,
    locations='id',
    geojson=japan_prefectures,
    color='population',
    hover_name='prefecture_jp',
    hover_data=['male_ratio', 'female_ratio'],
    mapbox_style='carto-positron',
    center={'lat': 35, 'lon': 139},
    zoom=3,
    opacity=0.5,
    labels=dict(
                prefecture_jp='都道府県',
                population='人口',
                male_ratio='男性比率',
                female_ratio='女性比率',
                ),
    title='都道府県別人口 (2021年度)',
)

fig.show()


# %%

### 2: Draw a sunburst chart

df = raw_df.copy()

### 2-1: Draw a sunburst chart : English
# tips: click continent ★
fig = px.sunburst(df,
            path=['region_en','prefecture_en'],
            values='population',
            hover_name='prefecture_jp',
            color='population',
            height=700,
            labels=dict(
                population='Population',
                prefecture_jp='Prefecture',
                region_en='Region'
                ),
            title="px.sunburst(,path=['region_en','prefecture_en'], values='population', color='population')")

fig.show()


# %%

### 2-2: Draw a sunburst chart : Japanese
# tips: click continent ★
fig = px.sunburst(df,
            path=['region_jp','prefecture_jp'],
            values='population',
            hover_name='prefecture_jp',
            color='population',
            height=700,
            labels=dict(
                labels='地方',
                parent='親',
                population='人口',
                population_sum='人口総数',
                prefecture_jp='都道府県',
                region_en='地域'
            ),
            title="地方別・都道府県別人口 (2021年度)")

fig.show()

# %%

### 3: Draw a treemap chart

### 3-1: Draw a treemap chart : English
# tips: click continent ★
fig = px.treemap(df,
           path=['region_en','prefecture_en'],
           values='population',
           hover_name='prefecture_en',
           color='population',
           height=700,
           labels=dict(
                population='Population',
                prefecture_jp='Prefecture',
                region_en='Region'
           ),
           title="px.treemap(,path=['region_en','prefecture_en'], values='population', color='population')")

fig.show()


# %%

### 3-2 Draw a treemap chart : Japanese
# tips: click continent ★
fig = px.treemap(df,
           path=['region_jp','prefecture_jp'],
           values='population',
           hover_name='prefecture_jp',
           color='population',
           height=700,
           labels=dict(
                population='人口',
                prefecture_jp='都道府県',
                region_en='地域'
           ),
           title="地方別・都道府県別人口 (2021年度)")

fig.show()

# %%

### 4: Draw a bar chart : English

### 4-1 bar chart: Japan population by prefecture in 2021
df = raw_df.copy()

fig = px.bar(df,
             x='prefecture_en', y='population',
             color='prefecture_en',
             labels=dict(
                    population='Population',
                    prefecture_en='Prefecture',
                    region_en='Region'
             ),
            title='Japan population by prefecture in 2021'
)

fig.show()


# %%

### 4-2: Draw a bar chart : Japanese
# add a hover_name, hover_data and labels
fig = px.bar(df,
             x='prefecture_jp', y='population',
             color='prefecture_jp',
             hover_name='prefecture_jp',
             hover_data=['male_ratio', 'female_ratio'],
             labels=dict(
                        prefecture_jp='都道府県',
                        population='人口',
                        male_ratio='男性比率',
                        female_ratio='女性比率',
                        ),
             title='都道府県別人口 (2021年度)'
)

fig.show()


# %%

### 4-3: Draw a vertical bar chart
# top 10 (vertical bar chart)

df = raw_df.copy()
df = df.nlargest(10, 'population')
df.reset_index(inplace=True)
df['rank'] = df.index+1

fig = px.bar(df,
             x='prefecture_jp', y='population',
             color='prefecture_jp',
             text='rank',
             hover_name='prefecture_jp',
             hover_data=['male_ratio', 'female_ratio'],
             labels=dict(
                        prefecture_jp='都道府県',
                        population='人口',
                        male_ratio='男性比率',
                        female_ratio='女性比率',
                        ),
             title='都道府県別人口 上位１０ (2021年度)'
)

fig.show()


# %%

### 4-4: Draw a horizontal bar chart
#  top 10 (horizontal bar chart)

df = raw_df.copy()
df = df.nlargest(10, 'population')
df.reset_index(inplace=True)
df['rank'] = df.index+1

fig = px.bar(df,
             y='prefecture_jp', x='population',
             color='prefecture_jp',
             orientation='h',   # h-horizontal, v-vertical
             text='population', # rank or population
             hover_name='prefecture_jp',
             hover_data=['rank', 'male_ratio', 'female_ratio'],
             labels=dict(
                        prefecture_jp='都道府県',
                        population='人口',
                        rank='順位',
                        male_ratio='男性比率',
                        female_ratio='女性比率',
                        ),
             title='都道府県別人口 上位１０ (2021年度)'
)

fig.update_traces(texttemplate='%{x:.2s}', textposition='inside')

fig.show()


# %%

### 4-5: Draw a horizontal bar chart by gender
#  top 10 (horizontal bar chat by gender)

df = raw_df.copy()
df = df.nlargest(10, 'population')
df.reset_index(inplace=True)
df['rank'] = df.index+1

# Group the "df" DataFrame by "prefecture_jp",
# summing the "male" and "female" columns, and reset the index
grp_df = df.groupby('prefecture_jp')[['male', 'female']].sum().reset_index()

# Reshape the "grp_df" DataFrame
# from wide to long format using the "melt()" method
melted_df = grp_df.melt(id_vars='prefecture_jp', var_name='gender', value_name='population')

# Replace the "male" and "female" values in the "gender" column
# with the Japanese equivalents "男性" and "女性", respectively
melted_df['gender'] = melted_df['gender'].apply(lambda x: x.replace('female','女性'))
melted_df['gender'] = melted_df['gender'].apply(lambda x: x.replace('male','男性'))

fig = px.bar(melted_df,
              x='population', y='gender',
              color='prefecture_jp',
              orientation='h',   # h-horizontal, v-vertical
              text='population',
              hover_name='prefecture_jp',
              # hover_data=['population'],
              labels=dict(
                            prefecture_jp='都道府県',
                            population='人口',
                            gender='性別'
                         ),
              title='都道府県別・男女比 上位１０ (2021年度)'
             )

fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')

fig.show()


# %%

### 4-6: Draw a horizontal bar chart by gender
# top 10 (horizontal bar chat by gender)

df = raw_df.copy()
df = df.nlargest(10, 'population')
df.reset_index(inplace=True)
df['rank'] = df.index+1

# Create a bar chart using Plotly with separate bars for male and female populations

fig = go.Figure()

# add a female bar chart
fig.add_trace(go.Bar(
    y=df['prefecture_jp'],
    x=df['female']*-1,
    orientation='h',
    name='女性',
    text=df['female'],
    textposition='inside',
    # marker=dict(color='red')
    marker=dict(color='#FFC0CB')
))

# add a male bar chart
fig.add_trace(go.Bar(
    y=df['prefecture_jp'],
    x=df['male'],
    orientation='h',
    name='男性',
    text=df['male'],
    textposition='inside',
    # marker=dict(color='green')
    marker=dict(color='#6495ED')
))

# Customize the chart layout with titles, legends, and axis labels
fig.update_layout(
    barmode='overlay',
    xaxis=dict(
        side='top',
        tickfont=dict(size=10)
    ),
    yaxis=dict(
        tickfont=dict(size=10),
        anchor='x',
        mirror=True
    ),
    title='都道府県別・男女別人口 上位１０ (2021年度)',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),
    height=600,
    margin=dict(l=150, r=50, t=50, b=50)
)

# fig.update_traces(texttemplate='%{x:.2s}', textposition='inside')

fig.update_traces(texttemplate='%{x:,.0f}', textposition='inside')

fig.show()


# %%

### 4-7: Draw a vertical bar chart
#  bottom 10 (Vertical bar chart)

df = raw_df.copy()
df = df.nsmallest(10, 'population')
df.reset_index(inplace=True)
df['rank'] = df.index+1

fig = px.bar(df,
             x='prefecture_jp', y='population',
             color='prefecture_jp',
             text='rank',
             hover_name='prefecture_jp',
             hover_data=['male_ratio', 'female_ratio'],
             labels=dict(
                        prefecture_jp='都道府県',
                        population='人口',
                        rank='順位',
                        male_ratio='男性比率',
                        female_ratio='女性比率',
                        ),
             title='都道府県別人口 下位１０ (2021年度)'
)

fig.show()


# %%

### 4-8: Draw a horizontal bar chart
# bottom 10 (Horizontal bar chart)

df = raw_df.copy()
df = df.nsmallest(10, 'population')
df.reset_index(inplace=True)
df['rank'] = df.index+1

fig = px.bar(df,
             y='prefecture_jp', x='population',
             color='prefecture_jp',
             orientation='h',   # h-horizontal, v-vertical
             text='rank',
             hover_name='prefecture_jp',
             hover_data=['male_ratio', 'female_ratio'],
             labels=dict(
                         prefecture_jp='都道府県',
                         population='人口',
                         rank='順位',
                         male_ratio='男性比率',
                         female_ratio='女性比率',
                        ),
             title='都道府県別人口 下位１０ (2021年度)'
            )

fig.show()  
