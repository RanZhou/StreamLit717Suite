import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="GeneID converter Demo 🌱", page_icon="🌱")

idmap='db/h1h2gv5.id.map'

user_suffix_flag = st.radio(
        "Select how do you want to proceed with suffix if your ID contains 👉",
        key="suffix",
        options=["Ignore suffix", "Keep suffix", "I don't know"],
        )

@st.cache_data
def load_map(idmap):
    idmap_dict=dict()
    with open(idmap) as file:
        for line in file:
            lsstr=line.rstrip().split()
            idmap_dict[lsstr[1]]=lsstr[0]
            idmap_dict[lsstr[0]]=lsstr[1]
        return idmap_dict

def user_input_parse(usertxt):
    usertxt=usertxt.replace("\n"," ")
    usertxt=usertxt.replace(","," ")
    x = usertxt.split()
    return x

def id_convert(parsed_userinput,IDmap):
    outlist = [];
    for i in parsed_userinput:
        try:
            if "." in i :
                idbyparts = i.split(".")
            newid = IDmap[i]
            outlist.append([i,newid])
        except:
            print("An exception occurred")
    outpd = pd.DataFrame(outlist, columns=['inputID','NewID'])
    return outpd

user_id_input = st.text_area('You can put the IDs from v4 here: e.g. Ptrev51000006m PoHAPv41023350m, both tab or comma separated format, or even a list is supported')
IDmap = load_map(idmap)

if st.button('Convert'):
    converted_id = user_input_parse(user_id_input)
    output_pddf = id_convert(converted_id,IDmap)
    st.write('Below is the converted IDs', output_pddf)
