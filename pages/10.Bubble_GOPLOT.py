import streamlit as st
import pandas as pd
import os
import subprocess
from PIL import Image

st.set_page_config(page_title="GO plot", page_icon="")

st.write("GO plot with ggplot2")

def save_uploadedfile(uploadedfile,path):
     with open(os.path.join(path,uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved File:{} to path".format(uploadedfile.name))

df = pd.DataFrame(
    [
        {"COND": "summer", "GO_term": "cell-cell signaling",  "GO.ID": "(GO:0007267)", "Annotated": 138,
         "Gene_number": 4, "Expected": 0.65, "classic": 0.0043, "Fold": 1.62, "logP": 0.9187},
         {"COND": "opposite", "GO_term": "cell-cell signaling",  "GO.ID": "(GO:0007267)", "Annotated": 138,
         "Gene_number": 8, "Expected": 4.92, "classic": 0.12057, "Fold": 6.153846, "logP": 0.9187},
    ]
)


edited_df = st.data_editor(df,num_rows="dynamic", hide_index=True) # 👈 An editable dataframe

if st.button('Save my input'):
    edited_df.to_csv("./tempDir/user_go.bubbleinput.txt", sep='\t', index=False)
    st.write('Dataframe has been written into a file successfully')


def run_bubble(user_input, outputname):
    R_cmd = f'Rscript ./scripts/GObubble.R {user_input} {outputname} >Go.log'
    st.write("Running GO plotter as:")
    st.write(str(R_cmd))
    subprocess.call(R_cmd, shell=True)


outplot = './tempDir/user_GObubble_plot.svg'

canvas_size=st.slider('Canvas size', 600, 1200, 100)
run_bubble("./tempDir/user_go.bubbleinput.txt",outplot)
st.image(outplot, caption='Your dotplot', width=canvas_size)

if os.path.exists(outplot):
    with open(outplot, "rb") as file:
        btn = st.download_button(
                label="Download your plot",
                data=file,
                file_name="user_GO.svg",
                mime="svg"
        )