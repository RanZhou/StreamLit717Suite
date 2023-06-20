# Draw a title and some text to the app:
'''
# This is the document title

This is some _markdown_.
'''
import pandas as pd
import numpy as np
import streamlit as st
import subprocess
import random
import os
from datetime import datetime

# Handling files uploaded for user
user_seq1_file = st.file_uploader('Please upload your R1 reads file here🧬', key="R1",type = ['gz', 'fq','fastq','fasta'], help="compressed files like fastq.gz and fq.gz are supported", accept_multiple_files = False)
if user_seq1_file is not None:
    st.write("filename:", user_seq1_file.name)


user_seq2_file = st.file_uploader('Please upload your R2 reads file here🧬',key="R2", type = ['gz', 'fq','fastq','fasta'], help="compressed files like fastq.gz and fq.gz are supported", accept_multiple_files = False)
if user_seq2_file is not None:
    st.write("filename:", user_seq2_file.name)


UAF_vis = "visible"
user_adapteraction_flag = st.radio(
        "Select what you want to do with the adapter sequences in the reads 👉",
        key="AdapterAction",
        options=["trim", "none", "mask","lowercase"],label_visibility= UAF_vis
        )

# -e Maximum error rate (default: 0.1)

UMEF_vis = "visible"
user_max_err_rate = st.slider('Maximum error rate', min_value=0.0, max_value=0.5, step=0.01, value=0.1, format="%f" , label_visibility = UMEF_vis )
st.write("Maximum error rate is set to", user_max_err_rate, "The suggested/default value is 0.1")

user_indel_cc = st.checkbox("Disallow Indels! This should always be true and checked, unless you are messing around 😈", value=True)

user_fprimer_file = st.file_uploader('Please upload your forward barcode files here file 🧬: (only :red[**fasta**] format is accepted)', accept_multiple_files = False)
if user_fprimer_file is not None:
    st.write("filename:", user_fprimer_file.name)
user_rprimer_file = st.file_uploader('Please upload your reverse barcode files here file 🧬: (only :red[**fasta**] format is accepted)', accept_multiple_files = False)
if user_rprimer_file is not None:
    st.write("filename:", user_rprimer_file.name)

def save_uploadedfile(uploadedfile,path):
     with open(os.path.join(path,uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved File:{} to path".format(uploadedfile.name))

def exec_cuta(user_max_err_rate,fprimerfile,rprimerfile,outfile1,outfile2,IN_R1,IN_R2,outpath,uaf):
    rst_dir = os.path.join(outpath,"demultiplexed")
    os.mkdir(rst_dir)
    cuta_cmd = f'cutadapt -e {user_max_err_rate} --no-indels action={uaf}' \
                   f' -g file:{fprimerfile}' \
                   f' -G file:{rprimerfile}' \
                   f' -o {outfile1}' \
                   f' -p {outfile2}' \
                   f' {IN_R1}' \
                   f' {IN_R2}' \
                   f' > {outpath}/runtime.log'
    st.write("Running cutadapt as:")
    st.write(str(cuta_cmd))
    subprocess.call(cuta_cmd, shell=True)
    subprocess.call(f'mv {outpath}/runtime.log {outpath}/demultiplexed', shell=True)

outfilename=''

if st.button('Demultiplex'):
    sysdatetime = datetime.now()
    dt_string = sysdatetime.strftime("%Y%m%d_%H_%M_%S")
    ransuffix = str(random.randint(1, 100))
    path="./"+dt_string+"_"+ransuffix
    os.mkdir(path)
    outfile1 = path+"/demultiplexed/"+"{name1}-{name2}.1.fastq.gz" 
    outfile2 = path+"/demultiplexed/"+"{name1}-{name2}.2.fastq.gz"
    save_uploadedfile(user_seq1_file,path)
    save_uploadedfile(user_seq2_file,path)
    save_uploadedfile(user_fprimer_file,path)
    save_uploadedfile(user_rprimer_file,path)
    useq_file1 = os.path.join(path,user_seq1_file.name)
    useq_file2 = os.path.join(path,user_seq2_file.name)
    ubar_file1 = os.path.join(path,user_fprimer_file.name)
    ubar_file2 = os.path.join(path,user_rprimer_file.name)
    exec_cuta(user_max_err_rate,ubar_file1,ubar_file2,outfile1,outfile2,useq_file1,useq_file2,path,user_adapteraction_flag)
    outgzip_name="rst_"+dt_string+".tar.gz"
    outfilename = outgzip_name
    zip_cmd = f'tar -zcvf {outgzip_name} {path}/demultiplexed'
    subprocess.call(zip_cmd, shell=True)


if os.path.exists(outfilename):
    with open(outfilename, "rb") as file:
        btn = st.download_button(
                label="Download your results",
                data=file,
                file_name=outgzip_name,
                mime="gz"
        )

st.write("This is only a wrapper for demuplexing function of Cutadapt, not a complete Cutadapt. For citation please use [link](https://cutadapt.readthedocs.io/en/stable/index.html) to the Cutadapt")
#Cutadapt parameters:
# -e Maximum error rate (default: 0.1)
# --no-indels always true for this purpose
# --action=trim is the default
# Use --action=none to not change the read even if there is a match. 
# Use --action=mask to write N characters to those parts of the read that would otherwise have been removed.
# Use --action=lowercase to change to lowercase those parts of the read that would otherwise have been removed. The rest is converted to uppercase.

#Running example
#cutadapt \
#    -e 0.1 --no-indels  \
#    -g file:f.primer.s.fa \
#    -G file:r.primer.s.fa \
#    -o ./rst_combinatorial_trimmed/{name1}-{name2}.1.fastq.gz -p ./rst_combinatorial_trimmed/{name1}-{name2}.2.fastq.gz \
#    F_R1_001.fastq.gz F_R2_001.fastq.gz
# --json=filename.cutadapt.json
