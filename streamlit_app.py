import streamlit as st

UC_IMAGE = 'https://github.com/kman2022/data/blob/main/main/berkley/berkley_logo.png'
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

st.sidebar.title("About")
st.sidebar.info(src_markdown)
logo = "https://emp.lbl.gov/sites/all/files/logo.png"
st.sidebar.image(logo)

# Customize page title
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
2. Each tab represents a different Berkley Labs report.
3. Scrapes have been built to interconnection queue data and this and other data can be added to this application.
4. The interconnection queue process follows a simplified process.
5. Data for the detailed steps (Interconnection Studies) are not included in the saource data.
6. Not all regions report interconnection agreement dates and official online dates. The proposed online dates are used as a proxy for COD but the data quality may be poor as the information is often an estimation provided by the developer.
"""

st.markdown(instructions)
st.image(PROCESS_IMAGE)