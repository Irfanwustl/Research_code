#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from collections import defaultdict
import sys

infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/B22withLTME/v3_3steps/thirdstepanalysis/try2/naive_myloid_CD8TIL_OthermeanIINTWITH_melCD8TIL_activatted-.1'

thresh=float(sys.argv[2])   #-.1

outfile=sys.argv[3]

cellType='CD8TIL'

indf=pd.read_csv(infile,sep="\t",index_col=['chrom','start','end'])
indf.head()


# In[2]:


indf['mincolname']=indf.idxmin(axis=1)
indf.head()


# In[3]:


CTspecific=indf[(indf['mincolname']==cellType+"-others") & (indf[cellType+"-others"]<=thresh)]
CTspecific.head()


# In[4]:


CTspecific.shape


# In[5]:


CTspecific[cellType+"-others"].min()


# In[6]:


CTspecific[cellType+"-others"].max()


# In[7]:


outdf=CTspecific.reset_index()
outdf.head()


# In[8]:


outdf[cellType+"-others"].min()


# In[9]:


outdf[cellType+"-others"].max()


# In[10]:


outdf=outdf[['chrom','start','end']]
outdf.head()


# In[11]:


outdf.shape


# In[12]:


outdf.to_csv(outfile+cellType+"_"+str(thresh)+"_onlypos",sep="\t",index=False,header=False)

