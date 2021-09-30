#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os
import subprocess
import sys
import pandas as pd
import sys


# In[2]:


bam_file_directory = sys.argv[1] #'/Users/irffanalahi/Research/Research_update/in-silico/gt/PBL_TIL_MEL/mixture_output_melcfdlike'#sys.argv[1]
mix_input_file = sys.argv[2] #'/Users/irffanalahi/Research/Research_update/in-silico/gt/PBL_TIL_MEL/TIL.txt'#sys.argv[2]
df_mix=pd.read_csv(mix_input_file,sep="\t") #############irf######
outfile=bam_file_directory+".txt"
fol = bam_file_directory + '_out1'
os.mkdir(fol)


# In[3]:


bam_file_list = [f for f in os.listdir(bam_file_directory) if f.endswith('.bam')]
bam_file_list = [bam_file_directory+'/'+bam_file_list[i] for i in range(len(bam_file_list))]


# In[4]:


cell_type_list = list(df_mix.columns)
df_summ = pd.DataFrame(columns = cell_type_list)
for bf in bam_file_list:
    #print(bf)
    file = bf.split('/')[-1]
    file = file.split('.bam')[0]
    bash_command = 'samtools view '+bf+' | cut -f 1 > '+fol+'/temp_'+file+'.txt'
    subprocess.call(bash_command,shell=True)
    with open(fol + '/temp_' + str(file) + '.txt') as f:
        read_names = f.read()
    read_names = np.array(read_names.splitlines())
    read_ct = np.array([c.split('.')[0] for c in read_names])
    ct_count = []
    for ct in cell_type_list:
        ct_count.append(sum(read_ct==ct))
    df_summ.loc[bf.split('/')[-1].replace('.bam','')] = ct_count
    
# For every bam file, we want a separate temp.txt
# Each read should be twice


# In[5]:


df_summ


# In[6]:


df_summ_norm = df_summ.div(0.01*df_summ.sum(axis=1),axis=0)


# In[7]:


df_summ_norm['Index Number'] = [int(i.split('insilmix')[-1]) for i in df_summ_norm.index]


# In[8]:


df_summ_norm.sort_values(['Index Number'], inplace=True)
df_summ_norm = df_summ_norm.drop('Index Number', axis=1)

df_summ_norm


# In[9]:


df_mix
# For each cell type, three lines 
# 1. Target (df_mix)
# 2. Previous method
# 3. Current method
# Summary: median


# In[10]:


df_summ


# In[11]:


df_summ_norm.to_csv(outfile, sep='\t')


# In[ ]:




