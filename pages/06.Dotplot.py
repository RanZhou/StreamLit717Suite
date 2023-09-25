# Draw a title and some text to the app:
'''
# Plotting cool dotplots
This is some _markdown_.
'''
import pandas as pd
import numpy as np
import streamlit as st
import subprocess
import random
import os
from PIL import Image

st.set_page_config(page_title="Create Dotplots 🌱", page_icon="🌱")

dbpath = 'db/lastzself'
gene_map = 'db/gv5.gene_line.bed'
plotter = 'scripts/dot_plotter.pl'

@st.cache_data
def load_gene(genemap_file):
    idmap_dict=dict()
    with open(genemap_file) as file:
        for line in file:
            lsstr=line.rstrip().split()
            idmap_dict[lsstr[1]]=lsstr[0]+"_"+str(lsstr[2])+"_"+str(lsstr[3])
        return idmap_dict

#Loading gene bed file for coordinates

gene_bed=load_gene(gene_map)

# default parameters for plotting
w_chrID = "T02"
w_start = 1
w_end = 10000

def id2coordinate(geneID):
    str_input = gene_bed[geneID]
    str_chunks = str_input.split("_")
    return str_chunks[0], int(str_chunks[1]), int(str_chunks[2])



user_simple_input = st.text_input('You can type a geneID or chr&#58;from\-to formatted interval', 'PtXaTreH.10G046700', 
                                  help = 'Both geneID PtXaTreH.01G000200 & and a formatted interval T02:5000-6000 would work')
user_input_type ='ID'

if ":" in user_simple_input:
    st.write('You typed an interval ', user_simple_input)
    user_input_type ='ITV'
else:
    st.write('You typed a geneID ', user_simple_input)

if user_input_type == "ID":
    if user_simple_input in gene_bed.keys():
        array_coord = id2coordinate(user_simple_input)
        w_chrID = array_coord[0]
        w_start = array_coord[1]
        w_end = array_coord[2]
        st.write('Your geneID is valid, which was found on Chr:',array_coord[0], ' from:', array_coord[1], ' to:', array_coord[2])
    else:
         st.write('We could not find your geneID, please check your input')

if user_input_type == "ITV":
    user_simple_input = user_simple_input.replace(":"," ")
    user_simple_input = user_simple_input.replace("-"," ")
    array_coord = user_simple_input.split()
    w_chrID = array_coord[0]
    w_start = int(array_coord[1])
    w_end = int(array_coord[2])
    if w_chrID.startswith("A") or w_chrID.startswith("T"):
        if w_end - w_start >0 and w_end - w_start<200000:
            st.write('Your geneID is valid, which was found on Chr:',array_coord[0], ' from:', array_coord[1], ' to:', array_coord[2])



flanking_size = st.number_input('🔢Type in the :red[**flanking size**] you want to include here', min_value = 0, max_value=500000, value=100000, step =1)
st.write('The flanking size is ', flanking_size)

interval_size = abs(w_end - w_start)

user_tick_num = st.number_input('🔢Type in the ticks control number', min_value = 1000, max_value=10000, value=10000, step =1000)
st.write('The ticks control number is ', user_tick_num)
#user_tick_num = 10000
canvas_size = st.number_input('How large will your image be', min_value = 600, max_value=3600, value=800, step =100)
st.write('The x-axis and y-axis of your image will be ', canvas_size ,"pixels")

tick_density = int(interval_size/user_tick_num)

@st.cache_data
def load_gff(gff, read_mode):
    idmap_dict=dict()
    with open(idmap) as file:
        for line in file:
            lsstr=line.rstrip().split()
            idmap_dict[lsstr[1]]=lsstr[0]
            idmap_dict[lsstr[0]]=lsstr[1]
        return idmap_dict



# lastz file naming : lastz.g717v5.h2_self.Chr12.dat.gz
# Plotter usage: 
# perl ~/script/plot.pl lastz_file start end svg_output tick_length 

if not os.path.exists("user_media"):
    os.mkdir("user_media")
svg_out = "./user_media/user.svg"

def plot(chr, start, end, tick_len, canvas_size , flanking_size):
    #fetching file name:
    chr = chr.replace("T","h1_self.Chr")
    chr = chr.replace("A","h2_self.Chr")
    st.write(chr)
    lastz_file_name = "lastz.g717v5."+chr+".dat.gz"
    lastz_file = os.path.join(dbpath,lastz_file_name)
    plot_cmd =  f'perl scripts/dot_plotter.pl {canvas_size} {lastz_file} ' \
                f' {start} {end} {svg_out} {tick_len} {flanking_size}'
    subprocess.call(plot_cmd, shell=True)
    st.write("Running plotter as:")
    st.write(str(plot_cmd))

if st.button('Plotting'):
    plot_start = w_start - flanking_size
    if plot_start < 0 :
        plot_start =1
    plot_end = w_end + flanking_size
    plot(w_chrID, plot_start, plot_end, user_tick_num, canvas_size, flanking_size)
    st.image(svg_out, caption='Your dotplot', width=canvas_size)
    if os.path.exists(svg_out):
        with open(svg_out, "rb") as file:
            btn = st.download_button(
                    label="Download your plot",
                    data=file,
                    file_name="user.svg",
                    mime="svg"
            )

st.write("Before you leave, please notice that the plot is from a prepared dataset, which means it could be different from the fact!")
st.write("To remove the trivial noise, identity lower than 70% were not shown!")
st.write("Warmer the color, higher the identity! (Upper part)")
st.write("Red is direct duplication, blue is inverted duplication (Lower part)")
st.write("This is a tool developed and maintained by Ran Zhou!")