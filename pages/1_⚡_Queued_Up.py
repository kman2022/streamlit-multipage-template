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
    df_dur = pd.read_csv(csv_duration, usecols=['q_year', 'q_status', 'cod_year', 'type_clean', 'mw1',
       'region', 'ix_voltage', 'diff_months_ia', 'diff_months_cod',
       'diff_months_wd'])
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

    row1_col1, row1_col2 = st.columns([3.0, 3.4])
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

        selected_options_ft = st.sidebar.multiselect("Select one or more options:",
                FUEL_LIST,key="selected_options", on_change=multi_change)

        all_ft = st.sidebar.checkbox("Select all", key='all_option',on_change= check_change)
    #############    
        row2_col1, row2_col2, row1_col3 = st.columns([3.0, 3.0, 3.4])

    with row2_col1:
        region_select = st.sidebar.selectbox('Region:', region_list,index=default_region,help = 'Filter report to show the market region.')

    with row2_col2:
        qyear_select = st.sidebar.slider("Enter queue year:",min_value=2001, max_value=2021,step=1, value = 2014, help = 'Filter report to show the year the project entered the queue.')
    ############# 
    with st.expander("See a trend by volume"):

        row3_col1, row3_col2= st.columns([5,1])
    with row3_col1:
        df_chart_trend = df_trend[(df_trend['region']==region_select)&(df_trend['type_clean'].isin(selected_options_ft))&(df_trend['q_year']>=qyear_select)]
        df_chart_trend = df_chart_trend[['q_year','q_status','mw1']]
        row3_col1.subheader("Trend: Total MW Volumes")
        bar_chart = alt.Chart(
                        df_chart_trend,
                    ).mark_bar().encode(
                        x = 'q_year:O',
                        y = 'sum(mw1):Q',
                        color = 'q_status:N'
                    )
        st.altair_chart(bar_chart, use_container_width=True)
    ############# 
    with st.expander("See a trend by count"):

        row4_col1, row4_col2= st.columns([5,1])
    with row4_col1:
        row4_col1.subheader("Trend: Total Count")
        bar_chart = alt.Chart(
                        df_chart_trend,
                    ).mark_bar().encode(
                        x = 'q_year:O',
                        y = 'count(mw1):Q',
                        color = 'q_status:N'
                    )
        st.altair_chart(bar_chart, use_container_width=True)
        ############# 
    with st.expander("See a trend by percent capacity"):

        row5_col1, row4_col2= st.columns([5,1])
    with row5_col1:
        row5_col1.subheader("Trend: By percent capacity")
        bar_chart = alt.Chart(
                        df_chart_trend,
                    ).mark_bar().encode(
                        x = 'q_year:O',
                        y = alt.Y('count(mw1):Q',stack='normalize'),
                        color = 'q_status:N'
                    )
        st.altair_chart(bar_chart, use_container_width=True)

app()

df_trend = df_trend[['q_year', 'q_status', 'mw1','region']]
df_trend = df_trend[(df_trend['q_year']>=2000)&(df_trend['q_year']<=2015)]
reg_status_volume = df_trend.groupby(['region','q_status']).agg({'mw1':'sum'})
reg_perc_vol = reg_status_volume.groupby(level=0).apply(lambda x: 100 * x/ float(x.sum()))

reg_status_count = df_trend.groupby(['region','q_status']).agg({'mw1':'count'})
reg_perc_count = reg_status_count.groupby(level=0).apply(lambda x: 100 * x/ float(x.sum()))
st.markdown('#### Overview:')
st.markdown('- PJM and MISO have the highest volume of projects completing each phase. Total volume decreases substantially across phases for most ISOs.')
st.markdown('- Historical completion rates 2000-2015: PJM (29%), MISO (27%), ISONE (22%), CAISO (13%) and NYISO (18%). (page 30)')
st.info('- This is misleading when viewed by volume: PJM (18%), MISO (19%), ISONE (23%), CAISO (10%) 📈')

with st.expander("See a completion by region"):
    st.code("""
    reg_status_volume = df_trend.groupby(['region','q_status']).agg({'mw1':'sum'})
    reg_perc = reg_status_volume.groupby(level=0).apply(lambda x: 100 * x/ float(x.sum()))
    """, language="python")
    row6_col1, row6_col2= st.columns([3,3])
    row6_col1.subheader("Region by count")
    row6_col1.dataframe(reg_perc_count)
    row6_col2.subheader("Region by volume")
    row6_col2.dataframe(reg_perc_vol)

st.markdown('- In PJM, Phase 1 takes typically 2-3 months; Phase 3 takes 20-25 months.')
st.markdown('- Only 27% of all projects requesting interconnection from 2000 to 2016 achieved commercial operation by year-end 2021.  📈')

with st.expander("See a completion trend"):
    st.code("""
    def_dur_cod = df_dur[(df_dur['q_year']>=2000)&(df_dur['q_year']<=2016)&(df_dur['cod_year']<=2021)]
    def_dur_count = def_dur_cod.groupby(['q_status']).agg({'mw1':'count'}) # 27%
    """, language="python")
    row7_col1, row7_col2= st.columns([3,3])
    row6_col1.subheader("Region by count")
    row6_col1.dataframe(reg_perc_count)
    row6_col2.subheader("Region by volume")
    row6_col2.dataframe(reg_perc_vol)

st.markdown('- PJM embarked on a queue reform that was recently approved by FERC (2022) which includes a clustered, **“first-ready, first-serve”** approach, size-based study deposits, and increased readiness deposits that are at risk when projects withdraw later in the study process.')