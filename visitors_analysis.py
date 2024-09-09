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
    ### 0-1: Read JAPAN GeoJson file
    json_file = './japan.geojson'
    japan_prefectures = json.load(open(json_file, 'r'))

    ### 0-2: Read FUKUI GeoJson file
    json_file = './fukui.geojson'
    fukui_prefecture = json.load(open(json_file, 'r'))
    #####################################################################################

    ### 1: Load a prefecture id map dictionary
    #####################################################################################
    ### 1-1: From the JAPAN geojson data
    # Create an empty dictionary to store prefecture IDs
    prefecture_id_map = {}

    # Loop through the "features" list in the "japan_prefectures" dictionary
    for feature in japan_prefectures['features']:
        feature['id'] = feature['properties']['id']
        prefecture_id_map[feature['properties']['nam_ja']] = feature['id']

    ### 1-2: From the FUKUI geojson data
    # Create an empty dictionary to store prefecture IDs
    city_id_map = {}

    # Loop through the "features" list in the "fukui_prefecture" dictionary
    for feature in fukui_prefecture['features']:
        feature['id'] = feature['properties']['id']
        city_id_map[feature['properties']['会員市町村']] = feature['id']
    #####################################################################################

    ### 2: Load datasets
    #####################################################################################
    ### 2-1: Load Fukui tourism dataset
    data = pd.read_csv('all.csv')

    ### 2-2: Load Japan geo data from a csv file
    geo_csv = './japan_geo.csv'
    geo_df = pd.read_csv(geo_csv)

    ### 2-3: Filter columns (latitude, longitude) from the pandas dataframe.
    pref_df = geo_df[['region_en', 'region_jp','prefecture_en', 'prefecture_jp']]
    # rename prefecture_jp to 都道府県
    pref_df.rename(columns={"prefecture_jp": "都道府県"}, inplace=True)
    #####################################################################################

    ### 3: Preprocessing
    #####################################################################################
    ### 3-1: Filter columns from Fukui tourism dataset and make some changes
    data_personal = data[['性別', '年代', '回答月', '都道府県', '会員市町村', '世帯年収']]

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
    #####################################################################################


    ### 4: Call visitors package
    #####################################################################################
    ### 4-1: JAPAN
    # Total visitors Japan: gender ratios
    total_visitors_pref_df = visitors.japan_visitors(data_personal_ohe)

    # Create mask to filter data on seasons
    mask_spring = (data_personal_ohe['回答月'] == '3月') | (data_personal_ohe['回答月'] == '4月') | (data_personal_ohe['回答月'] == '5月')
    mask_summer = (data_personal_ohe['回答月'] == '6月') | (data_personal_ohe['回答月'] == '7月') | (data_personal_ohe['回答月'] == '8月')
    mask_autumn = (data_personal_ohe['回答月'] == '9月') | (data_personal_ohe['回答月'] == '10月') | (data_personal_ohe['回答月'] == '11月')
    mask_winter = (data_personal_ohe['回答月'] == '12月') | (data_personal_ohe['回答月'] == '1月') | (data_personal_ohe['回答月'] == '2月')

    # Total visitors Japan per season: gender ratios
    spring_df = visitors.japan_visitors(data_personal_ohe[mask_spring])
    summer_df = visitors.japan_visitors(data_personal_ohe[mask_summer])
    autumn_df = visitors.japan_visitors(data_personal_ohe[mask_autumn])
    winter_df = visitors.japan_visitors(data_personal_ohe[mask_winter])

    ### 4-2: FUKUI
    # Total visitors Fukui: gender ratios
    mask_fukui = data_personal_ohe['都道府県'] == '福井県'
    data_personal_ohe_fukui = data_personal_ohe[mask_fukui]
    total_visitors_fukui_df = visitors.fukui_visitors(data_personal_ohe_fukui)

    # Create mask to filter data on seasons
    mask_spring = (data_personal_ohe_fukui['回答月'] == '3月') | (data_personal_ohe_fukui['回答月'] == '4月') | (data_personal_ohe_fukui['回答月'] == '5月')
    mask_summer = (data_personal_ohe_fukui['回答月'] == '6月') | (data_personal_ohe_fukui['回答月'] == '7月') | (data_personal_ohe_fukui['回答月'] == '8月')
    mask_autumn = (data_personal_ohe_fukui['回答月'] == '9月') | (data_personal_ohe_fukui['回答月'] == '10月') | (data_personal_ohe_fukui['回答月'] == '11月')
    mask_winter = (data_personal_ohe_fukui['回答月'] == '12月') | (data_personal_ohe_fukui['回答月'] == '1月') | (data_personal_ohe_fukui['回答月'] == '2月')

    # Total visitors Japan per season: gender ratios
    spring_fukui_df = visitors.fukui_visitors(data_personal_ohe_fukui[mask_spring])
    summer_fukui_df = visitors.fukui_visitors(data_personal_ohe_fukui[mask_summer])
    autumn_fukui_df = visitors.fukui_visitors(data_personal_ohe_fukui[mask_autumn])
    winter_fukui_df = visitors.fukui_visitors(data_personal_ohe_fukui[mask_winter])
    #####################################################################################

    ### 5: Merge datasets
    #####################################################################################
    ### 5-1: JAPAN
    # Merge dataframes for further analysis
    japan_visitors_df = pd.merge(pref_df, total_visitors_pref_df, on='都道府県', how='left')

    japan_visitors_spring_df = pd.merge(pref_df, spring_df, on='都道府県', how='left')
    japan_visitors_summer_df = pd.merge(pref_df, summer_df, on='都道府県', how='left')
    japan_visitors_autumn_df = pd.merge(pref_df, autumn_df, on='都道府県', how='left')
    japan_visitors_winter_df = pd.merge(pref_df, winter_df, on='都道府県', how='left')
    #####################################################################################

    ### 6: add a new column 'id' into the dataframe and create ouside FUKUI dataframe
    #####################################################################################
    ### 6-1: JAPAN
    japan_visitors_df['id'] = japan_visitors_df['都道府県'].apply(lambda x: prefecture_id_map[x])
    japan_visitors_spring_df['id'] = japan_visitors_spring_df['都道府県'].apply(lambda x: prefecture_id_map[x])
    japan_visitors_summer_df['id'] = japan_visitors_summer_df['都道府県'].apply(lambda x: prefecture_id_map[x])
    japan_visitors_autumn_df['id'] = japan_visitors_autumn_df['都道府県'].apply(lambda x: prefecture_id_map[x])
    japan_visitors_winter_df['id'] = japan_visitors_winter_df['都道府県'].apply(lambda x: prefecture_id_map[x])

    ### 6-2: FUKUI
    total_visitors_fukui_df['id'] = total_visitors_fukui_df['会員市町村'].apply(lambda x: city_id_map[x])
    spring_fukui_df['id'] = spring_fukui_df['会員市町村'].apply(lambda x: city_id_map[x])
    summer_fukui_df['id'] = summer_fukui_df['会員市町村'].apply(lambda x: city_id_map[x])
    autumn_fukui_df['id'] = autumn_fukui_df['会員市町村'].apply(lambda x: city_id_map[x])
    winter_fukui_df['id'] = winter_fukui_df['会員市町村'].apply(lambda x: city_id_map[x])


    ### 6-3: Filter the FUKUI prefecture from JAPAN dataframes
    japan_visitors_out_df = japan_visitors_df[japan_visitors_df['都道府県'] != '福井県']
    japan_visitors_spring_out_df = japan_visitors_spring_df[japan_visitors_spring_df['都道府県'] != '福井県']
    japan_visitors_summer_out_df = japan_visitors_summer_df[japan_visitors_summer_df['都道府県'] != '福井県']
    japan_visitors_autumn_out_df = japan_visitors_autumn_df[japan_visitors_autumn_df['都道府県'] != '福井県']
    japan_visitors_winter_out_df = japan_visitors_winter_df[japan_visitors_winter_df['都道府県'] != '福井県']
    #####################################################################################

    support_data = japan_prefectures, fukui_prefecture
    japan = japan_visitors_df, japan_visitors_spring_df, japan_visitors_summer_df, japan_visitors_autumn_df, japan_visitors_winter_df
    fukui_in = total_visitors_fukui_df, spring_fukui_df, summer_fukui_df, autumn_fukui_df, winter_fukui_df
    fukui_out = japan_visitors_out_df, japan_visitors_spring_out_df, japan_visitors_summer_out_df, japan_visitors_autumn_out_df, japan_visitors_winter_out_df
    return support_data, japan, fukui_in, fukui_out
if __name__ == '__main__':
    main()
