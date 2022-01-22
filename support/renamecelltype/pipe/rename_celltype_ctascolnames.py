#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/Bilge/boxplots/BL22_genepromSM_0.7.txt_TRAININGbestref.txt_result_dupindex_binnedstats.pkladjustedScore_minus_avgdivbyCTFRAG_CSxOut.txt_irAEgt.txt'
outfile=sys.argv[2]


##cell type as index###

indf=pd.read_csv(infile,sep="\t",index_col=0)
indf.head()


# In[2]:


standardnamedict={'TIL_real':'CD8TIL_real'}


# In[3]:


outdf=indf.copy()
outdf.rename(columns=standardnamedict,inplace=True)
outdf.head()


# In[4]:


outdf.to_csv(outfile,sep="\t")

