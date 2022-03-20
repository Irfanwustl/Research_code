#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/BL22_groupv2/All/Alllinked/towardsFinalRef/allct_towardsSM_dummy_min_SM.txt'

indf=pd.read_csv(infile,sep='\t',index_col=['chrom','start'])
indf.head()


# In[2]:


indf.shape


# In[3]:


indf = indf[~indf.index.duplicated(keep=False)]


# In[4]:


indf.shape


# In[5]:


indf.to_csv(infile+"_unique",sep='\t')

