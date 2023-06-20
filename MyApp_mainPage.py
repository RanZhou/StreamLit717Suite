# Draw a title and some text to the app:
'''
# This is the document title

This is some _markdown_.
'''

import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Poplar App Kits",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.aspendb.org/help',
        'Report a bug': "https://www.aspendb.org/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

image = Image.open('./webmedia/LabLogo.png')

st.image(image, caption='Sunrise by the mountains')

st.write("# Welcome to the TsaiLab's Poplar App Kits! 🌳")

st.sidebar.success("Select a task you want to do today.")

st.markdown(
    """
    ## Avaiable tools
    ###### Demultiplexing reads
    ###### Merging R1 and R2 reads from amplicon sequencing
    ###### Converting v4 geneIDs to Official geneIDs of the 717 gene models
    More tools are on the way!
    If you think these tools are helpful, great!
    For all questions and suggestions, please contact the admins: \
    [Ran.Zhou](mailto:ran.zhou@uga.edu), \
    [Chen Hsieh](mailto:chen.hsieh@uga.edu), \
    [CJ Tsai](mailto:cjtsai@uga.edu) ! 👋")
    """
)