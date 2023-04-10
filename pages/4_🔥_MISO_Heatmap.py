
import pandas as pd
import geopandas as gpd
import streamlit as st
import leafmap.foliumap as leafmap
from folium import plugins
import matplotlib.pyplot as plt
import matplotlib.style as style

st.set_page_config(page_title="MISO Costs ⚡",
                   page_icon='https://i.imgur.com/UbOXYAU.png',
                   layout="wide")

PROCESS_IMAGE = 'https://github.com/kman2022/data/blob/main/main/berkley/IQ_study_process_small%20copy.png?raw=true'
TRANSMISSION_IMAGE = 'https://github.com/kman2022/data/blob/main/main/berkley/transmission.png?raw=true'
miso_im = 'https://www.misoenergy.org/client/dist/img/logo.png'
MAP_GEO = "https://github.com/kman2022/data/blob/main/main/berkley/gdp_cost_miso_qeo.geojson?raw=true"
ISO_FILE = 'https://github.com/kman2022/data/blob/main/main/berkley/miso.geojson?raw=true'
# TRANS_FILE = 'https://github.com/kman2022/data/blob/main/main/berkley/pjm_transmission_short.geojson?raw=true'

style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1
dpi = 1000
plt.rcParams['font.size'] = 13
plt.rcParams['font.family'] = 'Lato'
plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
plt.rcParams['axes.titlesize'] = plt.rcParams['font.size']
plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['figure.figsize'] = 8, 8

mkdwn_analysis = """
    **Source:** [Generator Interconnection Costs to the Transmission System:](https://emp.lbl.gov/interconnection_costs) Seel, Joachim, Joseph Rand, Will Gorman, Dev Millstein, Ryan H Wiser, Will Cotton, Nicholas DiSanti, and Kevin Porter. "Generator Interconnection Cost Analysis in the Midcontinent Independent System Operator (MISO) territory." Oct-2022 (data thru 2021).
"""

st.sidebar.image(miso_im, width=200)
st.sidebar.image(TRANSMISSION_IMAGE, width=200)
st.sidebar.image(PROCESS_IMAGE, width=300,
                 caption="fig. Interconnection Study Process")
st.sidebar.info(mkdwn_analysis)
st.title("MISO Generator Interconnection Costs")

###########
# Load data
###########

@st.cache_data(persist=True)
def load_cost_map_data():
    # geodf
    gdf = gpd.read_file(MAP_GEO)
    # geoloc shape
    gdf_iso = gpd.read_file(ISO_FILE)
    return gdf, gdf_iso

with st.expander("See summary"):
    st.subheader(
        "MISO Generator Interconnection Costs to the Transmission System")
    st.markdown(
        '- Average interconnection costs have grown substantially over time.')
    st.markdown('- Projects that have completed all required interconnection studies have the lowest cost compared to applicants still actively working through the interconnection process or those that have withdrawn.')
    st.markdown(
        '- Broader network upgrade costs are the **primary driver** of recent cost increase.')
    st.markdown(
        '- Interconnection costs for wind, storage, and solar are greater than for natural gas.')
    st.markdown('- Larger generators have greater interconnection costs in absolute terms, but economies of scale exist on a per kW basis.')
    st.markdown(
        '- Interconnection costs vary by location as seen in the map below.')

with st.expander("See summary findings"):
    st.subheader('Findings:')
    st.info('Projects that were still actively moving through the interconnection queues saw **costs increase triple** over the last 3 years, from usd 48/kW to usd 156/kW (2018 vs. 2019-2021).')
    st.warning('**Network costs** are the real cost driver and have risen in recent years from **usd 57/kW for completed and usd 107/kW for active and for withdrawn have made up 85% of the costs measured at usd 388/kW**.')
    st.markdown('- Interconnection costs have **doubled 2000-2018 to usd 102/kW**.')
    st.markdown('- Projects that withdraw costs averaged usd 452/kW.')
    st.markdown('- Costs for projects in the study process averaged usd 156/kW.')
    st.markdown('- Costs grew for renewables grew considerably: solar costs usd 209/kW, storage usd 248/kW, whereas wind costs have rise 4x to usd 399/kW. For withdrawn wind projects this was usd 631/kW equivalent to 40% of total project costs with solar experiencing a similar pattern at 24% of total costs at usd 358/kW.')
    st.markdown('- Network costs increased dramatically since 2018 to usd 57/kW for completed, usd 107/kW active and usd 388/kW withdrawn.')
    st.markdown('- Eastern states (Indiana and Illinois) have comparatively lower interconnection costs (usd 50-70/kW for completed). North and South Dakota and parts of Texas have high potential costs usd 508/kW to usd 915/kW.')

