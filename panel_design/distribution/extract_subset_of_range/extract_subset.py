#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from collections import defaultdict
import sys

infile=sys.argv[1] #"toy7_out.bed"
outfile=sys.argv[2] # infile+"_stats.txt"

unique_cpg_number=[2,3,5,7]


indf=pd.read_csv(infile,sep="\t",header=None)
#indf.head()


# In[2]:


indf.rename(columns={0: 'chrom', 1: 'start',2:'end',3:'#cpg'},inplace=True,errors='raise')
#indf


# In[3]:





# In[4]:


outdict = defaultdict(list)

for uc in unique_cpg_number:
    tempdf=indf[indf['#cpg']>=uc]

    if tempdf.shape[0]>0:
        tempdf.to_csv(outfile+"_ge_"+str(uc)+".txt",sep="\t",index=False,header=False)
    
    outdict['atleast_linked_group_size'].append(uc)
    outdict['total_cpg'].append(tempdf.shape[0])

outdf=pd.DataFrame.from_dict(outdict)

outdf.to_csv(outfile,sep="\t",index=False)

