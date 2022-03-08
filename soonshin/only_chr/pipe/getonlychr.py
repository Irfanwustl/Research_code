#!/usr/bin/env python
# coding: utf-8

# In[14]:


# Shoonhsin Li
# 02/12/2022

import pandas as pd
import sys

# develop list of wanted chromosome positions
chrs = ["chr" + str(i) for i in range(1, 23)]
chrs.append("chrX")
chrs.append("chrY")

filename = sys.argv[1] #"genepromoter_1000_1000_sorted_onlypos_merged.txt"
outname=sys.argv[2]
data = pd.read_csv(filename, sep='\t', header=None, index_col=0)
df = data.loc[chrs]

df.to_csv(outname, sep='\t', header=None)


# In[ ]:




