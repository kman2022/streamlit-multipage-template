
# import numpy as np
# import pandas as pd
import geopandas as gpd
import streamlit as st
import leafmap.foliumap as leafmap
from folium import plugins
# import folium
# from streamlit_folium import st_folium
# from folium.plugins import Draw
# import leafmap.colormaps as cm
# from leafmap.common import hex_to_rgb

st.set_page_config(page_title="PJM Costs ⚡",
                   page_icon='https://i.imgur.com/UbOXYAU.png',
                   layout="wide")

PROCESS_IMAGE = 'https://github.com/kman2022/data/blob/main/main/berkley/IQ_study_process_small%20copy.png?raw=true'
TRANSMISSION_IMAGE = 'https://github.com/kman2022/data/blob/main/main/berkley/transmission.png?raw=true'
pjm_im = 'https://www.pjm.com/assets/responsive/img/pjm-logo.png'
MAP_FILE = "https://github.com/kman2022/data/blob/main/main/berkley/df_pjm_cost_map_agg.csv?raw=true"
MAP_GEO = "https://github.com/kman2022/data/blob/main/main/berkley/gdf_pjm_cost_map_agg.geojson?raw=true"

ISO_FILE = 'https://github.com/kman2022/data/blob/main/main/berkley/pjm.geojson?raw=true'
TRANS_FILE = 'https://github.com/kman2022/data/blob/main/main/berkley/pjm_transmission_short.geojson?raw=true'

mkdwn_analysis = """
    **Source:** [Generator Interconnection Costs to the Transmission System:](https://emp.lbl.gov/interconnection_costs): Data for PJM Territory through 2022. Joachim Seel, Joseph Rand, Will Gorman, Dev Millstein, Ryan Wiser. January 2023.
"""

st.sidebar.image(pjm_im, width=200)
st.sidebar.image(TRANSMISSION_IMAGE, width=200)
st.sidebar.image(PROCESS_IMAGE, width=300,
                 caption="fig. Interconnection Study Process")

st.title("PJM Generator Interconnection Costs")

# quantify growth
# quantify costs / split out / split out by fuel
# are costs and connection times higher in the border regions where must coordinate with adjoing tso?
@st.cache_data(persist=True)
def load_pjm_cost_map_data():
    # df hist
    # df_map_cost = pd.read_csv(MAP_FILE)
    # geodf
    gdf = gpd.read_file(MAP_GEO)
    # geoloc shape
    gdf_iso = gpd.read_file(ISO_FILE)
    # return df_map_cost, gdf, gdf_iso
    return gdf, gdf_iso

with st.expander("See summary"):
    st.subheader(
        "PJM Generator Interconnection Costs to the Transmission System")
    st.markdown(
        '- Average interconnection costs have grown substantially over time.')
    st.markdown('- Projects that have completed all required interconnection studies have the lowest cost compared to applicants still actively working through the interconnection process or those that have withdrawn.')
    st.markdown(
        '- Broader network upgrade costs are the primary driver of recent cost increase.')
    st.markdown(
        '- Interconnection costs for wind, storage, and solar are greater than for natural gas.')
    st.markdown('- Larger generators have greater interconnection costs in absolute terms, but economies of scale exist on a per kW basis.')
    st.markdown(
        '- Interconnection costs vary by location as seen in the map below.')

with st.expander("See summary findings"):
    st.subheader('Findings:')
    st.success('More than **95% of all projects have interconnection costs under usd 200/kW**, but five projects cluster around usd 400/kW and two havec osts of usd 712/kW and usd 3,728/kW. Typical project costs are $24/kW.')
    st.warning('Interconnection costs have **doubled from usd 42/kW before 2020 to usd 84/kW between 2020 and 2022**.')
    st.warning('Projects that were still actively moving through the interconnection queues saw **costs increase eightfold**, from usd 29/kW to usd 240/kW (2017-2019 vs. 2020-2022.')
    st.warning('Projects that withdraw have seen *costs more than double*,from usd 255/kW to usd 599/kW (2017-2019 vs. 2020-2022).')
    st.warning('Costs for withdrawn projects are *more than seven times* the costs of “complete” projects between 2017 and 2022 (usd521/kWvs. usd 73/kW.')
    st.warning('**Network costs** are the real cost driver and have risen in recent years from **usd 15/kW in 2017-2019 to usd 227/kW in 2020-2022**.')
    st.info('Looking at projects studied before and after 2017, we find that natural gas interconnection costs fell from usd 40/kW to usd 18/kW. Costs grew for renewables: solar costs increased from usd 54/kW to usd 99/kW, whereas onshore wind costs rise from usd 23/kW to usd 60/kW.')
    st.info('Network costs increased dramatically for active and withdrawn projects relative to those that completed all studies. Completed storage projects had no network upgrade costs (n=7), while the average costs for withdrawn projects was usd 709/kW (n=17). Network costs were *25 times greater* for withdrawn solar hybrid projects relative to complete projects (usd 457/kW vs. usd 18/kW). Withdrawn solar projects had **six times greater network costs** than complete projects (usd 520/kW vs. usd 82/kW), and withdrawn onshore wind projects had nearly five times the network costs of complete projects (usd 258/kW vs usd 56/kW).')
    st.info('Eastern states again have comparatively high interconnection costs among complete (New Jersey: usd 143/kW) and withdrawn  projects (North Carolina: usd 1,068/kW, New Jersey: usd 759/kW), while western states like Indiana and Illinois have lower costs for  completed  projects (usd 14/kW, usd 20/kW), as do Kentucky and Ohio for withdrawn projects (usd 88/kW, usd 108/kW). (seen map below)')

