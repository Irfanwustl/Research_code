#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import os
from collections import defaultdict

import sys

infolder=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/chromosome_Y_analysis/Extracting_SRY_gene/fulldepth_info'


# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[3]:


allfiles=listdir_nohidden(infolder)


# In[4]:


outdict = defaultdict(list)
for infile in allfiles:
    indf=pd.read_csv(infile,sep='\t',header=None)
    SRYdf=indf[(indf[0]=='chrY') & (indf[1]>2786855) & (indf[1]<2787682)]
    
    if SRYdf.shape[0]==0:
        tempmedian=0
    else:
        tempmedian=SRYdf[2].median()
   
        
    outdict[os.path.basename(infile)].append(tempmedian)


# In[5]:


outdict


# In[6]:


outdf=pd.DataFrame.from_dict(outdict,orient='index',columns=['median_depth'])
outdf.to_csv(infolder+"_srydepth.txt",sep='\t')

