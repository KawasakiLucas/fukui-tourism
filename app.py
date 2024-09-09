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
import visitors_analysis
import visited_city_analysis



####################################################################################################
####################################################################################################

### Load data
#####################################################################################
#support_data:
# 0: japan_prefectures / 1: fukui_prefecture

# japan, fukui_in, fukui_out
# 0: All year data / 1: Spring data / 2: Summer data / 3: Autumn data / 4: Winter data
support_data, japan, fukui_in, fukui_out = visitors_analysis.main()

#support_data2:
# 0: fukui_prefecture

# japan2, fukui_in2, fukui_out2
# 0: All year data / 1: Spring data / 2: Summer data / 3: Autumn data / 4: Winter data
support_data2, japan2, fukui_in2, fukui_out2 = visited_city_analysis.main()
#####################################################################################
#####################################################################################
#support_data:
# 0: japan_prefectures / 1: fukui_prefecture

# japan, fukui_in, fukui_out
# 0: All year data / 1: Spring data / 2: Summer data / 3: Autumn data / 4: Winter data
visitors_fukui = visitors_analysis.main()

#support_data2:
# 0: fukui_prefecture

# japan2, fukui_in2, fukui_out2
# 0: All year data / 1: Spring data / 2: Summer data / 3: Autumn data / 4: Winter data
visited_fukui = visited_city_analysis.main()
#####################################################################################





### Streamlit
### 0: Page setup
#####################################################################################
st.set_page_config(layout="wide")

# # Background color
# page_bg_img= """<style> [data-testid=stAppViewContainer] {background-color:#FFFFFF;
#                 opacity:0.8; margin-top: -130px} </style> """
# st.markdown(page_bg_img, unsafe_allow_html=True)
#####################################################################################

def container_maker_visitors(jp, fi, fo, jp_geojson, f_geojson):
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(visitors_map.fukui_map_visitors(
                            fi, f_geojson, title='県内居住地'),
                            theme="streamlit",
                            use_container_width=True)
        with col2:
            st.plotly_chart(visitors_map.japan_map_visitors(
                            fo, jp_geojson, title='県外居住地'),
                            theme="streamlit",
                            use_container_width=True)
        with col3:
            st.plotly_chart(visitors_map.japan_map_visitors(
                            jp, jp_geojson, title='全体'),
                            theme="streamlit",
                            use_container_width=True)
    pass

def container_maker_visited(jp, fi, fo, f_geojson):
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(visitors_map.fukui_map_visited(
                            fi, f_geojson, title='県内居住地'),
                            theme="streamlit",
                            use_container_width=True)

        with col2:
            st.plotly_chart(visitors_map.fukui_map_visited(
                            fo, f_geojson, title='県外居住地'),
                            theme="streamlit",
                            use_container_width=True)
        with col3:
            st.plotly_chart(visitors_map.fukui_map_visited(
                            jp, f_geojson, title='全体'),
                            theme="streamlit",
                            use_container_width=True)
    pass

### 1: Create tabs
#####################################################################################
tab1, tab2, tab3, tab4, tab5 = st.tabs(["通年", "春", "夏", "秋", "冬"])

with tab1:
    st.markdown("<h2 style='text-align: center; color: white;'>回答者の居住地</h2>", unsafe_allow_html=True)
    container_maker_visitors(japan[0], fukui_in[0], fukui_out[0], support_data[0], support_data[1])
    st.markdown("<h2 style='text-align: center; color: white;'>最も訪問した都市</h2>", unsafe_allow_html=True)
    container_maker_visited(japan2[0], fukui_in2[0], fukui_out2[0], support_data2)

# Spring Visitors
with tab2:
    st.markdown("<h2 style='text-align: center; color: white;'>回答者の居住地</h2>", unsafe_allow_html=True)
    container_maker_visitors(japan[1], fukui_in[1], fukui_out[1], support_data[0], support_data[1])
    st.markdown("<h2 style='text-align: center; color: white;'>最も訪問した都市</h2>", unsafe_allow_html=True)
    container_maker_visited(japan2[1], fukui_in2[1], fukui_out2[1], support_data2)

# Summer Visitors
with tab3:
    st.markdown("<h2 style='text-align: center; color: white;'>回答者の居住地</h2>", unsafe_allow_html=True)
    container_maker_visitors(japan[2], fukui_in[2], fukui_out[2], support_data[0], support_data[1])
    st.markdown("<h2 style='text-align: center; color: white;'>最も訪問した都市</h2>", unsafe_allow_html=True)
    container_maker_visited(japan2[2], fukui_in2[2], fukui_out2[2], support_data2)

# Autumn Visitors
with tab4:
    st.markdown("<h2 style='text-align: center; color: white;'>回答者の居住地</h2>", unsafe_allow_html=True)
    container_maker_visitors(japan[3], fukui_in[3], fukui_out[3], support_data[0], support_data[1])
    st.markdown("<h2 style='text-align: center; color: white;'>最も訪問した都市</h2>", unsafe_allow_html=True)
    container_maker_visited(japan2[3], fukui_in2[3], fukui_out2[3], support_data2)

# Winter Visitors
with tab5:
    st.markdown("<h2 style='text-align: center; color: white;'>回答者の居住地</h2>", unsafe_allow_html=True)
    container_maker_visitors(japan[4], fukui_in[4], fukui_out[4], support_data[0], support_data[1])
    st.markdown("<h2 style='text-align: center; color: white;'>最も訪問した都市</h2>", unsafe_allow_html=True)
    container_maker_visited(japan2[4], fukui_in2[4], fukui_out2[4], support_data2)

### 1: Create maps on streamlit
#####################################################################################
#visitors_map.fukui_map_visitors(total_visitors_fukui_df)

#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
