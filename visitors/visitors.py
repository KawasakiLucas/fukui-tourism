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
from visitors import visitors

# JAPAN Visitors per prefecture: gender ratios
# Function that create the gender ratios and assign to the dataframe
# based on prefectures
def japan_visitors(df):
    df = df.groupby('都道府県', as_index=False).sum()
    df = df.assign(total_visitors = lambda x: (
        x['性別_その他'] + x['性別_女'] + x['性別_無回答'] + x['性別_男']))
    df = df.assign(female_ratio = lambda x: round(x['性別_女']/x['total_visitors'],2))
    df = df.assign(male_ratio = lambda x: round(x['性別_男']/x['total_visitors'],2))
    df = df.assign(other_ratio = lambda x: round(x['性別_その他']/x['total_visitors'],2))
    df = df.assign(nashi_ratio = lambda x: round(x['性別_無回答']/x['total_visitors'],2))
    df = df[['都道府県', 'total_visitors', '性別_女', '性別_男', '性別_その他', '性別_無回答',
             'female_ratio', 'male_ratio', 'other_ratio', 'nashi_ratio']]
    return df

# FUKUI Visitors: gender ratios
# Function that create the gender ratios and assign to the dataframe
# based on cities
def fukui_visitors(df):
    df = df.groupby('会員市町村', as_index=False).sum()
    df = df.assign(total_visitors = lambda x: (
        x['性別_その他'] + x['性別_女'] + x['性別_無回答'] + x['性別_男']))
    df = df.assign(female_ratio = lambda x: round(x['性別_女']/x['total_visitors'],2))
    df = df.assign(male_ratio = lambda x: round(x['性別_男']/x['total_visitors'],2))
    df = df.assign(other_ratio = lambda x: round(x['性別_その他']/x['total_visitors'],2))
    df = df.assign(nashi_ratio = lambda x: round(x['性別_無回答']/x['total_visitors'],2))
    df = df[['会員市町村', 'total_visitors', '性別_女', '性別_男', '性別_その他', '性別_無回答',
             'female_ratio', 'male_ratio', 'other_ratio', 'nashi_ratio']]
    return df

# FUKUI Visitors: gender ratios
# Function that create the gender ratios and assign to the dataframe
# based on cities
def visited_places(df):
    df = df.groupby('市町村', as_index=False).sum()
    df = df.assign(total_visitors = lambda x: (
        x['性別_その他'] + x['性別_女'] + x['性別_無回答'] + x['性別_男']))
    df = df.assign(female_ratio = lambda x: round(x['性別_女']/x['total_visitors'],2))
    df = df.assign(male_ratio = lambda x: round(x['性別_男']/x['total_visitors'],2))
    df = df.assign(other_ratio = lambda x: round(x['性別_その他']/x['total_visitors'],2))
    df = df.assign(nashi_ratio = lambda x: round(x['性別_無回答']/x['total_visitors'],2))
    df = df[['市町村', 'total_visitors', '性別_女', '性別_男', '性別_その他', '性別_無回答',
             'female_ratio', 'male_ratio', 'other_ratio', 'nashi_ratio']]
    return df
