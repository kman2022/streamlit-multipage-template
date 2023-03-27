import datetime
import os
import pathlib
import zipfile
import pandas as pd
import pydeck as pdk
import altair as alt
import geopandas as gpd
import streamlit as st
import leafmap.colormaps as cm
from leafmap.common import hex_to_rgb

st.set_page_config(page_title="Queued Up  ⚡",
                   page_icon='📈',
                   layout="wide")
st.title("Queued Up  ⚡ ")

mkdwn_analysis = """
    **Source:** [Berkley Lab Queued Up v2](https://emp.lbl.gov/queues): Extended Analysis on Power Plants Seeking Transmission InterconnectionAs of the End of 2021. Joseph Rand, Will Gorman, Dev Millstein, Andrew Mills, Joachim Seel, Ryan Wiser Lawrence Berkeley National Laboratory. February 2022.  
"""

st.sidebar.info(mkdwn_analysis)

link_prefix = "https://raw.githubusercontent.com/kman2022/data/main/main/"
csv_trend = link_prefix + "berkley/df_trend.csv"
csv_duration = link_prefix + "berkley/df_trend_dur.csv"
csv_q_hist = link_prefix + "berkley/df_iq_clean.csv"
FUEL_LIST = ['Gas', 'Wind', 'Hydro', 'Solar', 'Other', 'Geothermal',
       'Other Storage', 'Nuclear', 'Wind+Battery', 'Solar+Battery',
       'Gas+Battery', 'Solar+Wind', 'Gas+Solar', 'Solar+Gas', 'Battery',
       'Battery+Gas', 'Coal', 'Offshore Wind', 'Wind+Storage',
       'Wind+Gas', 'CSP']
REGION_LIST = ['CAISO', 'ISO-NE', 'MISO', 'PJM', 'NYISO', 'SPP', 'ERCOT',
       'Southeast (non-ISO)', 'West (non-ISO)']

@st.cache_data(persist=True)
def load_q_data():
    # trend
    df_trend = pd.read_csv(csv_trend, usecols=['q_year', 'q_status', 'cod_year', 'type_clean', 'mw1','region'])    
    # duration
    df_dur = pd.read_csv(csv_duration)
    # history
    df_hist = pd.read_csv(csv_duration)
    return df_trend, df_dur, df_hist

# Load data
df_trend, df_dur, df_hist = load_q_data()

def regions(df):
    region_list = list(df['region'].unique())
    default_region = region_list.index('PJM')
    return region_list, default_region

def app():
    st.title("U.S. Interconnection Data and Market Trends")
    st.markdown(
        """**Introduction:** This interactive dashboard is designed for visualizing U.S. electrical interconnection data and trends at multiple levels (i.e., national,
         state, county, and ISO). The data sources is from [Berkley Labs](https://emp.lbl.gov/queues) and 
         [Cartographic Boundary Files](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html) from U.S. Census Bureau.
         Several open-source packages are used to process the data and generate the visualizations, e.g., [streamlit](https://streamlit.io),
          [geopandas](https://geopandas.org), [leafmap](https://leafmap.org), and [pydeck](https://deckgl.readthedocs.io).
    """
    )

    row1_col1, row1_col2, row1_col3 = st.columns(
    [3.0, 3.0, 3.4]
    )
    # Load regions
    region_list, default_region = regions(df_hist)

    #fuels_list, default_ft = fuel_types(df_dur)
    with row1_col1:
        # on the first run add variables to track in state
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

        selected_options_ft = st.multiselect("Select one or more options:",
                FUEL_LIST,key="selected_options", on_change=multi_change)

        all_ft = st.checkbox("Select all", key='all_option',on_change= check_change)
    
    with row1_col2:
        region_select = st.selectbox('Region:', region_list,index=default_region,help = 'Filter report to show the market region')

    with row1_col3:
        qyear_select = st.selectbox("Online Year:",range(2001,2026),1,help = 'Filter report to show the year the project entered the queue')

    row2_col1, row2_col2= st.columns([5,1])
    #with st.expander("See a summary"):
    with row2_col1:
        df_chart_trend = df_trend[(df_trend['region']==region_select)&(df_trend['type_clean'].isin(selected_options_ft))&(df_trend['q_year']>=qyear_select)]
        df_chart_trend = df_chart_trend[['q_year','q_status','mw1']]
        row2_col1.subheader("Trend")
        bar_chart = alt.Chart(
                        df_chart_trend,
                    ).mark_bar().encode(
                        x = 'q_year:O',
                        y = 'sum(mw1):Q',
                        color = 'q_status:N'
                    )
        st.altair_chart(bar_chart, use_container_width=True)

    # LOAD DATA
    # df_trend, df_dur, df_hist = load_q_data()
    # df_hist = fuel_types() 
    # LOAD MAP AND FILTERS
    # fuel_type = fuel_types(df_dur)
    #region = region_select(df_dur)
    #status_type = status_types(df_dur)

    with row1_col4:
        selected_col = st.selectbox("Attribute")
    with row1_col5:
        show_desc = st.checkbox("Show attribute description")
        if show_desc:
            try:
                label, desc = get_data_dict(selected_col.strip())
                markdown = f"""
                **{label}**: {desc}
                """
                st.markdown(markdown)
            except:
                st.warning("No description available for selected attribute")
    row2_col1, row2_col2, row2_col3, row2_col4, row2_col5, row2_col6 = st.columns(
        [0.6, 0.68, 0.7, 0.7, 1.5, 0.8]
    )

app()