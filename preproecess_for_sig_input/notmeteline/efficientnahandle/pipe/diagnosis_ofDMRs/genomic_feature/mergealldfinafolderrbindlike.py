#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob, os
import sys


# In[2]:


infolder=sys.argv[1] #"/Users/irffanalahi/Research/weekly/for_3_17_21/MLmodel/dataprepare_fragclassification/downstream/DCB_NDB_seperate/finalize/cpg2_nohealthy_melpos"
out=infolder+"_row_combined.txt"


# In[3]:


files = glob.glob(infolder+'/*.txt')
filesdf=[pd.read_csv(fp,sep="\t",low_memory = False) for fp in files]


# In[4]:


df_combined = pd.concat(filesdf, axis=0)
df_combined.head()


# In[5]:


df_combined.to_csv(out,sep="\t",na_rep="NA",index=False)

