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

edited_df.to_csv("my_input.txt", sep='\t', index=False)
if os.path.exists("my_input.txt"):
    with open("my_input.txt", "rb") as file:
        btn = st.download_button(
                label="Download the list",
                data=file,
                file_name="my_input.txt",
                mime="ll"
        )


user_seq1_file = st.file_uploader('Upload my input from a file', key="R1",type = ['txt'], help="Must be formatted", accept_multiple_files = False)
if user_seq1_file is not None:
    st.write("filename:", user_seq1_file.name)
    save_uploadedfile(user_seq1_file,"./tempDir")
    useq_file1 = os.path.join(path,user_seq1_file.name)
    subprocess.call(f'mv {useq_file1} ./tempDir/user_go.bubbleinput.txt', shell=True)




def run_bubble(user_input, outputname, w, h):
    R_cmd = f'Rscript ./scripts/GObubble.R {user_input} {outputname} {w} {h} >Go.log'
    st.write("Running GO plotter as:")
    st.write(str(R_cmd))
    subprocess.call(R_cmd, shell=True)


outplot = './tempDir/user_GObubble_plot.svg'

canvas_w=st.slider('Canvas width', 8, 16, 1)
canvas_h=st.slider('Canvas height', 8, 16, 1)

if st.button('Plotting'):
    run_bubble("./tempDir/user_go.bubbleinput.txt",outplot,canvas_w,canvas_h)


if os.path.exists(outplot):
    st.image(outplot, caption='Your dotplot', width=800)
    with open(outplot, "rb") as file:
        btn = st.download_button(
                label="Download your plot",
                data=file,
                file_name="user_GO.svg",
                mime="svg"
        )