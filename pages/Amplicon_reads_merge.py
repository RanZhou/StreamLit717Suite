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
user_seq1_file = st.file_uploader('Please upload your R1 reads file here  🧬', key="R1",type = ['gz', 'fq','fastq','fasta'], 
                                  help="compressed files like fastq.gz and fq.gz are supported", accept_multiple_files = True)

upload_R1_file_list = []
sample_file_r1_map = dict()

for uploaded_file in user_seq1_file:
    bytes_data = uploaded_file.read()
    upload_R1_file_list.append(uploaded_file.name)
    r1fileIDsep = uploaded_file.name.split("_")
    sampleID = r1fileIDsep[0]+"_"+r1fileIDsep[1]
    sample_file_r1_map[sampleID] = uploaded_file
    st.write("filename:", uploaded_file.name ,"Uploaded")


user_seq2_file = st.file_uploader('Please upload your R2 reads here file 🧬',key="R2", 
                                  type = ['gz', 'fq','fastq','fasta'], 
                                  help="compressed files like fastq.gz and fq.gz are supported", accept_multiple_files = True)
upload_R2_file_list = []
sample_file_r2_map = dict()
for uploaded_file in user_seq2_file:
    bytes_data = uploaded_file.read()
    upload_R2_file_list.append(uploaded_file.name)
    r1fileIDsep = uploaded_file.name.split("_")
    sampleID = r1fileIDsep[0]+"_"+r1fileIDsep[1]
    sample_file_r2_map[sampleID]= uploaded_file
    st.write("filename:", uploaded_file.name ,"Uploaded")

## Check uploaded files, the R1 and R2 should contain the same amount of files ##

r1uplen = len(upload_R1_file_list)
r2uplen = len(upload_R2_file_list)

if r1uplen == r2uplen :
    st.write("You uploaded "+str(r1uplen)+" in both and R1 and R2 slots successfully!")
else :
    st.write("Warning! File numbers are different between R1 and R2, please check your uploads and make sure R1 and R2 have the same amount of files uploaded!")

#parsing files uploaded into sample info list
sample_list = []
for r1file in upload_R1_file_list:
    r1fileIDsep = r1file.split("_")
    sampleID = r1fileIDsep[0]+"_"+r1fileIDsep[1]
    sample_list.append(sampleID)

#running mode#
user_run_mode_choice = st.radio(
        "Select the way how you want to run 👉",
        key="mode_choice",
        options=["All","Only a subset of files by manually selecting"],
        help = "All your files will be processed by default!"
        )

user_lable_vis1 = "collapsed"
user_customized_samplelist=st.multiselect(
                                        'Select the samples you want to run',
                                        options = sample_list,
                                        label_visibility = user_lable_vis1)
if user_run_mode_choice != "All" :
    user_lable_vis1 = "visible"
if user_run_mode_choice == "All" :
    user_lable_vis1 = "collapsed"

st.write('You selected:', user_customized_samplelist)

##Set up parameters##
user_algorithm_choice = st.radio(
        "Select which algorithm you want to use 👉",
        key="ALG_choice",
        options=["simple_bayesian (Masella 2012)", "ea_util (Aronesty 2013)", "flash (Magoc 2011)", "pear (Zhang 2013)", "rdp_mle (Cole 2013)", "stitch developed by Austin Richardson","uparse (UPARSE/USEARCH (Edgar 2013))"],
        )
st.write("This option is under construction currently!")

user_kmer = st.slider('Maximum error rate', min_value=1, max_value=10, step=1, value=1, format="%d" )
st.write("This should be small (no more than 10; the default is 2), and you chose", user_kmer, "Only increase this when your sequences are repetitive")

def save_uploadedfile(uploadedfile,path):
     with open(os.path.join(path,uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved File:{} to path".format(uploadedfile.name))

def exec_cuta(forwardfastqinput,reversefastqinput,logfile,unmergedoutfile,outfile, outpath):
    rst_dir = os.path.join(outpath,"merged")
    if not os.path.exists(rst_dir):
        os.mkdir(rst_dir)
    if not os.path.exists(os.path.join(outpath,"unmerged")):
        os.mkdir(os.path.join(outpath,"unmerged"))
    if not os.path.exists(os.path.join(outpath,"log")):   
        os.mkdir(os.path.join(outpath,"log"))
    panda_cmd = f'pandaseq -f {forwardfastqinput} ' \
                f' -r {reversefastqinput}' \
                f' -g {outpath}/log/{logfile}' \
                f' -U {outpath}/unmerged/{unmergedoutfile}' \
                f' -w {outpath}/merged/{outfile}' \
                f' >> {outpath}/log/runtime.log'
    st.write("Running pandaseq as:")
    st.write(str(panda_cmd))
    subprocess.call(panda_cmd, shell=True)
    subprocess.call(f'mv {outpath}/runtime.log {outpath}/merged', shell=True)

outfilename=''

passdownlist = sample_list
if user_run_mode_choice != "All" :
    passdownlist = user_customized_samplelist

if st.button('Merge'):
    sysdatetime = datetime.now()
    dt_string = sysdatetime.strftime("%Y%m%d_%H_%M_%S")
    ransuffix = str(random.randint(1, 100))
    path="./panda_run/"+dt_string+"_"+ransuffix
    if not os.path.exists("./panda_run/"):   
        os.mkdir("./panda_run/")
    os.makedirs(path)
    #outfile1 = path+"/merged/"+"{name1}-{name2}.1.fastq.gz" 
    #outfile2 = path+"/merged/"+"{name1}-{name2}.2.fastq.gz"
    for each_sample in passdownlist:
        file_R1 = sample_file_r1_map[each_sample]
        file_R2 = sample_file_r2_map[each_sample]
        save_uploadedfile(file_R1,path)
        save_uploadedfile(file_R2,path)
        useq_file1 = os.path.join(path,file_R1.name)
        useq_file2 = os.path.join(path,file_R2.name)
        logfile = each_sample+".log"
        mergedout = each_sample+"_merged"+".fastq.gz"
        unmergedout = each_sample+"_unmerged"+".fastq.gz"
        exec_cuta(useq_file1,
                useq_file2,
                logfile,
                unmergedout,
                mergedout,
                path)
        st.write("processing:", str(each_sample))
    st.write("Complete!")
    outgzip_name="panda_rst_"+dt_string+".tar.gz"
    outfilename = outgzip_name
    zip_cmd = f'tar -zcvf {outgzip_name} {path}/merged {path}/unmerged {path}/log'
    subprocess.call(zip_cmd, shell=True)


if os.path.exists(outfilename):
    with open(outfilename, "rb") as file:
        btn = st.download_button(
                label="Download your results with one click",
                data=file,
                file_name=outgzip_name,
                mime="gz"
        )

st.write("This is only a wrapper for pandaseq. For citation please use [the pandaseq publication here](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-13-31)")

#Running example
#pandaseq -f April6thLibrary_R1_001.fastq.gz -r April6thLibrary_R2_001.fastq.gz -F \
#	-g ./April6thLibrary_pandaseq_log -u ./unmerged/April6thLibrary_unmerged.fastq > ./merged/April6thLibrary_panda_merged.fastq
