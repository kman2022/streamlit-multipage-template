import streamlit as st
import leafmap.foliumap as leafmap

LOC_PATH = '/Users/kristian.lande@leveltenenergy.com/Documents/GitHub/streamlit-geospatial/data/'
UC_IMAGE = 'berkley_logo.png'
PWR_IMAGE = 'power_pic.jpeg'

st.set_page_config(page_title="PJM Interconnection Dashboard",
                   page_icon=LOC_PATH+UC_IMAGE,
                   layout="wide")

# Customize the sidebar
src_markdown = """
**[Berkley Lab Reports](https://emp.lbl.gov/)**  
GitHub Repository: <https://github.com/kman2022/streamlit-multipage-template>
"""
src_analysis = """
    **Source:** Berkley Lab Queued Up v2: Extended Analysis on Power Plants Seeking Transmission InterconnectionAs of the End of 2021. Joseph Rand, Will Gorman, Dev Millstein, Andrew Mills, Joachim Seel, Ryan Wiser Lawrence Berkeley National Laboratory February 2022.  <https://emp.lbl.gov/publications/queued-characteristics-power-plants>
"""

st.sidebar.info(src_analysis)
st.sidebar.title("About")
st.sidebar.info(src_markdown)
logo = "https://emp.lbl.gov/sites/all/files/logo.png"
st.sidebar.image(logo)

# Customize page title
st.title("Queued Up  ⚡ ")

st.markdown(
    """
    This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/giswqs/streamlit-multipage-template).
    """
)
st.image(LOC_PATH+PWR_IMAGE,width=350)

st.header("Instructions")

markdown = """
1. For the [GitHub repository](https://github.com/giswqs/streamlit-multipage-template) or [use it as a template](https://github.com/giswqs/streamlit-multipage-template/generate) for your own project.
2. Customize the sidebar by changing the sidebar text and logo in each Python files.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.

"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
