#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
from collections import defaultdict
import sys
infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/for_backgroundcalculation/try1/distribution_of_Hyper/BL22EPCAM_prom_all_matrix_NO_NA_head.txt'

distributiondelta=[0,.3,.5,.7,.9]


indf=pd.read_csv(infile,sep='\t')
indf.head()


# In[2]:


outdf=indf.copy()


# In[3]:


outdf['Minimum Value']=indf.min(axis = 1)
outdf.head()


# In[4]:


distdict = defaultdict(list)
for ddelta in distributiondelta:
    tempdf=outdf[outdf['Minimum Value']>=ddelta]
    distdict[ddelta].append(tempdf.shape[0])
    


# In[5]:


distdictDF=pd.DataFrame.from_dict(distdict)
distdictDF.head()


# In[6]:


distdictDF.to_csv(infile+"_dist.txt",sep='\t',index=False)
outdf.to_csv(infile+"_withmincol.txt",sep='\t',index=False)

