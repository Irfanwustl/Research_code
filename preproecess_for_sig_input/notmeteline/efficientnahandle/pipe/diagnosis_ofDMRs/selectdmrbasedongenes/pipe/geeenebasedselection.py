#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys


# In[2]:


cellsepgenfile=sys.argv[1] #"/Users/irffanalahi/Research/Research_update/SM/melcfdref/Allseperated/preprocess/defaultagain/monovst_input_out_mincpg2_q0.05_diff0.1_hypo_promdata_genomic_feature_withrepeat_header_celltypeseperated/CD14_TIL_row_combined.txt"
out=sys.argv[2]
genelist=["PDCD1","CTLA4","ITGAE","TIGIT","TOX","CD82","CD38","ICOS","HAVCR2","TNFRSF9","MKI67","ENTPD1","LAG3"]

cellsepgendf=pd.read_csv(cellsepgenfile,sep="\t")
cellsepgendf.head()


# In[3]:


outdf=cellsepgendf[cellsepgendf["Gene/Repeat type"].isin(genelist)]
outdf.to_csv(out,sep="\t",index=False)

