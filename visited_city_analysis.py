import streamlit as st
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
from visitors import visitors, visitors_map

def main():
    ### 0: Prepare geojason
    #####################################################################################
    ### 0-2: Read FUKUI GeoJson file
    json_file = './fukui2.geojson'
    fukui_prefecture = json.load(open(json_file, 'r'))
    #####################################################################################

    ### 1: Load a prefecture id map dictionary
    #####################################################################################
    ### 1-1: From the FUKUI geojson data
    # Create an empty dictionary to store prefecture IDs
    city_id_map = {}

    # Loop through the "features" list in the "fukui_prefecture" dictionary
    for feature in fukui_prefecture['features']:
        feature['id'] = feature['properties']['id']
        city_id_map[feature['properties']['市町村']] = feature['id']
    #####################################################################################

    ### 2: Load datasets
    #####################################################################################
    ### 2-1: Load Fukui tourism dataset
    data = pd.read_csv('all.csv')
    #####################################################################################

    ### 3: Preprocessing
    #####################################################################################
    ### 3-1: Filter columns from Fukui tourism dataset and make some changes
    data_personal = data[['性別', '年代', '回答月', '都道府県', '市町村', '世帯年収']]

    # Create a dictionary with the average values from 世帯年収
    average = {
        '100万円未満': 100,
        '100万円以上 200万円未満': 150,
        '200万円以上 300万円未満': 250,
        '300万円以上 400万円未満': 350,
        '400万円以上 500万円未満': 450,
        '500万円以上 600万円未満': 550,
        '600万円以上 700万円未満': 650,
        '700万円以上 800万円未満': 750,
        '800万円以上 900万円未満': 850,
        '900万円以上 1,000万円未満': 950,
        '1,000万円以上 1,200万円未満': 1100,
        '1,200万円以上 1,500万円未満': 1350,
        '1,500万円以上': 1500,
        '分からない/無回答': np.nan
    }

    # Apply these values on 世帯年収
    data_personal['世帯年収'] = data_personal['世帯年収'].apply(lambda x: average[x])

    # Make a one hot enconder on '性別', '年代','世帯年収' for further analysis
    data_personal_ohe = pd.get_dummies(data_personal, columns = ['性別', '年代','世帯年収'], dtype='int64')

    ### 3-1: Split data
    japan = data_personal_ohe.copy()
    fukui_in = data_personal_ohe[data_personal_ohe['都道府県'] == '福井県']
    fukui_out = data_personal_ohe[data_personal_ohe['都道府県'] != '福井県']
    #####################################################################################


    ### 4: Call visitors package
    #####################################################################################

    # JAPAN
    # Create mask to filter data on seasons
    mask_spring = (japan['回答月'] == '3月') | (japan['回答月'] == '4月') | (japan['回答月'] == '5月')
    mask_summer = (japan['回答月'] == '6月') | (japan['回答月'] == '7月') | (japan['回答月'] == '8月')
    mask_autumn = (japan['回答月'] == '9月') | (japan['回答月'] == '10月') | (japan['回答月'] == '11月')
    mask_winter = (japan['回答月'] == '12月') | (japan['回答月'] == '1月') | (japan['回答月'] == '2月')

    # Total visitors Japan: gender ratios
    japan_visited = visitors.visited_places(japan)
    japan_visited_spring_df = visitors.visited_places(japan[mask_spring])
    japan_visited_summer_df = visitors.visited_places(japan[mask_summer])
    japan_visited_autumn_df = visitors.visited_places(japan[mask_autumn])
    japan_visited_winter_df = visitors.visited_places(japan[mask_winter])

    ################################################################################################################
    # FUKUI OUT
    # Create mask to filter data on seasons
    mask_spring = (fukui_out['回答月'] == '3月') | (fukui_out['回答月'] == '4月') | (fukui_out['回答月'] == '5月')
    mask_summer = (fukui_out['回答月'] == '6月') | (fukui_out['回答月'] == '7月') | (fukui_out['回答月'] == '8月')
    mask_autumn = (fukui_out['回答月'] == '9月') | (fukui_out['回答月'] == '10月') | (fukui_out['回答月'] == '11月')
    mask_winter = (fukui_out['回答月'] == '12月') | (fukui_out['回答月'] == '1月') | (fukui_out['回答月'] == '2月')

    # Total visitors Japan: gender ratios
    fukui_out_visited = visitors.visited_places(fukui_out)
    fukui_out_visited_spring_df = visitors.visited_places(fukui_out[mask_spring])
    fukui_out_visited_summer_df = visitors.visited_places(fukui_out[mask_summer])
    fukui_out_visited_autumn_df = visitors.visited_places(fukui_out[mask_autumn])
    fukui_out_visited_winter_df = visitors.visited_places(fukui_out[mask_winter])

    ################################################################################################################
    # FUKUI IN
    # Create mask to filter data on seasons
    mask_spring = (fukui_in['回答月'] == '3月') | (fukui_in['回答月'] == '4月') | (fukui_in['回答月'] == '5月')
    mask_summer = (fukui_in['回答月'] == '6月') | (fukui_in['回答月'] == '7月') | (fukui_in['回答月'] == '8月')
    mask_autumn = (fukui_in['回答月'] == '9月') | (fukui_in['回答月'] == '10月') | (fukui_in['回答月'] == '11月')
    mask_winter = (fukui_in['回答月'] == '12月') | (fukui_in['回答月'] == '1月') | (fukui_in['回答月'] == '2月')

    # Total visitors Japan: gender ratios
    fukui_in_visited = visitors.visited_places(fukui_in)
    fukui_in_visited_spring_df = visitors.visited_places(fukui_in[mask_spring])
    fukui_in_visited_summer_df = visitors.visited_places(fukui_in[mask_summer])
    fukui_in_visited_autumn_df = visitors.visited_places(fukui_in[mask_autumn])
    fukui_in_visited_winter_df = visitors.visited_places(fukui_in[mask_winter])
    #####################################################################################

    ### 6: add a new column 'id' into the dataframe and create ouside FUKUI dataframe
    #####################################################################################
    ### 6-1: JAPAN
    japan_visited['id'] = fukui_in_visited['市町村'].apply(lambda x: city_id_map[x])
    japan_visited_spring_df['id'] = japan_visited_spring_df['市町村'].apply(lambda x: city_id_map[x])
    japan_visited_summer_df['id'] = japan_visited_summer_df['市町村'].apply(lambda x: city_id_map[x])
    japan_visited_autumn_df['id'] = japan_visited_autumn_df['市町村'].apply(lambda x: city_id_map[x])
    japan_visited_winter_df['id'] = japan_visited_winter_df['市町村'].apply(lambda x: city_id_map[x])

    ### 6-2: FUKUI OUT
    fukui_out_visited['id'] = fukui_in_visited['市町村'].apply(lambda x: city_id_map[x])
    fukui_out_visited_spring_df['id'] = fukui_out_visited_spring_df['市町村'].apply(lambda x: city_id_map[x])
    fukui_out_visited_summer_df['id'] = fukui_out_visited_summer_df['市町村'].apply(lambda x: city_id_map[x])
    fukui_out_visited_autumn_df['id'] = fukui_out_visited_autumn_df['市町村'].apply(lambda x: city_id_map[x])
    fukui_out_visited_winter_df['id'] = fukui_out_visited_winter_df['市町村'].apply(lambda x: city_id_map[x])

    ### 6-3: FUKUI IN
    fukui_in_visited['id'] = fukui_in_visited['市町村'].apply(lambda x: city_id_map[x])
    fukui_in_visited_spring_df['id'] = fukui_in_visited_spring_df['市町村'].apply(lambda x: city_id_map[x])
    fukui_in_visited_summer_df['id'] = fukui_in_visited_summer_df['市町村'].apply(lambda x: city_id_map[x])
    fukui_in_visited_autumn_df['id'] = fukui_in_visited_autumn_df['市町村'].apply(lambda x: city_id_map[x])
    fukui_in_visited_winter_df['id'] = fukui_in_visited_winter_df['市町村'].apply(lambda x: city_id_map[x])
    #####################################################################################

    support_data = fukui_prefecture
    japan = japan_visited, japan_visited_spring_df, japan_visited_summer_df, japan_visited_autumn_df, japan_visited_winter_df
    fukui_in = fukui_in_visited, fukui_in_visited_spring_df, fukui_in_visited_summer_df, fukui_in_visited_autumn_df, fukui_in_visited_winter_df
    fukui_out = fukui_out_visited, fukui_out_visited_spring_df, fukui_out_visited_summer_df, fukui_out_visited_autumn_df, fukui_out_visited_winter_df
    return support_data, japan, fukui_in, fukui_out
if __name__ == '__main__':
    main()
