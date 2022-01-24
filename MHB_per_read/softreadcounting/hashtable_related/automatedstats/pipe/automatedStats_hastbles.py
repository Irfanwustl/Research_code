#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import os
from collections import defaultdict

import sys

#infol must have only one cutoff for  one comparison. other 2 vary.
infol=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/downstream/hashtablestats/test'

celltype=sys.argv[2] #'CD8TIL'

outfile=sys.argv[3]


# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[3]:


allfiles=listdir_nohidden(infol)


# In[4]:


outdict= defaultdict(list)

for  f in  allfiles:
    tempdf=pd.read_csv(f,sep='\t',index_col=['chrom','start'])
    if tempdf.shape[0]==0:
        outdict[os.path.basename(f)].append(0)
        continue
    tempdf['mincolname']=tempdf.idxmin(axis=1)
    ctspecificcpg=tempdf[tempdf['mincolname']==celltype+"-others"]
    
    
    if  ctspecificcpg.shape[0]!=tempdf.shape[0]:
        print("if this is supposed to one ct ref file, it is an error. LOOK CAREFULLY")
    outdict[os.path.basename(f)].append(ctspecificcpg.shape[0])
    


# In[11]:


outdf=pd.DataFrame.from_dict(outdict,orient='index',columns=[celltype])
outdf.index.name='SM'

outdf.to_csv(outfile,sep='\t')

