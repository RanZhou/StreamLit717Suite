import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib_venn import venn2
from matplotlib_venn import venn2_unweighted

st.set_page_config(page_title="Magic on comparing your uploaded lists", page_icon="🌱")

def user_input_parse(usertxt):
    usertxt=usertxt.replace("\n"," ")
    usertxt=usertxt.replace(","," ")
    x = usertxt.split()
    return x


user_id_inputA = st.text_area('You can put your items in GroupA here',key="fA", value="A B C")
user_input_listA = user_input_parse(user_id_inputA)
user_setA = set(user_input_listA)
user_id_inputB = st.text_area('You can put your items in GroupB here',key="fB", value="B,C,D,E")
user_input_listB = user_input_parse(user_id_inputB)
user_setB = set(user_input_listB)

user_group = st.text_area('You can customize your group names in order here',key="fN", value="Science, Nature")
user_group_list = user_input_parse(user_group)

w_option = st.selectbox(
    'How would you like the Venn diagram to be plotted?',
    ('Unweighted', 'Weighted'))


# Use the venn2 function

fig, ax = plt.subplots()

if w_option == "Weighted":
    v=venn2(subsets = [user_setA, user_setB], set_labels = (str(user_group_list[0]), str(user_group_list[1])))
else:
    v=venn2_unweighted(subsets = [user_setA, user_setB], set_labels = (str(user_group_list[0]), str(user_group_list[1])))

col1, col2, col3 = st.columns(3)
with col1:
    colorA = st.color_picker('Pick a color for A', '#c94dac')
    v.get_patch_by_id('10').set_color(colorA)
with col2:
    colorB = st.color_picker('Pick a color for B', '#40438e')
    v.get_patch_by_id('01').set_color(colorB)
with col3:
    if v.get_patch_by_id('11') is not None:
        colorAB = st.color_picker('Pick a color for A&#8745;B', '#d8ae21')
        v.get_patch_by_id('11').set_color(colorAB)

st.pyplot(fig)

#calculate the actual set

def acquireID(user_setA, user_setB):
    spA = user_setA.difference(user_setB)
    spB = user_setB.difference(user_setA)
    ABshared = user_setA.intersection(user_setB)
    outlist = []
    for i in spA:
        outlist.append([i,'A'])
    for i in spB:
        outlist.append([i,'B'])
    for i in ABshared:
        outlist.append([i,'AB'])
    outpd = pd.DataFrame(outlist, columns=['input','tag'])
    return outpd

output_pddf = acquireID(user_setA, user_setB)
if st.button('Get list'):
    st.write('Below is the labeled inputs', output_pddf)

output_pddf.to_csv("venn2_rst.label.txt", sep='\t', index=False)

if os.path.exists("venn2_rst.label.txt"):
    with open("venn2_rst.label.txt", "rb") as file:
        btn = st.download_button(
                label="Download the list",
                data=file,
                file_name="venn2_rst.label.txt",
                mime="ll"
        )