with st.expander("See summary details"):
    st.subheader('Details:')
    st.info('The total requests in 2022 **increased by 220%** since 2021. The capacity of these requests is **2x the peak load** (120 GW).')
    st.markdown('- Cost sample represents 50% of new projects requesting interconnection between 2010-20.')
    st.markdown('- Does not reflect projects entering the queue after February 2022.')
    st.markdown('- 922 listed projects were evaluated.')
    st.markdown('- Only 349 with in service dates and 295 that were withdrawn.')
    st.markdown('- Only 25 of the 923 projects did not geomap or 2.7%.')    
    st.markdown('- Not all have cost data: 722 have POI costs (78%), 683 have network costs (74.1%) and 830 include total costs (90%).')

def unique_no_nan(x):
    return x.dropna().unique()

gdf, gdf_iso = load_cost_map_data()

row1_col1, row1_col2, row1_col3, row1_col4, row1_col5 = st.columns([1, 1, 1, 1, 1])
with row1_col1:
    status_list = list(unique_no_nan(gdf['request_status']))
    default_st = status_list.index('Withdrawn')
    status_type = st.selectbox('Status:',
                                   status_list,index=default_st,
                                   help = 'Filter to show the status type of the project (see fig. Interconnection Study Process).')
with row1_col2:
      year_list = gdf['q_year'].sort_values(ascending=False,na_position='last')
      year_list = list(unique_no_nan(year_list))
      default_yr = year_list.index(2020)
      select_yr = st.selectbox('Year entered queue:',
                                year_list,index=default_yr,
                                help = 'Filter to display the year in which the project entered the queue (see fig. Interconnection Study Process).')
with row1_col3:
      fuel_list = list(unique_no_nan(gdf['fuel']))
      default_ft = fuel_list.index('Solar')
      select_fuel = st.selectbox('Fuel:',
                                  fuel_list,index=default_ft,
                                  help = 'Filter report to show the fuel type of the project.')

gdf = gdf[gdf['q_year'] == select_yr]
gdf = gdf[gdf['fuel']==select_fuel]
gdf = gdf[gdf['request_status'] == status_type]
# not all of the records have cost information
gdf = gdf[gdf['real_total/kw']>0]
# creating a mid point to initialize the map
cmap_lat = gdf.centroid.y.mean()
cmap_lon = gdf.centroid.x.mean()
gdf = gdf[['NAME','real_poi/kw','real_network/kw','real_total/kw','nameplate_mw','geometry']]
gdf = gdf.to_crs(4326)
gdf['lon'] = gdf.centroid.x
gdf['lat'] = gdf.centroid.y

with st.expander("See map and source code"):
    with st.echo():
        cm = leafmap.Map(center=[cmap_lat, cmap_lon],
                        zoom_start=7,
                        tiles="stamentoner")

        cm.add_heatmap(
            gdf,
            latitude="lat",
            longitude="lon",
            value="real_total/kw",
            name="Heat map",
            radius=20,
        )

        g_hover_style = {"fillOpacity": 0.7}
        g_style = {
                "stroke": True,
                "color": "#0000ff",
                "weight": 2,
                "opacity": 1,
                "fill": True,
                "fillColor": "#0000ff",
                "fillOpacity": 0.1,
                "font-family": "lato"
                }

        cm.add_gdf(gdf,layer_name='Cost and Capacity',
                  zoom_to_layer=True,
                  info_mode='on_hover',
                  style=g_style,
                  hover_style=g_hover_style
                  )

        vmin = 0
        vmax = max(gdf['real_total/kw'])
        colors = ['a7d661','f2e250','f58727','f52b25']
        cm.add_colorbar(colors=colors, vmin=vmin, vmax=vmax,caption='Costs in $/kW')

        iso_style = {
                "stroke": True,
                "color": "#607fc2",
                "weight": 2,
                "opacity": 1,
                "fill": True,
                "fillColor": "##607fc2",
                "fillOpacity": 0.1,
                "font-family": "lato"
                }
        iso_hover_style = {"fillOpacity": 0.7}

        cm.add_geojson(ISO_FILE,
                      layer_name="MISO area",
                      style=iso_style,
                      hover_style=iso_hover_style,
                      show=False)

        # t_style = {
        #         "stroke": True,
        #         "color": "#8a8988",
        #         "weight": 1,
        #         "opacity": 0.5,
        #         "fill": True,
        #         "fillColor": "#94908b",
        #         "fillOpacity": 0.1,
        #         "font-family": "lato"
        #         }
        # t_hover_style = {"fillOpacity": 0.5}
        # m.add_geojson(TRANS_FILE,
        #               layer_name="HV transmission",
        #               style=t_style,
        #               hover_style=t_hover_style)

        plugins.MiniMap().add_to(cm)

