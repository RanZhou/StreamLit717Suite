import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib_venn as mv

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

user_id_inputC = st.text_area('You can put your items in GroupC here',key="fC", value="C,2,5,71")
user_input_listC = user_input_parse(user_id_inputC)
user_setC = set(user_input_listC)


user_group = st.text_area('You can customize your group names in order here',key="fN", value="NIH, NSF, DOE")
user_group_list = user_input_parse(user_group)

w_option = st.selectbox(
    'How would you like the Venn diagram to be plotted?',
    ('Unweighted', 'Weighted'))

# Use the venn3 function

fig, ax = plt.subplots()

if w_option == "Weighted":
    v=mv.venn3(subsets = [user_setA, user_setB, user_setC], set_labels = (str(user_group_list[0]), str(user_group_list[1]), str(user_group_list[2])))
else:
    v=mv.venn3_unweighted(subsets = [user_setA, user_setB, user_setC], set_labels = (str(user_group_list[0]), str(user_group_list[1]), str(user_group_list[2])))

col1, col2, col3 = st.columns(3)

with col1:
    colorA = st.color_picker('Pick a color for A', '#c94dac')
    v.get_patch_by_id('100').set_color(colorA)
with col2:
    colorB = st.color_picker('Pick a color for B', '#40438e')
    v.get_patch_by_id('010').set_color(colorB)
with col3:
    colorC = st.color_picker('Pick a color for C', '#130dce')
    v.get_patch_by_id('001').set_color(colorC)
with col1:
    if v.get_patch_by_id('111') is not None:
        colorAB = st.color_picker('Pick a color for A&#8745;B&#8745;C', '#d8ae21')
        v.get_patch_by_id('111').set_color(colorAB)
with col2:       
    if v.get_patch_by_id('110') is not None:
        colorAB = st.color_picker('Pick a color for A&#8745;B&#8745;&#172;C', '#10ad2f')
        v.get_patch_by_id('110').set_color(colorAB)
with col3:
    if v.get_patch_by_id('101') is not None:
        colorAB = st.color_picker('Pick a color for A&#8745;C&#8745;&#172;B', '#eeaaff')
        v.get_patch_by_id('101').set_color(colorAB)
if v.get_patch_by_id('011') is not None:
    colorAB = st.color_picker('Pick a color for B&#8745;C&#8745;&#172;A', '#11ff55')
    v.get_patch_by_id('011').set_color(colorAB)

st.pyplot(fig)

#calculate the actual set

def acquireID(user_setA, user_setB, user_setC):
    sp10X = user_setA.difference(user_setB)
    sp100 = sp10X.difference(user_setC)
    sp101 = sp10X.intersection(user_setC)
    
    sp01X = user_setB.difference(user_setA)
    sp010 = sp01X.difference(user_setC)
    sp011 = sp01X.intersection(user_setC)

    spX10 = user_setB.difference(user_setC)
    sp110 = spX10.intersection(user_setA)

    sp11X = user_setA.intersection(user_setB)
    sp111 = sp11X.intersection(user_setC)

    spX01 = user_setC.difference(user_setB)
    sp001 = spX01.difference(user_setA)
    outlist = []
    for i in sp100:
        outlist.append([i,'100'])
    for i in sp010:
        outlist.append([i,'010'])
    for i in sp001:
        outlist.append([i,'001'])
    for i in sp110:
        outlist.append([i,'110'])
    for i in sp101:
        outlist.append([i,'101'])
    for i in sp011:
        outlist.append([i,'011'])
    for i in sp111:
        outlist.append([i,'111'])

    outpd = pd.DataFrame(outlist, columns=['input','tag'])
    return outpd

output_pddf = acquireID(user_setA, user_setB, user_setC)
if st.button('Get list'):
    st.write('Below is the labeled inputs', output_pddf)

output_pddf.to_csv("venn3_rst.label.txt", sep='\t', index=False)

if os.path.exists("venn3_rst.label.txt"):
    with open("venn3_rst.label.txt", "rb") as file:
        btn = st.download_button(
                label="Download the list",
                data=file,
                file_name="venn3_rst.label.txt",
                mime="ll"
        )
