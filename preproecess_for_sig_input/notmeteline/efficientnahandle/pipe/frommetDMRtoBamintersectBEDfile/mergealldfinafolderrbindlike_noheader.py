#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob, os
import sys


# In[2]:


infolder=sys.argv[1] #"/Users/irffanalahi/Research/Research_update/SM/melcfdref/LargerLTME/forbam/alltogother"
out=sys.argv[2] #infolder+"_row_combined.txt"


# In[3]:


files = glob.glob(infolder+'/*.txt')
filesdf=[pd.read_csv(fp,sep="\t",header=None) for fp in files]


# In[4]:


df_combined = pd.concat(filesdf, axis=0)
df_combined.head()


# In[5]:


df_combined.to_csv(out,sep="\t",na_rep="NA",index=False,header=False)

