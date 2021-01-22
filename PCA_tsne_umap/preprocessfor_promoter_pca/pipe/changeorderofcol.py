#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
infile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/prep_promoterbasedpca/data_intersectedwith_protein-coding_gene_promoterSorteduniq.txt_head/amel-139-P-CD14.bedgraph_rolled.bedgraph"
outfile=sys.argv[2] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/prep_promoterbasedpca/out/amel-139-P-CD14.bedgraph_rolled.bedgraph"

indf=pd.read_csv(infile, sep="\t",header=None)

indf


# In[2]:


outdf=indf[[4,5,6,3]]
outdf


# In[3]:


outdf.to_csv(outfile,sep="\t",index=False, header=False)