with st.expander("See summary details"):
    st.subheader('Details:')
    st.markdown('- Cost sample represents 86% of new generators requesting interconnection over the past decade.')
    st.markdown('- Does not reflect projects entering the queue after March 2021.')
    st.markdown('- Data acquisition required manual cost extraction from study pdfs averaging 30-50 minutes per project, equivalent to about 550 hours for the entire sample.')
    st.markdown('- 1,127 listed projects all with study dates.')
    st.markdown('- Only 215 with in service dates and 189 that were withdrawn.')
    st.markdown('- Not all have cost data: 818 have POI costs, 920 have network costs and 981 include total costs.')
    st.markdown('- Only 1 project has a duration under 3 months which appears to be related to the [Peach Bottom](https://www.nrc.gov/info-finder/reactors/pb3.html) relicensing in 2004 for which there are no cost data.')

def unique_no_nan(x):
    return x.dropna().unique()

# assign data and filters
# df_map_cost, gdf, gdf_iso = load_pjm_cost_map_data()

gdf, gdf_iso = load_pjm_cost_map_data()

# volume how to make 3D or format the border of the polygon - team
# perhaps a better way to display map filtering by cost type - team
# need format popup box - team
# need chart below showing avg cost by status type
# need chart showing cost growth

row1_col1, row1_col2, row1_col3, row1_col4, row1_col5 = st.columns([1, 1, 1, 1, 1])
with row1_col1:
    status_list = list(unique_no_nan(gdf['request_status']))
    default_st = status_list.index('Complete')
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
gdf = gdf[gdf['$2022_total_cost/kw']>0]
# creating a mid point to initialize the map
map_lat = gdf.centroid.y.mean()
map_lon = gdf.centroid.x.mean()
gdf = gdf[['NAME','$2022_poi_cost/kw','$2022_network_cost/kw','$2022_total_cost/kw','nameplate_mw','geometry']]
gdf = gdf.to_crs(4326)
gdf['lon'] = gdf.centroid.x  
gdf['lat'] = gdf.centroid.y

with st.expander("See map and source code"):
    with st.echo():
        m = leafmap.Map(center=[map_lat, map_lon], 
                        zoom_start=7, 
                        tiles="stamentoner")

        m.add_heatmap(
            gdf,
            latitude="lat",
            longitude="lon",
            value="$2022_total_cost/kw",
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
                # 'fillColor': 'red' if feature['properties']['$2022_total_cost/kw'] > 150 else '#0000ff',
                }
        
        m.add_gdf(gdf,layer_name='Cost and Capacity', 
                  zoom_to_layer=True, 
                  info_mode='on_hover',
                  style=g_style,
                  hover_style=g_hover_style
                  )
        
        vmin = 0
        vmax = max(gdf['$2022_total_cost/kw'])
        colors = ['a7d661','f2e250','f58727','f52b25']
        m.add_colorbar(colors=colors, vmin=vmin, vmax=vmax,caption='Costs in $/kW')
        
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
        
        m.add_geojson(ISO_FILE, 
                      layer_name="PJM area", 
                      style=iso_style, 
                      hover_style=iso_hover_style,
                      show=False)
        
        t_style = {
                "stroke": True,
                "color": "#8a8988",
                "weight": 1,
                "opacity": 0.5,
                "fill": True,
                "fillColor": "#94908b",
                "fillOpacity": 0.1,
                "font-family": "lato"
                }
        t_hover_style = {"fillOpacity": 0.5}
        m.add_geojson(TRANS_FILE, 
                      layer_name="HV transmission", 
                      style=t_style, 
                      hover_style=t_hover_style)
        
        plugins.MiniMap().add_to(m)
        
