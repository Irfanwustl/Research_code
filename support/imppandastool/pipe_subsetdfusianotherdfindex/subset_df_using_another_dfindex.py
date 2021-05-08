#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
dftosubset=sys.argv[1] #"/Users/irffanalahi/Research/weekly/for_10_1_20/SM/poormanMHB/allpblsubset/sm/processthelonglist/processdownsample/smfromdownsample/pblsubsetpoormanMHB_hypo.txt"
indexdf=sys.argv[2] #"/Users/irffanalahi/Research/weekly/for_10_1_20/SM/poormanMHB/allpblsubset/sm/processthelonglist/processdownsample/smfromdownsample/pblsubsetpoormanMHB_hypo.txt_assigned.txt_mhb_sampled_ciberin"

outname=sys.argv[3]

dfs=pd.read_csv(dftosubset,sep="\t",index_col=0)
dfi=pd.read_csv(indexdf,sep="\t",index_col=0)


# In[2]:


dfs.head()


# In[3]:


dfi.head()


# In[4]:


outdf=dfs[dfs.index.isin(dfi.index)]


# In[5]:


outdf.head()


# In[6]:


outdf.to_csv(outname,sep="\t")

