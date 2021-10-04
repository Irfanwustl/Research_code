#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/panel_design/distribution/mergetest/toy1.bed'
outfile=sys.argv[2] #infile+"_offsetadded.txt"

offset=5
indf=pd.read_csv(infile,sep="\t",header=None)
#indf.head()


# In[2]:


indf.rename(columns={0: 'chrom', 1: 'prevstart',2:'prevend'},inplace=True,errors='raise')
#indf.head()


# In[3]:


indf['start']=indf['prevstart']-offset
indf['end']=indf['prevend']+offset


indf.loc[indf['start']<=0,'start']=0


outdf=indf[['chrom','start','end']]
#outdf.head()


# In[4]:


outdf.to_csv(outfile,sep="\t",index=False,header=False)

