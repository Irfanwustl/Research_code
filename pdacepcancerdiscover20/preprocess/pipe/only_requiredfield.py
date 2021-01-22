#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

infile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/pdacepcamcanerdiscovery/input2/GSM4928782_PDAC1-Ep_raw.bed"
outname=sys.argv[2] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/pdacepcamcanerdiscovery/GSM4928782_PDAC1-Ep_raw.bed_full.txt"
indf=pd.read_csv(infile,sep="\t",header=None)

indf.head()


# In[2]:


indf=indf.drop([3,5],axis=1)


# In[3]:


indf.head()


# In[4]:


indf=indf.dropna()


# In[5]:


indf[4]=indf[4]/1000*1.0


# In[6]:


indf.head()


# In[7]:


minval=indf[4].min()
minval


# In[8]:


maxval=indf[4].max()
maxval


# In[9]:


if minval<0:
    print("min error",minval)
    sys.exit(1)
if maxval>1:
    print("maxerror",maxval)
    sys.exit(1)


# In[10]:


indf=indf.astype({1: int,2:int})
indf.head()


# In[11]:


indf.to_csv(outname,sep="\t",index=False,header=False)

