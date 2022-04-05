#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

infile=sys.argv[1]   #'/Users/irffanalahi/Research/Research_update/SoftRD/largerEXP/BL22_tiered_rankedidea/irAE/somecandidate_result/method1Fract_allct_towardsSM_dummy_mean_SM.txt_unique_result_dupindex_binnedstats.pkl_maxscore_CSxOut.txt'

outfile=sys.argv[2] #infile+"_normalized"

indf=pd.read_csv(infile,sep='\t',index_col=0)
indf.head()


# In[2]:


normalized_df=indf.div(indf.sum(axis=1), axis=0)


# In[3]:


normalized_df.head()


# In[4]:


outdf=normalized_df*100
outdf.head()


# In[5]:


outdf.to_csv(outfile,sep='\t')

