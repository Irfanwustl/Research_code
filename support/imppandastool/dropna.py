#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
infile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/pythonsupport/dropna/melhealthycfDNAbgrolled_all_matrix_head100.txt"
outfile=infile+"_nona"
indf=pd.read_csv(infile,sep="\t")


# In[2]:


outdf=indf.dropna()
outdf.to_csv(outfile,sep="\t",index=False)

