#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
BL22file=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/compareBetweenRefernces/Rawscore_noextraneous_m1weightbydelta/method1deltaweight_allct_towardsSM_dummy_mean_SM.txt_unique_result_dupindex_binnedstats.pkl_maxscore_cancerPBL_CSxOut.txt'

outfile=sys.argv[2]

BL22df=pd.read_csv(BL22file,sep='\t',index_col=0)
BL22df.head()


# In[2]:


outdf=pd.DataFrame()
outdf.head()


# In[3]:


outdf['CD4']=BL22df['NaiveCD4']+BL22df['Tregs']+BL22df['em4']+BL22df['cm4']


outdf['CD8']=BL22df['NaiveCD8']+BL22df['em8']+BL22df['cm8']

if 'CD8TIL' in BL22df.columns:
    outdf['CD8']=outdf['CD8']+BL22df['CD8TIL']

outdf['Bcell']=BL22df['nB']+BL22df['mB']
if 'PC' in BL22df.columns:
    outdf['Bcell']= outdf['Bcell']+BL22df['PC']

outdf['Mono']=BL22df['Mono']
outdf['NK']=BL22df['NK']

outdf.head()


# In[9]:


outdf_normalized= (outdf.div(outdf.sum(axis=1), axis=0))*100
outdf_normalized['total']=outdf_normalized.sum(axis=1)
outdf_normalized.head()


# In[12]:


outdf_nomono=outdf.drop(['Mono'],axis=1)
outdf_nomono.head()


# In[14]:


outdf_nomono_normalized=(outdf_nomono.div(outdf_nomono.sum(axis=1), axis=0))*100
outdf_nomono_normalized['total']=outdf_nomono_normalized.sum(axis=1)
outdf_nomono_normalized.head()


outdf_normalized.to_csv(outfile,sep='\t')
outdf_nomono_normalized.to_csv(outfile+"_nomono",sep='\t')

