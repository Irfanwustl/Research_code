#!/usr/bin/env python
# coding: utf-8

# In[1]:


###if multiple build, exit


import yaml
import pandas as pd
import glob
import sys
import os


# In[2]:


model_info_file=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/support/MGI_automation/After_MGI_RUN/toydata/filelist.txt'


destinationfolder=sys.argv[2] #'/Users/irffanalahi/Research/Research_code/support/MGI_automation/After_MGI_RUN/toydata/destination'
destinationfolder_bam=destinationfolder+"_bam"
destinationfolder_commands=destinationfolder+"_commands"

os.mkdir(destinationfolder)
os.mkdir(destinationfolder_bam)
os.mkdir(destinationfolder_commands)




gmspath='/storage1/fs1/aadel/Active/gmsroot/model_data'

model_info_df=pd.read_csv(model_info_file,sep='\t',header=None)

model_info_list=model_info_df[0].tolist()
model_info_list


# In[3]:



copycommands=[]
cramtobamcommands=[]

for onemodel in model_info_list:
    build=glob.glob(gmspath+"/"+onemodel+'/build*')

    cramflag=0
    for abuild in build:
        acram=glob.glob(gmspath+'/'+onemodel+'/'+os.path.basename(abuild)+'/results/*cram')
        if len(acram)==1:
            build=abuild
            cramflag=1
            break
        '''
        print("Failed Build")
        print(onemodel)
        print(abuild)
        '''

    if cramflag==0:
        print(onemodel)

        print("not found successful BULD.EXITING")
        sys.exit(1)
 
    
    with open(gmspath+"/"+onemodel+"/"+os.path.basename(build)+'/inputs.yaml', 'r') as file:
        yamlinfo = yaml.safe_load(file)
        samplename=yamlinfo['sample_name']
    
    copycommand="bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo "+destinationfolder_commands+"/"+samplename+"_copy.log" + "  -q general -a 'docker(irfanwustl/insilico_mix)'  cp -r "+gmspath+"/"+onemodel+' '+destinationfolder+"/"+samplename+"\n"
    
    
    
    copycommands.append(copycommand)
    
    
    cramtobamcommand="bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo "+destinationfolder_commands+"/"+samplename+"_cramtobam.log" + "  -q general -a 'docker(irfanwustl/insilico_mix)'"+ " samtools view -b -T /storage1/fs1/aadel/Active/work/Hg38Reference/all_sequences.fa -o "+destinationfolder_bam+"/"+samplename+".final.bam  "+gmspath+"/"+onemodel+"/"+os.path.basename(build)+"/results/final.cram  \n"

    cramtobamcommands.append(cramtobamcommand)


# In[4]:


with open(destinationfolder_commands+"/copy_commands.sh", 'w') as f:
    for item in copycommands:
        f.write("%s" % item)


# In[5]:


with open(destinationfolder_commands+"/cramtobam_commands.sh", 'w') as f:
    for item in cramtobamcommands:
        f.write("%s" % item)

