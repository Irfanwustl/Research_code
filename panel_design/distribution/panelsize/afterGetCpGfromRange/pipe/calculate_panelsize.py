#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

infile=sys.argv[1]  #'/Users/irffanalahi/Research/Research_code/panel_design/distribution/mergetest/toy1.bed_offsetadded.txt'
outfile=sys.argv[2]  #infile+"_panelsize.txt"


indf=pd.read_csv(infile,sep="\t",header=None)
indf.head()


# In[2]:


indf.rename(columns={0: 'chrom', 1: 'start',2:'end'},inplace=True,errors='raise')
indf['size']=indf['end']-indf['start']

panelsize=indf['size'].sum()


# In[3]:


with open(outfile, 'w') as f:
    f.write(str(panelsize))

