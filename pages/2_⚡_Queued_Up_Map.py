
import pandas as pd
import altair as alt
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Queued Up Map ⚡",
                   page_icon='📈',
                   layout="wide")

st.title("Queued Up Map ⚡ ")

mkdwn_analysis = """
    **Source:** [Berkley Lab Queued Up v2](https://emp.lbl.gov/queues): Extended Analysis on Power Plants Seeking Transmission InterconnectionAs of the End of 2021. Joseph Rand, Will Gorman, Dev Millstein, Andrew Mills, Joachim Seel, Ryan Wiser Lawrence Berkeley National Laboratory. February 2022.
"""

st.sidebar.info(mkdwn_analysis)

link_prefix = "https://raw.githubusercontent.com/kman2022/data/main/main/"
csv_q_hist = link_prefix + "berkley/df_iq_clean.csv"
gj_iq_geo = link_prefix + "berkley/gdp_iq_qeo.geojson"
sh_iso_geo = link_prefix + "berkley/geojson_iso.json"

REGION_LIST = ['CAISO', 'ISO-NE', 'MISO', 'PJM', 'NYISO', 'SPP', 'ERCOT',
       'Southeast (non-ISO)', 'West (non-ISO)']

MAP_LAT = 39.49
MAP_LON = -75.35
MAP_ZOOM = 6

@st.cache_data(persist=True)
def load_qmap_data():
    # geoloc hist
    gdf_hist = gpd.read_file(gj_iq_geo)
    # geoloc shape
    gdf_iso = gpd.read_file(sh_iso_geo)
    return gdf_hist, gdf_iso

def unique_no_nan(x):
    return x.dropna().unique()

def filter_regions(df):
    region_list = list(unique_no_nan(df['region']))
    default_region = region_list.index('PJM')
    region_select = st.selectbox('Region:', region_list,index=default_region,help = 'Filter report to show the merket region')
    return region_select, default_region

def filter_status(df):
    status_list = list(unique_no_nan(df['q_status']))
    default_st = status_list.index('active')
    status_type = st.selectbox('Status:', status_list,index=default_st,help = 'Filter report to show the status type of the project')
    return status_type

def filter_year(df):
    year_list = df['q_year'].sort_values(ascending=False,na_position='last')
    year_list = list(unique_no_nan(year_list))
    default_yr = year_list.index(2020)
    select_yr = st.selectbox('Year entered queue:', year_list,index=default_yr,help = 'Filter report to show the year in which the project entered the queue.')
    return select_yr

def filter_fuel(df):
    # on the first run add variables to track in state
    FUEL_LIST = list(unique_no_nan(df['type_clean'].sort_values(ascending=False,na_position='last')))
    
    if "all_option" not in st.session_state:
        st.session_state.all_option = True
        st.session_state.selected_options = FUEL_LIST

    def check_change():
    # this runs BEFORE the rest of the script when a change is detected
    # from your checkbox to set selectbox
        if st.session_state.all_option:
            st.session_state.selected_options = FUEL_LIST
        else:
            st.session_state.selected_options = []
        return

    def multi_change():
    # this runs BEFORE the rest of the script when a change is detected
    # from your selectbox to set checkbox
        if len(st.session_state.selected_options) == 3:
            st.session_state.all_option = True
        else:
            st.session_state.all_option = False
        return

    select_fuel = st.multiselect("Select one or more fuels:",
            FUEL_LIST,key="selected_options", on_change=multi_change)

    all_fuels = st.checkbox("Select all", key='all_option',on_change= check_change)
    return select_fuel, all_fuels

###########
# Load data
###########
gdf_hist, gdf_iso = load_qmap_data()

def main():
    
    ################################
    st.markdown('#### Map:')
    st.markdown('- roughly 18% of the records did not have a geoloc including 15% operational status listed projects.')
    
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
        
    row2_col1, row2_col2 = st.columns([19, 1])    
    ###############
    # Load fuel type
    ###############    
    with row2_col1: 
        select_fuel = filter_fuel(gdf_hist)
    
    row3_col1, row3_col2 = st.columns([3, 3.4])
    
    # row4_col1, row4_col2 = st.columns([19, 1])
    
    # with row4_col1:
    #     # filter_data(df, yr, ft, loc)
    #     gdf = gdf_hist
    #     gdf = gdf[gdf['q_year'] == select_year]
    #     gdf = gdf[gdf['type_clean'].isin(select_fuel)]
    #     gdf = gdf[gdf['region'].isin(region_list)]
    #     gdf = gdf[gdf['q_status'] == status_type]
    #     gdf_short = gdf[['NAME','diff_months_cod','geometry']]
        # df = pd.DataFrame(gdf_short)
        # gdf_agg = gdf_short.dissolve(by='NAME', aggfunc = {'diff_months_cod':'mean'},as_index=False) #{'diff_months':['min','max','mean','median']}
        # gdf_geo = gdf_agg[gdf_agg['diff_months_cod']>0]

        # row4_col1.dataframe(df)

    # map = folium.Map(location=[MAP_LAT,MAP_LON], zoom_start=MAP_ZOOM)

    # # folium.GeoJson(data=gdf_iso["geometry"],name=('Market areas')).add_to(map)

    # cp = folium.Choropleth(
    #     geo_data=gdf_geo.to_json(),
    #     name="choropleth",
    #     data=gdf_geo,
    #     columns=["NAME","diff_months_cod"],
    #     key_on="feature.id",
    #     fill=True,
    #     fill_color="YlGn",
    #     fill_opacity=0.6,
    #     line_opacity=0.8,
    #     highlight=True,
    #     edgecolor='k',
    #     bins=[3, 9, 18, 36, 72,100,200],
    #     legend_name="Duration in months"
    # )
    # cp.add_to(map)

    # feature = folium.features.GeoJson(gdf_agg,
    #   name='NAME',
    #   tooltip=folium.GeoJsonTooltip(fields= ["NAME","diff_months_cod"],aliases=["County name: ","COD duration: "],labels=True, localize=True))
    # cp.add_child(feature)
    # cp.add_child(
    #     folium.features.GeoJsonTooltip(["GEOID", "duration"], labels=True)
    # )

    # folium.LayerControl().add_to(map)
    # row2_col1, row2_col2 = st.columns([19, 1.0])
    # row2_col1.st_map = st_folium(map, width=700, height=450)

main()


