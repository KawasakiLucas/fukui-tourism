import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import geopandas as gpd
import shapefile as shp
from urllib.request import urlopen
import urllib
import json
from sklearn.preprocessing import OneHotEncoder
from visitors import visitors_map

# Function to create a JAPAN map
# default: JAPAN
# japan: zoom = 4.4, lat = 36.5, lon = 137.8, title = '都道府県別訪問者'
# fukui_out: zoom = 4.4, lat = 36.5, lon = 137.8, title = '福井県外訪問者'
def japan_map_visitors(df, japan_geojson, zoom = 3.5, lat = 36.5, lon = 137.8, title = '都道府県別訪問者'):
    pio.templates.default = 'plotly_white'
    df = df.copy()
    fig = px.choropleth_mapbox(
        df, locations='id', geojson=japan_geojson,
        color='total_visitors', color_continuous_scale=px.colors.sequential.Viridis, hover_name='都道府県',
        hover_data=['male_ratio', 'female_ratio', 'other_ratio', 'nashi_ratio'],
        mapbox_style='carto-positron', center={'lat': lat, 'lon': lon},
        zoom=zoom, opacity=0.5, title=title, #width=800, height=800,
        labels=dict(prefecture_jp='都道府県', total_visitors='訪問者数', male_ratio='男性比率',
                    female_ratio='女性比率', other_ratio='その他比率', nashi_ratio='無回答比率',),
    )
    fig.update_layout(margin={"r":100,"t":40,"l":30,"b":0})
    #fig.show()
    return fig

def japan_map_visitors_female(df, japan_geojson, zoom = 3.5, lat = 36.5, lon = 137.8, title = '都道府県別訪問者'):
    pio.templates.default = 'plotly_white'
    df = df.copy()
    fig = px.choropleth_mapbox(
        df, locations='id', geojson=japan_geojson,
        color='性別_女', color_continuous_scale=px.colors.sequential.Viridis, hover_name='都道府県',
        mapbox_style='carto-positron', center={'lat': lat, 'lon': lon},
        zoom=zoom, opacity=0.5, title=title, #width=800, height=800,
        labels=dict(prefecture_jp='都道府県', 性別_女='女訪問者数'),
    )
    fig.update_layout(margin={"r":100,"t":40,"l":30,"b":0})
    #fig.show()
    return fig







##########################################################################################################
# Function to create a FUKUI map
# default: FUKUI
# fukui_in: zoom = 8.3, lat = 35.9, lon = 136.13, title = '福井県内訪問者'
def fukui_map_visitors(df, fukui_geojson, zoom = 7.3, lat = 35.9, lon = 136.13, title = '福井県内訪問者'):
    pio.templates.default = 'plotly_white'
    df = df.copy()
    fig = px.choropleth_mapbox(
        df, locations='id', geojson=fukui_geojson,
        color='total_visitors', color_continuous_scale=px.colors.sequential.Viridis, hover_name='会員市町村',
        hover_data=['male_ratio', 'female_ratio', 'other_ratio', 'nashi_ratio'],
        mapbox_style='carto-positron', center={'lat': lat, 'lon': lon},
        zoom=zoom, opacity=0.5, title=title, #width=800, height=800,
        labels=dict(prefecture_jp='会員市町村', total_visitors='訪問者数', male_ratio='男性比率',
                    female_ratio='女性比率', other_ratio='その他比率', nashi_ratio='無回答比率',),
    )
    fig.update_layout(margin={"r":100,"t":40,"l":30,"b":0})
    #fig.show()
    return fig

def fukui_map_visitors_female(df, fukui_geojson, zoom = 7.3, lat = 35.9, lon = 136.13, title = '福井県内訪問者'):
    pio.templates.default = 'plotly_white'
    df = df.copy()
    fig = px.choropleth_mapbox(
        df, locations='id', geojson=fukui_geojson,
        color='性別_女', color_continuous_scale=px.colors.sequential.Viridis, hover_name='会員市町村',
        mapbox_style='carto-positron', center={'lat': lat, 'lon': lon},
        zoom=zoom, opacity=0.5, title=title, #width=800, height=800,
        labels=dict(prefecture_jp='会員市町村', 性別_女='女訪問者数'),
    )
    fig.update_layout(margin={"r":100,"t":40,"l":30,"b":0})
    #fig.show()
    return fig

# Function to create a FUKUI map
# default: FUKUI
# fukui_in: zoom = 7.3, lat = 35.9, lon = 136.13, title = '福井県内訪問者'
def fukui_map_visited(df, fukui_geojson, zoom = 7.3, lat = 35.9, lon = 136.13, title = '福井県内訪問者'):
    pio.templates.default = 'plotly_white'
    df = df.copy()
    fig = px.choropleth_mapbox(
        df, locations='id', geojson=fukui_geojson,
        color='total_visitors', color_continuous_scale=px.colors.sequential.Viridis, hover_name='市町村',
        hover_data=['male_ratio', 'female_ratio', 'other_ratio', 'nashi_ratio'],
        mapbox_style='carto-positron', center={'lat': lat, 'lon': lon},
        zoom=zoom, opacity=0.5, title=title, #width=800, height=800,
        labels=dict(prefecture_jp='市町村', total_visitors='訪問者数', male_ratio='男性比率',
                    female_ratio='女性比率', other_ratio='その他比率', nashi_ratio='無回答比率',),
    )
    fig.update_layout(margin={"r":100,"t":40,"l":30,"b":0})
    #fig.show()
    return fig
