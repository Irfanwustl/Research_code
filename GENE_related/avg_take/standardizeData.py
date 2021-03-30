#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys


# In[2]:

infile=sys.argv[1] ##ciberin
outfile=sys.argv[2]

df = pd.read_csv(infile,sep="\t",index_col=0)
df


# In[3]:


#df.sub(df.mean(1), axis=0).div(df.std(1), axis=0)


# In[4]:


standardizedDF=df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)


# In[5]:


standardizedDF.to_csv(outfile,sep="\t")

