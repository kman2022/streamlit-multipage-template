import streamlit as st
import leafmap.foliumap as leafmap



st.set_page_config(page_title="PJM Costs ⚡",
                   page_icon='🔥',
                   layout="wide")


mkdwn_analysis = """
    **Source:** [Generator Interconnection Costs to the Transmission System:](https://emp.lbl.gov/interconnection_costs): Data for PJM Territory through 2022. Joachim Seel, Joseph Rand, Will Gorman, Dev Millstein, Ryan Wiser. January 2023.
"""

pjm_im = 'https://www.pjm.com/assets/responsive/img/pjm-logo.png'
st.sidebar.image(pjm_im,width=200)
st.sidebar.info(mkdwn_analysis)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("PJM Generator Interconnection Costs")

with st.expander("See summary"):
    st.subheader("PJM Generator Interconnection Costs to the Transmission System")
    st.markdown('- Average interconnection costs have grown substantially over time.')
    st.markdown('- Projects that have completed all required interconnection studies have the lowest cost compared to applicants still actively working through the interconnection process or those that have withdrawn.')
    st.markdown('- Broader network upgrade costs are the primary driver of recent cost increase.')
    st.markdown('- Interconnection costs for wind, storage, and solar are greater than for natural gas.')
    st.markdown('- Larger generators have greater interconnection costs in absolute terms, but economies of scale exist on a per kW basis.')
    st.markdown('- Interconnection costs vary by location.')
with st.expander("See summary details"):
    st.subheader('Details:')
    st.markdown('- 1,127 listed projects all with study dates.')
    st.markdown('- Only 215 with in service dates and 189 that were withdrawn.')
    st.markdown('- Not all have cost data: 818 have POI costs, 920 have network costs and 981 include total costs.')
    st.markdown('- Only 1 project has a duration under 3 months which appears to be related to the [Peach Bottom](https://www.nrc.gov/info-finder/reactors/pb3.html) relicensing in 2004 for which there are no cost data.')
    
with st.expander("See source code"):
    with st.echo():
        filepath = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
        m = leafmap.Map(center=[40, -100], zoom=4, tiles="stamentoner")
        m.add_heatmap(
            filepath,
            latitude="latitude",
            longitude="longitude",
            value="pop_max",
            name="Heat map",
            radius=20,
        )
m.to_streamlit(height=700)

with st.expander("See technical notes"):
    st.subheader('Definitions:')
    st.markdown('- Project status: "active", "withdrawn", and "completed" projects.')
    st.markdown('- Study Type: interconnection study (Feasibility Study, System Integration Study, Addendum).')
    st.markdown('- 2022 POI Cost/kW: interconnection costs of point of interconnection components in real usd 2022/kW using a gdp deflator.')
    st.markdown('- 2022 Network Cost/kW: interconnection costs of network upgrade components in real usd 2022/kW using a gdp deflator.')
    st.markdown('- 2022 Total Cost/kW: total interconnection costs (sum of POI and network components) in real usd 2022/kW using a gdp deflator.')
    st.markdown('- POI (Interconnection Facilities) costs usually do not include electrical facilities at the generator itself, like transformers or spur lines. Instead, they are predominantly driven by the construction of an interconnection station and transmission line extensions to those interconnection stations aka “Attachment Facilities” in PJM’sinterconnection studies.')
    st.markdown('- Network costs refer to two broad categories:') 
    st.markdown('- Network Upgrade Charges (consisting of estimates for “Direct Connection Facilities").')
    st.markdown('- Direct Connect Costs') 
    st.markdown('- Allocation for New System Upgrades” (or System Network Upgrades), “Contribution for Previously Identified Upgrades,” and “Other Charges”)')

with st.expander("See PJM resources"):
    st.subheader('[PJM](https://www.pjm.com/) Resources:')
    st.markdown('- [PJM Maps](https://www.pjm.com/library/maps)')
    st.markdown('- [PJM Planning](https://www.pjm.com/planning)')
    st.markdown('- [PJM Que Scope](https://queuescope.pjm.com/queuescope/pages/public/evaluator.jsf)')

with st.expander("See service type notes"):
    st.subheader('Service Type')
    st.markdown('- Generators seeking interconnection must choose between **capacity** (FERC’s pro-forma LGIA as network resource interconnection service, NRIS) or **energy** service (energy resource interconnection service, ERIS).')
    st.markdown('- Capacity status reserves transmission capacity for the output of the generator during high load hours, for example allowing the project owner to have deliverable capacity that it can bid into resource adequacy markets. While  capacity resources may still be curtailed during emergency events, they are treated preferentially in comparison to energy resources. This privilege comes with  a  cost  however, as the generator may need to pay for additional transmission network upgrades.')
    st.markdown('- Energy service permits participation in the energy market and largely uses the existing transmission system on an as available basis. The **vast majority (95%)** of all projects studied between 2017 and 2022 chose **capacity** as service type, a substantial increase over earlier years.')
    st.markdown('- Capacity status for wind offshore: 100%, solar: 99%,  wind  onshore: 98%. The  exception  of  solar  hybrid  projects (76%). Natural gas (95%) and storage (92%) stand-alone installations have slightly lower rates.')
