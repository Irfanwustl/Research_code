#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys


# In[2]:


infile=sys.argv[1]  #"/Users/irffanalahi/Research/weekly/for_3_24_21/ML/ML_postprocess/dataprepare/testdata/allfinal_lenrefCPG_subsetoffinal_cpg1_row_combinedfilename.txt"
outfile=sys.argv[2]  #infile+"_informative.txt"
indf=pd.read_csv(infile, sep="\t")
indf.head()


# In[3]:


outdf=indf[(indf['finalacceptedfor']!='notdetermined') | (indf['finalrejectedfor']!='notdetermined')]
outdf.head()


# In[4]:


outdf.to_csv(outfile,sep="\t",index=False)

