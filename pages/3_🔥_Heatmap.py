import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
Web App URL: <https://template.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Heatmap")

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

st.markdown('------')
st.header('Technical Notes:')
st.markdown('- POI (Interconnection Facilities) costs usually do not include electrical facilities at the generator itself, like transformers or spur lines. Instead, they are predominantly driven by the construction of an interconnection station and transmission line extensions to those interconnection stations aka “Attachment Facilities” in PJM’sinterconnection studies.')
st.markdown('- Network costs refer to two broad categories: Network Upgrade Charges (consisting of estimates for “Direct Connection Facilities”, “Total Direct Connect Costs”, “Direct Connection Network Upgrades”, “Total Non-Direct Connection Costs”, “Network Upgrade Facilities,” “Non Direct Connection Facilities” and “Non Direct Connection Network Upgrades”) and Other Network Costs (consisting of estimates for "Non-Direct  Local  Network  Upgrades,”“Allocation for New System Upgrades” (or System Network Upgrades), “Contribution for Previously Identified Upgrades,” and “Other Charges”)')
st.markdown('- [PJM Maps](https://www.pjm.com/library/maps)')
st.subheader('Service Type')
st.markdown('Generators seeking interconnection must choose between capacity (FERC’s pro-forma LGIA as network resource interconnection service, NRIS) or energy service (energy resource interconnection service, ERIS).')
st.markdown('Capacity status reserves transmission capacity for the output of the generator during high load hours, for example allowing the project owner to have deliverable capacity that it can bid into resource adequacy markets.')
st.markdown('While  capacity resources may still be curtailed during emergency events, they are treated preferentially in comparison to energy resources. This privilege comes with  a  cost  however, as the generator may need to pay for additional transmission network upgrades.')
st.markdown('Energy service permits participation in the energy market and largely uses the existing transmission system on an as available basis.')
st.markdown('- The vast majority (95%) of all projects studied between 2017 and 2022 chose capacity as service type, a substantial increase over earlier years.')
st.markdown('- Nearly all renewable projects opt for capacity status (wind offshore: 100%, solar: 99%,  wind  onshore: 98%) with  the  exception  of  solar  hybrid  projects (76%). Natural gas (95%) and storage (92%) stand-alone installations have slightly lower rates.')