m.to_streamlit(height=700)

if st.checkbox("Show Raw Cost Data from Map",False,help = 'Displays the raw data based on filters.'):
      st.subheader('Raw Cost Data')
      raw_gdf = gdf[['NAME','nameplate_mw','$2022_poi_cost/kw','$2022_network_cost/kw','$2022_total_cost/kw']]
      raw_gdf.rename({'NAME':'County name','nameplate_mw':'Capacity (MW)'},axis=1,inplace=True)
      st.write(raw_gdf)

# st.plotly_chart(f)

with st.expander("See technical notes"):
    st.subheader('Definitions:')
    st.info('Project status: **"active"**, **"withdrawn"**, and **"completed"** projects. (see fig. Interconnection Study Process)')
    st.markdown('- **Complete**: These projectshave completed all interconnection studies and progressed to (or completed) the interconnection agreement phase.This includes plants that are now in service.')
    st.markdown('- **Active:** These  projects  are actively working through the  interconnection study process, progressing from an initial feasibility study via a system impact study to a refined facility study.')
    st.markdown('- **Withdrawn:** These interconnection requests have been withdrawn from the queue (cancelled).')
    st.info('Study Types: **"Interconnection Agreement"**,"Interim Interconnection Service Agreement", **"Facilities"**,**"System Impact"**, **"Feasibility"**, "WMPA". (see fig. Interconnection Study Process)')
    st.markdown('- **2022 POI Cost/kW**: interconnection costs of point of interconnection components in real usd 2022/kW using a gdp deflator.')
    st.markdown('- **2022 Network Cost/kW**: interconnection costs of network upgrade components in real usd 2022/kW using a gdp deflator.')
    st.markdown('- **2022 Total Cost/kW**: total interconnection costs (sum of POI and network components) in real usd 2022/kW using a gdp deflator.')
    st.info('Note: POI (Interconnection Facilities) costs usually do not include electrical facilities at the generator itself, like transformers or spur lines. Instead, they are predominantly driven by the construction of an interconnection station and transmission line extensions to those interconnection stations aka “Attachment Facilities” in PJM’sinterconnection studies.')

with st.expander("See PJM resources"):
    st.subheader('[PJM](https://www.pjm.com/) Resources:')
    st.markdown('- [PJM Maps](https://www.pjm.com/library/maps)')
    st.markdown('- [PJM Planning](https://www.pjm.com/planning)')
    st.markdown('- PJM launched a new public tool [QueueScope](https://queuescope.pjm.com/queuescope/pages/public/evaluator.jsf) in Dec-2022 to facilitate the assessment of grid impacts of proposed generation before submitting interconnection requests, but information is limited to line loading changes and does not include potential upgrade costs. ')

with st.expander("See PJM news"):
    st.markdown('- [IER](https://www.instituteforenergyresearch.org/the-grid/pjm-plans-for-a-two-year-pause-on-reviewing-project-applications/) Wind, solar and hydro represent roughly 6% of installed capacity but represent the overwhelming majprity of projects stuck in the queue. ')
    st.markdown('- [1898 Blog](https://1898blog.burnsmcd.com/finding-new-opportunities-under-a-streamlined-pjm-interconnection-process) The congestion is largely due to the increase in applications for renewable solar, wind, energy storage or combined generation and storage projects. ')

with st.expander("See service type notes"):
    st.subheader('Service Type')
    st.markdown('- Generators seeking interconnection must choose between **capacity** (FERC’s pro-forma LGIA as network resource interconnection service, NRIS) or **energy** service (energy resource interconnection service, ERIS).')
    st.markdown('- Capacity status reserves transmission capacity for the output of the generator during high load hours, for example allowing the project owner to have deliverable capacity that it can bid into resource adequacy markets. While  capacity resources may still be curtailed during emergency events, they are treated preferentially in comparison to energy resources. This privilege comes with  a  cost  however, as the generator may need to pay for additional transmission network upgrades.')
    st.markdown('- Energy service permits participation in the energy market and largely uses the existing transmission system on an as available basis. The **vast majority (95%)** of all projects studied between 2017 and 2022 chose **capacity** as service type, a substantial increase over earlier years.')
    st.markdown('- Capacity status for wind offshore: 100%, solar: 99%,  wind  onshore: 98%. The  exception  of  solar  hybrid  projects (76%). Natural gas (95%) and storage (92%) stand-alone installations have slightly lower rates.')


