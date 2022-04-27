#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/opensource_data/ENCODE/downloadtest/ENCFF716SXG_head.bed.txt'

outfile=sys.argv[2] #infile+"_formated.txt"

indf=pd.read_csv(infile,header=None,sep='\t',low_memory=False)
indf.head()


# In[2]:


indf[2]=indf[2]+1
indf.head()


# In[3]:


indf[10]=indf[10]/100
indf.head()


# In[4]:


outdf=indf[[0,1,2,10]]
outdf.head()


# In[5]:


outdf.to_csv(outfile,sep='\t',index=False,header=False)

