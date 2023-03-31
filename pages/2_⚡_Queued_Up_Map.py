
# import pandas as pd
# import altair as alt
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw

st.set_page_config(page_title="Queued Up Map ⚡",
                   page_icon='📈',
                   layout="wide")

st.title("Queued Up Map ⚡ ")

mkdwn_analysis = """
    **Source:** [Berkley Lab Queued Up v2](https://emp.lbl.gov/queues): Extended Analysis on Power Plants Seeking Transmission InterconnectionAs of the End of 2021. Joseph Rand, Will Gorman, Dev Millstein, Andrew Mills, Joachim Seel, Ryan Wiser Lawrence Berkeley National Laboratory. February 2022.
"""

st.sidebar.info(mkdwn_analysis)

# to do
# need to remap projects as CA is not avail
# rerun figures for map 1 file per market in order to speed up the map
# use file in doc/streamlit/data file as manual adjustments were made to several hundred plants
# add height or increased weight on borders for volume
# https://folium.streamlit.app/


link_prefix = "https://raw.githubusercontent.com/kman2022/data/main/main/"
csv_q_hist = link_prefix + "berkley/df_iq_clean.csv"
gj_iq_geo = link_prefix + "berkley/gdp_iq_qeo.geojson"
sh_iso_geo = link_prefix + "berkley/geojson_iso.json"

REGION_LIST = ['CAISO', 'ISO-NE', 'MISO', 'PJM', 'NYISO', 'SPP', 'ERCOT',
       'Southeast (non-ISO)', 'West (non-ISO)']

REGION_MAP = {'CALIFORNIA INDEPENDENT SYSTEM OPERATOR':'CAISO',
              'ISO NEW ENGLAND INC.':'ISO-NE',
              'MIDCONTINENT INDEPENDENT TRANSMISSION SYSTEM OPERATOR, INC..':'MISO',
              'NEW YORK INDEPENDENT SYSTEM OPERATOR':'NYISO',
              'PJM INTERCONNECTION, LLC':'PJM',
              'SOUTHWEST POWER POOL':'SPP',
              'ELECTRIC RELIABILITY COUNCIL OF TEXAS, INC.':'ERCOT'}

MAP_ZOOM = 6

@st.cache_data(persist=True)
def load_qmap_data():
    # geoloc hist
    gdf_hist = gpd.read_file(gj_iq_geo)
    # geoloc shape
    gdf_iso = gpd.read_file(sh_iso_geo)
    gdf_iso['region'] = gdf_iso['NAME'].map(REGION_MAP)
    return gdf_hist, gdf_iso

def unique_no_nan(x):
    return x.dropna().unique()

def filter_regions(df):
    region_list = list(unique_no_nan(df['region']))
    default_region = region_list.index('PJM')
    region_select = st.selectbox('Region:',
                                 region_list,index=default_region,
                                 help = 'Filter report to show the market region')
    return region_select, default_region

def filter_status(df):
    status_list = list(unique_no_nan(df['q_status']))
    default_st = status_list.index('active')
    status_type = st.selectbox('Status:',
                               status_list,index=default_st,
                               help = 'Filter report to show the status type of the project')
    return status_type

def filter_year(df):
    year_list = df['q_year'].sort_values(ascending=False,na_position='last')
    year_list = list(unique_no_nan(year_list))
    default_yr = year_list.index(2020)
    select_yr = st.selectbox('Year entered queue:',
                             year_list,index=default_yr,
                             help = 'Filter report to show the year in which the project entered the queue.')
    return select_yr

def filter_fuel(df):
    fuel_list = list(unique_no_nan(df['type_clean']))
    default_ft = fuel_list.index('Solar')
    select_fuel = st.selectbox('Fuel:',
                               fuel_list,index=default_ft,
                               help = 'Filter report to show the status type of the project')
    return select_fuel

###########
# Load data
###########
gdf_hist, gdf_iso = load_qmap_data()

