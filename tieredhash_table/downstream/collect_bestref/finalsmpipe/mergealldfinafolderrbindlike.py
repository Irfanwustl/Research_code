#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob, os

import sys

# In[2]:


infolder=sys.argv[1] #"/Users/irffanalahi/Research/Research_update/SM/ShowcaseSM/BL17_14/genomic_feature/howmany_in_genomic_body /BL14in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.1"
out=sys.argv[2]  #infolder+"_row_combined.txt"

suffix=sys.argv[3]


# In[3]:


files = glob.glob(infolder+'/*'+suffix)
filesdf=[pd.read_csv(fp,sep="\t") for fp in files]


# In[4]:


df_combined = pd.concat(filesdf, axis=0)
df_combined.head()


# In[5]:


df_combined.to_csv(out,sep="\t",na_rep="NA",index=False)

