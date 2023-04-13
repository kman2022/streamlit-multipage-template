
import pandas as pd
import altair as alt
import streamlit as st
from matplotlib import pyplot as plt
import matplotlib.style as style

style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1
dpi = 1000
plt.rcParams['font.size'] = 13
plt.rcParams['font.sans-serif'] = 'Lato'
plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
plt.rcParams['axes.titlesize'] = plt.rcParams['font.size']
plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['figure.figsize'] = 8, 8

# fix the legend in the charts

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

def unique_no_nan(x):
    return x.dropna().unique()

@st.cache_data(persist=True)
def regions(df):
    region_list = list(unique_no_nan(df['region']))
    default_region = region_list.index('PJM')
    return region_list, default_region

@st.cache_data(persist=True)
def filter_data(df, yr, ft, loc):
    df = df.iloc[:,:9]
    df = df[df['q_year'] == yr]
    if ft:
        df = df[df['type_clean'].isin(ft)]
    df = df[df['region'] == loc]
    return df

def status_types(df):
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
    #############
    ############# Toggles
    row1_col1, row1_col2 = st.columns([3.0, 3.4])
    # Load regions
    region_list, default_region = regions(df_hist)

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
        
    row2_col1, row2_col2, row1_col3 = st.columns([3.0, 3.0, 3.4])

    with row2_col1:
        region_select = st.sidebar.selectbox('Region:', region_list,index=default_region,help = 'Filter report to show the market region.')

    with row2_col2:
        qyear_select = st.sidebar.slider("Enter queue year range for trends:",min_value=2001, max_value=2021,step=1, value = 2014, help = 'Filter report to show the year the project entered the queue.')

    #############
    #############
    with st.expander("See chart trend by volume"):

        row3_col1, row3_col2= st.columns([5,1])
    with row3_col1:
        df_chart_trend = df_trend[(df_trend['region']==region_select)&(df_trend['type_clean'].isin(selected_options_ft))&(df_trend['q_year']>=qyear_select)]
        df_chart_trend = df_chart_trend[['q_year','q_status','mw1']]
        
        bar_chart = alt.Chart(
                        df_chart_trend,
                        title="Trend: volume",
                    ).mark_bar(
                        cornerRadiusTopLeft=3,
                        cornerRadiusTopRight=3
                        ).encode(
                        x = alt.X('q_year:O',title="Year"),
                        y = alt.Y('sum(mw1):Q',title="Capapcity"),
                        color = 'q_status:N'
                    )

        st.altair_chart(bar_chart, theme="streamlit", use_container_width=True)

    #############
    with st.expander("See chart trend by count"):

        row4_col1, row4_col2= st.columns([5,1])
    with row4_col1:
        bar_chart = alt.Chart(
                        df_chart_trend,
                        title="Trend: count",
                    ).mark_bar(
                        cornerRadiusTopLeft=3,
                        cornerRadiusTopRight=3                                                
                        ).encode(
                        x = alt.X('q_year:O',title="Year"),
                        y = alt.Y('count(mw1):Q',title="Count"),
                        color = 'q_status:N'
                    )

        st.altair_chart(bar_chart, theme="streamlit", use_container_width=True)

    #############
    with st.expander("See chart trend by status breakout"):

        row5_col1, row4_col2= st.columns([5,1])
    with row5_col1:
        bar_chart = alt.Chart(
                        df_chart_trend,
                        title="Trend: percent capacity",
                    ).mark_bar(
                        cornerRadiusTopLeft=3,
                        cornerRadiusTopRight=3                        
                        ).encode(
                        x = alt.X('q_year:O',title="Year"),
                        y = alt.Y('count(mw1):Q',title="Count",stack='normalize'),
                        color = 'q_status:N'
                    )

        st.altair_chart(bar_chart, theme="streamlit", use_container_width=True)

    df_tr = df_trend[['q_year', 'q_status', 'mw1','region']]
    df_tr = df_tr[(df_tr['q_year']>=2000)&(df_tr['q_year']<=2015)]

    reg_status_count = df_tr.groupby(['region','q_status']).agg({'q_status':'count'},group_keys=False)
    reg_status_count_tot =df_tr.groupby(['region']).agg({'q_status':'count'},group_keys=False)
    reg_perc_count = reg_status_count.div(reg_status_count_tot,level=0) * 100

    reg_status_volume = df_trend.groupby(['region','q_status']).agg({'mw1':'sum'},group_keys=False)
    reg_status_volume_tot =df_trend.groupby(['region']).agg({'mw1':'sum'},group_keys=False)
    reg_perc_volume = reg_status_volume.div(reg_status_volume_tot,level=0) * 100

    st.header('Overview')
    st.subheader('Trends:')
    st.markdown('- PJM and MISO have the highest volume of projects completing each phase. Total volume decreases substantially across phases for most ISOs.')
    st.markdown('- Historical completion rates 2000-2015: PJM (29%), MISO (27%), ISONE (22%), CAISO (13%) and NYISO (18%). (page 30)')
    st.info('- This is misleading when viewed by volume: PJM (18%), MISO (19%), ISONE (23%), CAISO (10%) 📈')

    #############
    with st.expander("See tabular completion by region"):
        st.code('''# p30 Completion (COD) Percentage of Queued Projects for IRs from 2000-2015
            df_trend = df_trend[['q_year', 'q_status', 'mw1','region']]
            df_trend = df_trend[(df_trend['q_year']>=2000)&(df_trend['q_year']<=2015)]
            reg_status_volume = df_trend.groupby(['region','q_status']).agg({'mw1':'sum'})
            reg_perc_vol = reg_status_volume.groupby(level=0).apply(lambda x: 100 * x/ float(x.sum()))
        ''', language="python")
        row6_col1, row6_col2= st.columns([1,1])
        row6_col1.caption("Region by count")
        row6_col1.table(reg_perc_count[['q_status']].style.format('{:.1f}', na_rep="")\
             .bar(align=0, vmin=-2.5, vmax=2.5, cmap="bwr", height=50,
                  width=60, props="width: 120px; border-right: 1px solid black;")\
             .text_gradient(cmap="bwr", vmin=-2.5, vmax=2.5))
        row6_col2.caption("Region by volume")
        row6_col2.table(reg_perc_volume[['mw1']].style.format('{:.1f}', na_rep="")\
             .bar(align=0, vmin=-2.5, vmax=2.5, cmap="bwr", height=50,
                  width=60, props="width: 120px; border-right: 1px solid black;")\
             .text_gradient(cmap="bwr", vmin=-2.5, vmax=2.5))

    st.markdown('- Only 27% of all projects requesting interconnection from 2000 to 2016 achieved commercial operation by year-end 2021. (page 2 PJM Costs)')
    st.info('- While unable to tie out the number exactly it misses the trend and wide variation between markets 📈')

    df_tr1 = df_trend[['q_year', 'cod_year','q_status','mw1','region']]
    def_cod = df_tr1[(df_tr1['q_year']>=2000)&(df_tr1['q_year']<=2016)&(df_tr1['cod_year']<=2021)&(df_tr1['cod_year']>=2000)]

    def_cod_count_yr = def_cod.groupby(['cod_year','q_status']).agg({'q_status':'count'}) # 27%
    def_cod_count_tot_yr = def_cod.groupby(['cod_year']).agg({'q_status':'count'})
    def_perc_cod_count_yr = def_cod_count_yr.div(def_cod_count_tot_yr,level=0) * 100

    # How the 27% claim evolved overall
    def_perc_cod_trend = def_perc_cod_count_yr[def_perc_cod_count_yr.index.isin(['operational'], level=1)]

    # How the 27% claim evolved by region / needed to subset by mw1 b/c status in the index
    def_reg_count_yr = def_cod.groupby(['cod_year','region','q_status']).agg({'mw1':'count'})
    def_reg_count_yr = def_reg_count_yr[def_reg_count_yr.index.get_level_values(2).isin(['operational'])]
    def_reg_count_tot_yr = def_cod.groupby(['cod_year','q_status']).agg({'mw1':'count'})
    def_reg_count_tot_yr = def_reg_count_tot_yr[def_reg_count_tot_yr.index.get_level_values(1).isin(['operational'])]
    def_reg_count_yr = def_reg_count_yr.reset_index()
    def_reg_count_yr = def_reg_count_yr.set_index(['cod_year','q_status'])
    df_reg_perc_cod_tot = def_reg_count_yr.join(def_reg_count_tot_yr,lsuffix='_r', rsuffix='_t')
    df_reg_perc_cod_tot['perc'] = df_reg_perc_cod_tot.mw1_r/df_reg_perc_cod_tot.mw1_t

    #############
    with st.expander("See tabular operational trend"):
        row7_col1, row7_col2= st.columns([1,1])
        st.code("""
            def_cod = df_trend[(df_tr1['q_year']>=2000)&(df_tr1['q_year']<=2016)&(df_tr1['cod_year']<=2021)]
            def_cod_count = def_cod.groupby(['q_status']).agg({'mw1':'count'}) # 24%
            def_cod_count_tot = def_cod.agg({'mw1':'count'})
            def_perc_cod_count = def_cod_count.div(def_cod_count_tot,level='mw1') * 100
        """, language="python")
        row7_col1.caption("Trend operational count")
        row7_col1.dataframe(def_perc_cod_trend)
        row7_col2.caption("Trend regional operational volume")
        row7_col2.dataframe(df_reg_perc_cod_tot)

    #############
    with st.expander("See chart operational trend"):
        row8_col1, row8_col2= st.columns([5,1])
        chart_cod = def_perc_cod_trend.reset_index('q_status',drop=True)
        chart_cod.reset_index(inplace=True)
        overall_op_chart = alt.Chart(chart_cod).mark_line().encode(
                  x=alt.X('cod_year:O', title="COD Year"),
                  y=alt.Y('q_status:Q', title = "Percent")
                ).properties(title="Overall operational trend")
        row8_col1.altair_chart(overall_op_chart, use_container_width=True)

        row9_col1, row9_col2= st.columns([24,1])
        chart_region_cod = df_reg_perc_cod_tot
        # chart_region_cod = df_cod[df_cod['q_year']>=qyear_select]
        # chart_region_cod = df_cod[df_cod['type_clean'].isin(selected_options_ft)]
        chart_region_cod = chart_region_cod.reset_index()
        chart_region_cod.drop(labels=['q_status','mw1_r','mw1_t'],axis=1,inplace=True)
        chart = alt.Chart(chart_region_cod).mark_line().encode(
                  x=alt.X('cod_year:O', title="COD Year"),
                  y=alt.Y('perc:Q', title = "Percent"),
                  color=alt.Color('region:N',legend=alt.Legend(title='Market'))
                ).properties(title="Regional operational trend")
        row9_col1.altair_chart(chart, use_container_width=True)

    st.subheader('Duration:')
    st.markdown('- The duration from Interconnection Request (IR) to COD is increasing, averaging ~4 years since 2016.')

    chart_dur = df_dur[['q_year','mw1','diff_months_cod']]
    chart_dur = chart_dur[chart_dur['q_year']>2008]
    chart_dur_vol = chart_dur.groupby('q_year').agg({'diff_months_cod':'mean','mw1':'sum'})

        #############
    with st.expander("See chart IR to COD"):

        latest_day_data = chart_dur_vol.diff_months_cod.iloc[-1]
        st.subheader(f"2021 mean duration: {latest_day_data:.2f}")
        row10_col1, row10_col2= st.columns([5,1])
        row10_col1.line_chart(chart_dur_vol.diff_months_cod)
        volume = chart_dur_vol.mw1

        st.subheader("Selection bias: successful projects have not seen their duration significantly increase")
        row11_col1, row11_col2= st.columns([5,1])
        row11_col1.bar_chart(volume)

    # raw queue data filter_data(df, yr, ft, loc)
    st.subheader("Historical Data")
    raw_trend_data = filter_data(df_dur, qyear_select, selected_options_ft, region_select)
    if st.checkbox("Show Raw Trend Queue Data",False,help = 'Displays the raw data based on filters.'):
          st.subheader('Raw Queue Data')
          st.write(raw_trend_data)

    st.markdown('- But durations from IR to interconnection agreement (IA) have been mostly steady at 2-3 years in the last decade')
    st.markdown('- In PJM, Phase 1 takes typically 2-3 months; Phase 3 takes 20-25 months.')
    st.markdown('- Many markets including PJM are embarking on queue reform whuch has been encouraged and approved by FERC (2022). This includes a clustered, **“first-ready, first-serve”** approach, size-based study deposits, and increased readiness deposits that are at risk when projects withdraw later in the study process.')

app()


