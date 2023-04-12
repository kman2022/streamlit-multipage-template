
import pandas as pd
import geopandas as gpd
import streamlit as st
import leafmap.foliumap as leafmap
from folium import plugins
import matplotlib.pyplot as plt
import matplotlib.style as style

st.set_page_config(page_title="NYISO Costs ⚡",
                   page_icon='https://i.imgur.com/UbOXYAU.png',
                   layout="wide")

# add transmission map

PROCESS_IMAGE = 'https://github.com/kman2022/data/blob/main/main/berkley/IQ_study_process_small%20copy.png?raw=true'
TRANSMISSION_IMAGE = 'https://github.com/kman2022/data/blob/main/main/berkley/transmission.png?raw=true'
nyiso_im = 'https://www.nyiso.com/o/nyiso-main-theme/images/logo.svg'
NY_MAP_GEO = "https://github.com/kman2022/data/blob/main/main/berkley/gdp_cost_nyiso_qeo.geojson?raw=true"
NYISO_FILE = 'https://github.com/kman2022/data/blob/main/main/berkley/nyiso.geojson?raw=true'
# TRANS_FILE = 'https://github.com/kman2022/data/blob/main/main/berkley/miso_transmission_short.geojson?raw=true'

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
    **Source:** [Generator Interconnection Costs to the Transmission System:](https://emp.lbl.gov/interconnection_costs) Kemp J., Seel J., Rand J., Millstein D., Kahrl F., Gorman W., Wiser R., "Interconnection Cost Analysis in the NYISO Territory" Mar-2023 (data 2006 thru 2021).
"""

st.sidebar.image(nyiso_im, width=200)
st.sidebar.image(TRANSMISSION_IMAGE, width=200)
st.sidebar.image(PROCESS_IMAGE, width=300,
                 caption="fig. Interconnection Study Process")
st.sidebar.info(mkdwn_analysis)
st.title("NYISO Generator Interconnection Costs")

###########
# Load data
###########

@st.cache_data(persist=True)
def load_cost_map_data():
    # clean ' $-   ' from network cost column
    # geodf
    gdf = gpd.read_file(NY_MAP_GEO)
    gdf.replace(' $-   ',0,inplace=True)
    gdf['$2022_network_cost/kw'] = gdf['$2022_network_cost/kw'].astype(float)
    # geoloc shape
    gdf_iso = gpd.read_file(NYISO_FILE)
    return gdf, gdf_iso

with st.expander("See summary"):
    st.subheader(
        "NYISO Generator Interconnection Costs to the Transmission System")
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
    st.info('**Project-specific interconnection costs can differ widely** depending on many variables and do not follow a normal distribution, among in-service projects studied by NYISO since 2017, more than half cost less than usd 100/kW to interconnect, yet one project cost almost usd 1,000/kW.')
    st.markdown('- Interconnection costs have **doubled since 2017** (mean: usd 86/kW to  usd 167/kW, median: usd 66/kW to usd 115/kW) relative to costs for projects studied from 2006 to 2016.')
    st.markdown('- Projects still actively moving through the queue (“active”) also have higher costs (mean: usd 145/kW, median: usd 108/kW) than historical projects (all of which have withdrawn from the queue or been completed).')
    st.markdown('- Solar project interconnection costs are **8-18 % higher than costs for other resources**.')
    st.markdown('- Larger generators have greater interconnection costs in absolute terms, but economies of scale exist for all projects. Specifically, average costs for small (<50 MW) and large (≥250 MW) solar projects are **usd 224/kW and usd 70/kW**, respectively, and the corresponding costs for small and large onshore wind projects are **usd 264/kW and usd 45/kW**. Natural gas and storage projects do not display a clear trend between project capacity and interconnection costs per kW.')
    st.markdown('- Cost estimates increase as projects complete more studies in the interconnection process. Costs for the same project increase by **usd 30/kW on average from their system impact study to their facilities study**, with costs at least doubling for more than a quarter of projects. Between the feasibility study and the system impact study, cost increases are usually more modest: $16/kW on average with a median change of 0%.')
    st.markdown('- POI costs represented 48% and 53% of the average total for complete and active projects from 2017-2021, up from 40% for complete projects during 2006-2016. In both time periods, at least 90% of projects expected some (nonzero) POI costs. POI costs comprise a greater portion of the total for projects that ultimately withdraw from the interconnection process7, a situation that is **distinct from MISO and PJM** where network upgrades dominate withdrawn project costs.')
    st.markdown('- Network costs did grow at a faster rate than POI costs among withdrawn projects, however, decreasing POI’s share of the total from 69% during 2006-2016 to 62% during 2017-2021.')
    st.markdown('- **Interconnection costs vary by location:** Nassau County (on Long Island) and Monroe County (includes Rochester) have the highest costs among counties with more than one project. The most northern and western counties tend to have lower costs than those located more centrally or to the southeast. Location, at the county level, does not appear to have a significant impact on the cost to interconnect onshore wind projects, compared to other resources which have more geographic variation.')
    st.markdown('- Suffolk County (on Long Island) is an expensive location to interconnect solar projects (4 projects studied since 2017, mean: usd 665/kW, median: usd 612/kW), but has much lower costs for proposed storage (10 projects studied since 2017, median: usd 60/kW) and offshore wind (4 projects studied since 2017, mean: usd 53/kW, median: usd 19/kW). As background, Suffolk County belongs to Zone K, where capacity prices were the highest in NYISO nearly every month in summer 2021 and summer 2022, reaching at least twice the price of the broader New York Control Area in some months. This Suffolk County example highlights the challenge of estimating interconnection costs in advance of completing interconnection studies, even within a small geographic area.')

with st.expander("See summary details"):
    st.subheader('Details:')
    st.info('As of November 2022, NYISO had nearly 107 gigawatts (GW) of generation and storage capacity actively seeking grid interconnection (NYISO’s peak loadcwas 30.5 GW in 2022). This “active” capacity in NYISO’s queue is dominated by wind (65 GW of offshore and onshore wind, combined) and, to a lesser extent, battery storage (20 GW) and solar (20 GW) power capacity; those three resources alone account for 98% of all capacity actively seeking interconnection.')
    st.markdown('- Cost sample represents 43% of new projects requesting interconnection between 2003-2019.')
    st.markdown('- Does not reflect projects entering the queue after May 2022.')
    st.markdown('- 310 listed projects were evaluated using interconnection studies between 2006 and 2021.')
    st.markdown('- Manually extracting cost information from study PDFs typically took 25-40 minutes per project for a total of about 430 hours.')
    st.markdown('- All 294 projects geomap after correcting county/place info.')
    # st.markdown('- 274 have POI costs (93%), 683 have network costs (74.1%) and 830 include total costs (90%).')


def unique_no_nan(x):
    return x.dropna().unique()


gdf, gdf_iso = load_cost_map_data()

row1_col1, row1_col2, row1_col3, row1_col4, row1_col5 = st.columns([
                                                                   1, 1, 1, 1, 1])
with row1_col1:
    status_list = list(unique_no_nan(gdf['request_status']))
    default_st = status_list.index('Active')
    status_type = st.selectbox('Status:',
                                   status_list, index=default_st,
                                   help='Filter to show the status type of the project (see fig. Interconnection Study Process).')
with row1_col2:
      year_list = gdf['q_year'].sort_values(
          ascending=False, na_position='last')
      year_list = list(unique_no_nan(year_list))
      default_yr = year_list.index(2019)
      select_yr = st.selectbox('Year entered queue:',
                                year_list, index=default_yr,
                                help='Filter to display the year in which the project entered the queue (see fig. Interconnection Study Process).')
with row1_col3:
      fuel_list = list(unique_no_nan(gdf['resource_type']))
      default_ft = fuel_list.index('Solar')
      select_fuel = st.selectbox('Fuel:',
                                  fuel_list, index=default_ft,
                                  help='Filter report to show the fuel type of the project.')

gdf = gdf[gdf['q_year'] == select_yr]
gdf = gdf[gdf['resource_type'] == select_fuel]
gdf = gdf[gdf['request_status'] == status_type]
# not all of the records have cost information
gdf = gdf[gdf['$2022_total_cost/kw'] > 0]
# creating a mid point to initialize the map
cmap_lat = gdf.centroid.y.mean()
cmap_lon = gdf.centroid.x.mean()
gdf = gdf[['county', '$2022_poi_cost/kw', '$2022_network_cost/kw',
    '$2022_total_cost/kw', 'nameplate_mw', 'geometry']]
gdf = gdf.to_crs(4326)
gdf['lon'] = gdf.centroid.x
gdf['lat'] = gdf.centroid.y

with st.expander("See map and source code"):
    with st.echo():

        n_map = leafmap.Map(center=[cmap_lat, cmap_lon],
                        zoom_start=7,
                        tiles="stamentoner")

        n_map.add_heatmap(
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
                }

        n_map.add_gdf(gdf, layer_name='Cost and Capacity',
                  zoom_to_layer=True,
                  info_mode='on_hover',
                  style=g_style,
                  hover_style=g_hover_style
                  )

        vmin = 0
        vmax = max(gdf['$2022_total_cost/kw'])
        colors = ['a7d661', 'f2e250', 'f58727', 'f52b25']
        n_map.add_colorbar(colors=colors, vmin=vmin,
                        vmax=vmax, caption='Costs in $/kW')

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

        n_map.add_geojson(NYISO_FILE,
                      layer_name="NYISO area",
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

        plugins.MiniMap().add_to(n_map)

n_map.to_streamlit(height=700)

###########
# Display raw data
###########

raw_gdf = gdf[['county', 'nameplate_mw', '$2022_poi_cost/kw','$2022_network_cost/kw', '$2022_total_cost/kw']]
raw_gdf.rename({'county': 'County name', 'nameplate_mw': 'Capacity (MW)'}, axis=1, inplace=True)

if st.checkbox("Show Raw Cost Data from Map", False, help='Displays the raw data based on filters.'):
      st.subheader('Raw Cost Data')
      st.write(raw_gdf)

###########
# Boxplot chart
###########
chart_df = pd.DataFrame(gdf)
arr = chart_df[['$2022_poi_cost/kw', '$2022_network_cost/kw', '$2022_total_cost/kw']]
columns = arr.columns.values.tolist()
fig, ax = plt.subplots()

ax.set(
# title='Cost distribution',
ylabel='Costs per kW',
# xlabel='Types of Costs'
)

ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)

ax.boxplot(arr, sym='+', vert=True, whis=1.5, notch=False)

ax.set_xticklabels(columns)

st.pyplot(fig)

###########
# Cost growth chart
###########

with st.expander("See technical notes"):
    st.subheader('Definitions:')
    st.info('Project status: **"active"**, **"withdrawn"**, and **"completed"** projects. (see fig. Interconnection Study Process)')
    st.markdown('- Large Generator Interconnection Agreement (**LGIA**) The NYISO’s tender of the LGIA commences a six-month time limitation for the Developer to execute the LGIA.')
    st.markdown('- **Complete**: These projectshave completed all interconnection studies and progressed to (or completed) the interconnection agreement phase.This includes plants that are now in service.')
    st.markdown('- **Active:** These projects are actively working through the interconnection study process, progressing from an initial feasibility study via a system impact study to a refined facility study.')
    st.markdown('- **Withdrawn:** These interconnection requests have been withdrawn from the queue (cancelled).')
    st.markdown('- **Queue ID 2:** additional queue position identifier, present for two-phase projects with two interconnection requests (one request per phase) that are treated as one project with aggregated costs and capacity in this study.')

    st.info('Study Types: **"Facilities Part 1 & 2"**,**"System Impact"**, **"Feasibility"**. (see fig. Interconnection Study Process)')
    st.markdown('- **2022 POI Cost/kW**: interconnection costs of point of interconnection components in real usd 2022/kW using a gdp deflator.')
    st.markdown('- **2022 Network Cost/kW**: interconnection costs of network upgrade components in real usd 2022/kW using a gdp deflator.')
    st.markdown('- **2022 Total Cost/kW**: total interconnection costs (sum of POI and network components) in real usd 2022/kW using a gdp deflator.')
    st.markdown('- Note: POI (Interconnection Facilities) costs usually do not include electrical facilities at the generator itself, like transformers or spur lines. Instead, they are predominantly driven by the construction of an interconnection station and transmission line extensions to those interconnection stations. The categories are referred to in the interconnection studies as “Connecting Transmission Owner Attachment Facilities” and “Stand-alone System Upgrade Facilities.” Commonly listed equipment includes new POI stations, revenue metering, and disconnect switches at the point of change of ownership."')
    st.markdown('- Note: Network costs are referred to in interconnection studies as “System Upgrade Facilities,” “System Deliverability Upgrades,” “Affected System Upgrades,” “Part 2 Allocation,” and “Headroom Payments.” A wide array of upgrades and equipment can fall in this category, including remote substation work, transmission line protection upgrades, and other transmission line work.')

with st.expander("See NYISO resources"):
    st.subheader('[NYISO Resources:](https://www.nyiso.com/cspp)')
    st.subheader('[NYISO queue](https://www.nyiso.com/interconnections)')
    st.markdown('- [NYISO Power System Information](https://www.nyiso.com/ny-power-system-information-outlook)')
    st.markdown('- [NYISO Planning Reñiability Compliance](https://www.nyiso.com/planning-reliability-compliance)')
    st.markdown('- The Climate Leadership and Community Protection Act (CLCPA) of 2019 that mandates New York State procure 9 GW of offshore wind by 2035. Long Island offers the closest interconnection location for several offshore lease areas. Based on the expected influx of offshore wind power driven by the CLCPA, the Long Island Power Authority identified, and the New York Public Service Commission (PSC) established, the need for (1) increased export capability “from Zone K to Zones I and J to ensure the full output from at least 3,000 MW of offshore wind is deliverable from Long Island to the rest of the State” and (2) upgraded local transmission facilities to support the increased export capability (“Order Addressing Public Policy Requirements For Transmission Planning Purposes” 2021). This is known as the Long Island Offshore Wind Export Public Policy Transmission Need ([LI PPTN](https://www.nyiso.com/documents/20142/22968753/LI-OSW-Export-PPTN-Viability-Sufficiency-Assessment_Report.pdf)).')
    st.markdown('- The costs of selected LI PPTN transmission project(s) will be allocated to all load zones in the state based on their share of total energy consumption. Statewide allocation, as opposed to assigning most costs to Long Island and New York City where the project(s) will be located, was deemed most appropriate by the PSC because “the entire focus of the identified transmission need is on facilitating compliance with the CLCPA” (“Order On Petitions For Rehearing - Case 20-E-0497 and Case 18-E-0623” 2022).')

with st.expander("See interconnection study notes"):
    st.subheader('NYISO Interconnection Studies (see [manual Jan-23](https://www.nyiso.com/documents/20142/2924447/tei_mnl.pdf/b2f926e9-2faa-2c42-5a09-2402cdb8bacc?t=1672852997127))')
    st.markdown('- **Feasibility Study:** The IR fee is 10k usd, the FS deposit is 10k usd. It takes from 45 to 90 days.')
    st.markdown('- **System Impact Study:** The deposit is 120k usd. It takes around 90 days.')
    st.markdown('- **Facilities Study:** The deposit is 100k usd or 50k usd as applicable.')
    st.markdown('- NYISO initiated substantial interconnection process reforms in 2019, which were designed to expedite the interconnection study process. The reforms included requiring deliverability evaluation earlier in the process, removing duplication between studies, and shortening the timeline for developers to submit data for class year studies.')
    st.markdown('- With the queue reaching an unprecedented volume in 2022, NYISO began consideringadditional interconnection process improvements and reforms, such as developing system impact study report templates, adding staff dedicated to interconnection support, enhancing the interconnection portal, and moving to a “queue window-based approach with a binding multi-phase study structure” (Smith 2022), the details of which are not yet available.')
    st.markdown('- In NYISO, the change in a project’s expected interconnection costs from their feasibility study to their system impact study is typically modest, with the majority of projects experiencing an increase between 25% and -5% (where a negative value indicates a cost decrease). This corresponds to an increase of usd 16/kW on average. Between the system impact study and the most recent facilities study, cost increases are more substantial: costs change by at least 50% for around half the projects, and more than a quarter of projects see costs at least double. The average increase of usd 30/kW is due to cost increases both at the POI and in the broader network.')
    st.markdown('- Cost estimates for active projects are primarily based on system impact studies (74%), suggesting the current costs reported for this group may underestimate the costs that will ultimately be paid to interconnect.')
    st.markdown('- The majority of solar projects in the interconnection queue are small (<50 MW) which contributes to their high cost, since we show in following section that economies of scale exist for solar interconnection costs. The other resource types do not present consistently high or low costs relative to one another, unlike in MISO (Seel et al. 2022) and PJM (Seel et al. 2023), where natural gas had the lowest interconnection costs in recent years.')
    st.markdown('- While interconnection costs for resources of any type, anywhere in the system could change because of LI PPTN projects, it is reasonable to expect that offshore wind projects interconnecting in Long Island are among the most sensitive to this change and will likely see reduced costs.')
    st.markdown('- Cost estimates used were generally from the most recent available interconnection study report for each project. However, when the most recent study was a class year facilities study – part 2, which lacks the cost detail present in other studies, information from the second-most recent study was also incorporated. Specifically, oConnecting transmission owner attachment facility (CTOAF) costs from second-most recent study were used, since they are not reported in the most recent study, andoThe ratio of POI to network costs within system upgrade facilities costs in the second-most recent study is applied to the reported total of system upgrade facilities costs in part 1.')
    st.markdown('- Interconnection requests that do not refer to new generation or storage projects, such as transmission, repowering, or uprate projects, are excluded.')
    st.markdown('- Each project’s request status is based on NYISO’s published interconnection queue as of 7 December2021.')

with st.expander("See service type notes"):
    st.subheader('Service Type')
    st.markdown('- Generators seeking interconnection must choose between **capacity** (FERC’s pro-forma LGIA as network resource interconnection service, NRIS) or **energy** service (energy resource interconnection service, ERIS).')
    st.markdown('- Capacity status reserves transmission capacity for the output of the generator during high load hours, for example allowing the project owner to have deliverable capacity that it can bid into resource adequacy markets. While capacity resources may still be curtailed during emergency events, they are treated preferentially in comparison to energy resources. This privilege comes with a cost however, as the generator may need to pay for additional transmission network upgrades.')
    st.markdown('- NYISO should consider reducing the ERIS distribution factor cutoff in Generator Interconnection Definitive Planning Phase (DPP) studies from 20% to 10% to better mitigate overloaded facilities')
    st.markdown('- For NYISO, ERIS will not be considered unless they have a confirmed firm transmission service reservation associated with the generator.')
