#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/Majorlineage/Genomic_feature/BLU_inflection/Bcell_CpGdelta_info_faster.txt_5000_forheatunderlyingdata_ranked.txt_pos.txt__row_combined.txt'
outfile=sys.argv[2] #infile+"_nondup.txt"


indf=pd.read_csv(infile,sep='\t')

indf.head()


# In[2]:


outdf=indf.drop(['3','4','5'],axis=1)
outdf.head()


# In[3]:


outdf.shape


# In[4]:


outdf.drop_duplicates(inplace=True)


# In[5]:


outdf.shape


# In[6]:


outdf.to_csv(outfile,sep='\t',index=False)

