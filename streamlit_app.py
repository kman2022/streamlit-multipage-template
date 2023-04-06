import streamlit as st

UC_IMAGE = '🔌'
PWR_IMAGE = 'https://raw.githubusercontent.com/kman2022/data/main/main/berkley/power_pic.jpeg'
PROCESS_IMAGE ='https://github.com/kman2022/data/blob/main/main/berkley/IQ_study_process_small%20copy.png?raw=true'

st.set_page_config(page_title="Interconnection Dashboard",
                   page_icon=UC_IMAGE,
                   layout="wide")

# Customize the sidebar
src_markdown = """
**[Berkley Lab Reports](https://emp.lbl.gov/)**  
GitHub Repository: <https://github.com/kman2022/streamlit-multipage-template>
"""
ferc_markdown = """
**[Federal Energy Regulatory Commission (FERC)](https://www.ferc.gov/)**
"""

st.sidebar.title("About")

st.sidebar.info(src_markdown)
b_logo = "https://emp.lbl.gov/sites/all/files/logo.png"
st.sidebar.image(b_logo)

st.sidebar.info(ferc_markdown)
f_logo = "https://elibrary.ferc.gov/eLibrary/assets/img/FERC-banner.png"
st.sidebar.image(f_logo,width=75)

st.title("Berkley Labs Data")
st.markdown(
    """
    This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/giswqs/streamlit-multipage-template).
    """
)

st.image(PWR_IMAGE,width=350)
st.header("Instructions")
instructions = """
1. For the [GitHub repository](https://github.com/kman2022/streamlit-multipage-template), [data](https://github.com/kman2022/data/tree/main/main/berkley).
2. Each tab (upper left) represents a different report.
3. Scrapes have been built to interconnection queue data and this and other data can be added.
"""
st.markdown(instructions)
st.image(PROCESS_IMAGE,caption='Note: detailed steps (Interconnection Studies) were not included')

st.markdown('------')
st.header('[FERC 845](https://elibrary.ferc.gov/eLibrary/docinfo?accession_Number=20190221-3075)')
st.markdown('Order No. 845 (effective 2019 and applying to units > 20 MW) driven by developer complaints around lack of transparency and control over the interconnection process.')
st.markdown('[Provides](https://www.projectfinance.law/publications/2018/june/big-changes-in-how-new-power-projects-connect-to-the-grid/):')
st.subheader('1. 👷 Option to build')
st.markdown('- allows a project developer to take over design and construction of the intertie and any stand-alone network upgrades for a project irrespective of the grid operator or owner’s capabilities, provided there are **no conflicting** state or local prohibitions. This will allow developers to have more control over the timing and costs of interconnection.')
st.subheader('2. 🛣️ Frees up unused capacity')
st.markdown('- requires grid operators to permit a new project to use the **“surplus interconnection service”** for itself, an affiliate or for sale to a third party at the same interconnection point.')
st.subheader('3. ⚙️ Interconnection below capacity')
st.markdown('- allows new projects to request interconnection service at levels below total project capacity, especially helpful to renewable projects (mainly wind 🌬️ and storage  🔋 ).')
st.subheader('4. 🏁 Provisional interconnection')
st.markdown('- A project may be able to interconnect before the full interconnection process has been completed.')
st.subheader('5. 💡 Transparent models')
st.markdown('- directs each grid operator to maintain the following: **base power flow, short circuit ⚡ and stability databases**, including all underlying assumptions, and contingency list, [network models](https://www.pjm.com/library/reports-notices/rtep-documents.aspx) and underlying assumptions those used during the most recent interconnection study and representing current system conditions, and a list of all generation and [transmission projects](https://www.pjm.com/planning/project-construction).')
st.markdown('- [PJM](https://www.pjm.com/markets-and-operations/etools/planning-center) launched QueueScope (Dec-2022) to facilitate the assessment of grid impacts of proposed generation before submitting interconnection requests, but information is limited to line loading changes and does not include potential upgrade costs.')
st.subheader('6. 🚦 Contingent interties')
st.markdown('- the grid operator must divulge its method for identifying contingent facilities, and explain why each specific contingent facility was identified and how it will affect the new project seeking interconnection. This information must be provided at the close of the system impact study phase.')
st.markdown('- Upon request, the grid operator must also provide the project developer with an estimate of interconnection costs and in-service dates for each contingent facility, provided the information is readily available and not commercially sensitive. FERC declined to impose a standard method for identifying contingent facilities, declaring that “it is not clear a single method would apply across different queue types and footprints,” but it left open the possibility that harmonization may be appropriate.')
st.subheader('7. 🔋 Energy storage')
st.markdown('- FERC broadened how it defines “generating facility” to include a battery or other storage device. This should make interconnection easier for standalone storage facilities and also make it easier.')
st.subheader('8. 🔑 Technological changes')
st.markdown('- Grid operators assess proposed changes to pending interconnection requests to determine whether the changes are a “material modification,” meaning whether they would materially affect the cost or timing of projects later in the interconnection queue. If a proposed change is a material modification, then the project developer must either forgo the change or forfeit its queue position and start over.')
st.markdown('- Grid operators must also provide lists of “permissible technological advancements” that are not material modifications by definition.')
