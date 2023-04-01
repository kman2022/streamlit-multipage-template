import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(page_title="PJM Costs ⚡",
                   page_icon='https://i.imgur.com/UbOXYAU.png',
                   layout="wide")

PROCESS_IMAGE = 'https://github.com/kman2022/data/blob/main/main/berkley/IQ_study_process_small%20copy.png?raw=true'
TRANSMISSION_IMAGE = 'https://github.com/kman2022/data/blob/main/main/berkley/transmission.png?raw=true'
pjm_im = 'https://www.pjm.com/assets/responsive/img/pjm-logo.png'

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
    st.markdown('- PJM launched a new public tool [QueueScope](https://queuescope.pjm.com/queuescope/pages/public/evaluator.jsf) in Dec-2022 to facilitate the assessment of grid impacts of proposed generation before submitting interconnection requests, but information is limited  to line loading changes and does not include potential upgrade costs.')

with st.expander("See service type notes"):
    st.subheader('Service Type')
    st.markdown('- Generators seeking interconnection must choose between **capacity** (FERC’s pro-forma LGIA as network resource interconnection service, NRIS) or **energy** service (energy resource interconnection service, ERIS).')
    st.markdown('- Capacity status reserves transmission capacity for the output of the generator during high load hours, for example allowing the project owner to have deliverable capacity that it can bid into resource adequacy markets. While  capacity resources may still be curtailed during emergency events, they are treated preferentially in comparison to energy resources. This privilege comes with  a  cost  however, as the generator may need to pay for additional transmission network upgrades.')
    st.markdown('- Energy service permits participation in the energy market and largely uses the existing transmission system on an as available basis. The **vast majority (95%)** of all projects studied between 2017 and 2022 chose **capacity** as service type, a substantial increase over earlier years.')
    st.markdown('- Capacity status for wind offshore: 100%, solar: 99%,  wind  onshore: 98%. The  exception  of  solar  hybrid  projects (76%). Natural gas (95%) and storage (92%) stand-alone installations have slightly lower rates.')
