#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import background_calculation
import sys


# In[2]:



infol = sys.argv[1]  #'/Users/irffanalahi/Research/Research_update/in-silico/Rdresult/corrmNeuallrange/v4_1000000/5g/studyFPR/BL14_atleast.2_top-1_singleCpG_final_assignedref_uniq.txt_result_final.txt_folder'
gtfile=sys.argv[2]  #'/Users/irffanalahi/Research/Research_update/in-silico/Rdresult/corrmNeuallrange/v4_1000000/5g/studyFPR/mixture_output_1000000.txt'  #mixture_output_81205allrange_nozero.txt
gtdf=pd.read_csv(gtfile,sep="\t")
celltype='mNeu'
gtdf=gtdf[['Mixture',celltype+"_real"]]

infiles = os.listdir(infol)

if '.DS_Store' in infiles:
    infiles.remove('.DS_Store')
    
if '.ipynb_checkpoints' in infiles:
    infiles.remove('.ipynb_checkpoints')


# In[3]:


outdflist=[]


for name in infiles:
    file = infol + '/' + name
    new_df = background_calculation.decode_files(file,celltype)
    outdflist.append(new_df)
out_df = pd.concat(outdflist, axis=0)


# In[4]:


out_df['false_neg/all_pos']=out_df['rejectedfalseCTcount'].astype('float64')/(out_df['acceptedtrueCTcount'].astype('float64')+out_df['rejectedfalseCTcount'].astype('float64'))
out_df['false_neg/all_pos'] = out_df['false_neg/all_pos'].fillna(-1)

out_df['false_pos/all_neg']=out_df['acceptedfalseCTcount'].astype('float64')/(out_df['acceptedfalseCTcount'].astype('float64')+out_df['rejectedtrueCTcount'].astype('float64'))
out_df['false_pos/all_neg'] = out_df['false_pos/all_neg'].fillna(-1)

out_df['F1-score']=out_df['acceptedtrueCTcount']/(out_df['acceptedtrueCTcount']+0.5*(out_df['acceptedfalseCTcount']+out_df['rejectedfalseCTcount']))

out_df['F1-score']=out_df['F1-score'].fillna(-1)


out_df['totalTestedreadCT']=out_df['acceptedtrueCTcount']+out_df['rejectedfalseCTcount']
out_df['totalTestedreadnonCT']=out_df['acceptedfalseCTcount']+out_df['rejectedtrueCTcount']
out_df['totalTestedread']=out_df['totalTestedreadCT']+out_df['totalTestedreadnonCT']
out_df['totalread']=out_df['totalreadCT'] + out_df['totalreadnonCT']

out_df[celltype+"_real_rdtotal"]=out_df['totalreadCT']/out_df['totalread']
out_df[celltype+"_real_rdtested"]=out_df['totalTestedreadCT']/out_df['totalTestedread']


# In[5]:


out_df=out_df.merge(gtdf,on='Mixture')


# In[6]:


out_df.to_csv(infol+'collected_file.txt', sep='\t', index=False)

