#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/ENCODE_data/toydata/BL22_CD8TIL_withCD14TILprom_all_matrix_head1000.txt'
indf=pd.read_csv(infile,sep='\t',low_memory=False,index_col=['chrom','start','end'])

distributiondelta=[.3,.5]
indf.head()


# In[2]:


outdf=indf.copy()


# In[3]:


outdf['Minimum Value']=indf.mean(axis = 1)
outdf.head()


# In[3]:



for ddelta in distributiondelta:
    tempdf=(outdf[outdf['Minimum Value']>=ddelta]).copy()
    outtmp=tempdf.reset_index()
    (outtmp[['chrom','start','end']]).to_csv(infile+"_atleastMeanBeta_"+str(ddelta),sep='\t',index=False,header=False)
   