cm.to_streamlit(height=700)

###########
# Display raw data
###########

if st.checkbox("Show Raw Cost Data from Map",False,help = 'Displays the raw data based on filters.'):
      st.subheader('Raw Cost Data')
      raw_gdf = gdf[['NAME','nameplate_mw','real_poi/kw','real_network/kw','real_total/kw']]
      raw_gdf.rename({'NAME':'County name','nameplate_mw':'Capacity (MW)'},axis=1,inplace=True)
      st.write(raw_gdf)

###########
# Boxplot chart
###########
chart_df = pd.DataFrame(gdf)
arr = chart_df[['real_poi/kw','real_network/kw','real_total/kw']]
columns = arr.columns.values.tolist()
fig, ax = plt.subplots()

ax.set(
# title='Cost distribution',
ylabel='Costs per kW',
# xlabel='Types of Costs'
)

ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)

ax.boxplot(arr,sym='+',vert=True,whis=1.5,notch=False)

ax.set_xticklabels(columns)

st.pyplot(fig)

###########
# Cost growth chart
###########

with st.expander("See technical notes"):
    st.subheader('Definitions:')
    # st.info('Project status: **"active"**, **"withdrawn"**, and **"completed"** projects. (see fig. Interconnection Study Process)')
    # st.markdown('- **Complete**: These projectshave completed all interconnection studies and progressed to (or completed) the interconnection agreement phase.This includes plants that are now in service.')
    # st.markdown('- **Active:** These  projects  are actively working through the  interconnection study process, progressing from an initial feasibility study via a system impact study to a refined facility study.')
    # st.markdown('- **Withdrawn:** These interconnection requests have been withdrawn from the queue (cancelled).')
    # st.info('Study Types: **"Interconnection Agreement"**,"Interim Interconnection Service Agreement", **"Facilities"**,**"System Impact"**, **"Feasibility"**, "WMPA". (see fig. Interconnection Study Process)')
    # st.markdown('- **2022 POI Cost/kW**: interconnection costs of point of interconnection components in real usd 2022/kW using a gdp deflator.')
    # st.markdown('- **2022 Network Cost/kW**: interconnection costs of network upgrade components in real usd 2022/kW using a gdp deflator.')
    # st.markdown('- **2022 Total Cost/kW**: total interconnection costs (sum of POI and network components) in real usd 2022/kW using a gdp deflator.')
    # st.info('Note: POI (Interconnection Facilities) costs usually do not include electrical facilities at the generator itself, like transformers or spur lines. Instead, they are predominantly driven by the construction of an interconnection station and transmission line extensions to those interconnection stations aka “Attachment Facilities” in PJM’sinterconnection studies.')

with st.expander("See MISO resources"):
    st.subheader('[MISO Resources:](https://www.misoenergy.org/planning/generator-interconnection/)')
    st.subheader('- [MISO queue](https://www.misoenergy.org/planning/generator-interconnection/GI_Queue/gi-interactive-queue/)')
    st.markdown('- [MISO Maps: Active Projects](https://giqueue.misoenergy.org/PublicGiQueueMap/index.html)')
    st.markdown('- [MISO Planning Modeling](https://www.misoenergy.org/planning/planning-modeling/)')
    st.markdown('- [MISO Future Planning Scenarios (https://www.misoenergy.org/planning/transmission-planning/futures-development/)')
    st.markdown('- MISO public tool [Points of Interconnection Map](https://giqueue.misoenergy.org/PoiAnalysis/index.html) (April-2020) for facilitate the assessment of grid impacts of proposed generation before submitting interconnection requests, but information is limited to line loading changes and does not include potential upgrade costs. ')

with st.expander("See service type notes"):
    st.subheader('Service Type')
    st.markdown('- Generators seeking interconnection must choose between **capacity** (FERC’s pro-forma LGIA as network resource interconnection service, NRIS) or **energy** service (energy resource interconnection service, ERIS).')
    st.markdown('- Capacity status reserves transmission capacity for the output of the generator during high load hours, for example allowing the project owner to have deliverable capacity that it can bid into resource adequacy markets. While  capacity resources may still be curtailed during emergency events, they are treated preferentially in comparison to energy resources. This privilege comes with  a  cost  however, as the generator may need to pay for additional transmission network upgrades.')
    st.markdown('- MISO should consider reducing the ERIS distribution factor cutoff in Generator Interconnection Definitive Planning Phase (DPP) studies from 20% to 10% to better mitigate overloaded facilities')
    st.markdown('- For MISO, ERIS will not be considered unless they have a confirmed firm transmission service reservation associated with the generator.')