def main():

    ################################
    st.markdown('#### Map:')
    st.markdown('- Roughly 18% of the records did not have a geoloc including 15% operational status listed projects.')

    ############# Toggles
    row1_col1, row1_col2, row1_col3 = st.columns([3.0, 3.0, 3.4])
    ###############
    # Load year
    ###############
    with row1_col1:
        select_year = filter_year(gdf_hist)

    ###############
    # Load status
    ###############
    with row1_col2:
        status_type = filter_status(gdf_hist)

    ###############
    # Load regions
    ###############
    with row1_col3:
        select_region, default_region = filter_regions(gdf_hist)

    row2_col1, row2_col2, row2_col3 = st.columns([3.0,3.0,3.4])
    ###############
    # Load fuel type
    ###############
    with row2_col1:
        select_fuel = filter_fuel(gdf_hist)

    row3_col1, row3_col2 = st.columns([3, 3.4])

    row4_col1, row4_col2 = st.columns([19, 1])

    with row4_col1:
        # filter_data(df, yr, ft, loc)
        gdf = gdf_hist
        gdf_iso_sel = gdf_iso
        gdf = gdf[gdf['q_year'] == select_year]
        gdf = gdf[gdf['type_clean']==select_fuel]
        gdf = gdf[gdf['region']==select_region]
        gdf_iso_sel = gdf_iso[gdf_iso['region']==select_region]
        gdf = gdf[gdf['q_status'] == status_type]
        gdf_short = gdf[['NAME','diff_months_cod','geometry']]

        gdf_agg = gdf_short.dissolve(by='NAME', aggfunc = {'diff_months_cod':'mean'},as_index=False) #{'diff_months':['min','max','mean','median']}
        gdf_geo = gdf_agg[gdf_agg['diff_months_cod']>0]
        gdf_geo = gdf_geo[['NAME','diff_months_cod','geometry']]

        map_lat = gdf_iso_sel.centroid.y
        map_lon = gdf_iso_sel.centroid.x
        max_dur = gdf_geo['diff_months_cod'].max()
        mean_75 = gdf_geo['diff_months_cod'].quantile(0.75)
        mean_dur = gdf_geo['diff_months_cod'].mean()
        mean_25 = gdf_geo['diff_months_cod'].quantile(0.25)
        min_dur = gdf_geo['diff_months_cod'].min()

        map = folium.Map(location=[map_lat,map_lon], zoom_start=MAP_ZOOM, control_scale=True)
        Draw(export=True).add_to(map)
        folium.GeoJson(data=gdf_iso_sel,name=('Market areas'),
                        tooltip=folium.GeoJsonTooltip(fields=['region','PEAK_LOAD','AVG_LOAD','YEAR']),
                        style_function= lambda feature: {'fillOpacity':0.3, 'weight':.2}).add_to(map)

        cp = folium.Choropleth(
            geo_data=gdf_geo,
            name="Counties",
            data=gdf_geo,
            columns=["NAME","diff_months_cod"],
            key_on="feature.id",
            fill=True,
            fill_color="YlOrRd",
            fill_opacity=0.6,
            line_opacity=0.5,
            highlight=True,
            edgecolor='k',
            bins=[min_dur,mean_25,mean_dur,mean_75,max_dur],
            legend_name="Duration in months"
        )
        cp.add_to(map)
        feature = folium.features.GeoJson(gdf_agg,
          name='NAME',
          tooltip=folium.GeoJsonTooltip(fields= ["NAME","diff_months_cod"],aliases=["County name: ","COD duration: "],labels=True, localize=True))
        cp.add_child(feature)

        folium.LayerControl().add_to(map)
        row4_col1 = st_folium(map, width=750)
    # cp.add_child(
    #     folium.features.GeoJsonTooltip(["GEOID", "duration"], labels=True)
    # )

    
    # row2_col1, row2_col2 = st.columns([19, 1.0])
    # row2_col1.st_map = st_folium(map, width=700, height=450)

main()


