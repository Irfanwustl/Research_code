#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import sys


# In[2]:


infile=sys.argv[1] #"/Users/irffanalahi/Research/weekly/for_1_14_21/gene_analysis_pub_data/downstream/sep_gene/heat/data_reqfield_hg38_sorted_rolled_sorted_mergedonlyoverlapping_others_all_matrix_intesectedwith_gene_sorted_onlypromu_dict_geneDict2_1000_V3sorted.txt_gene_sorted_onlypromu_dict_geneDict2_1000_V3sorted.txt_ciberin_forheatmap/EPCAM.txt_cyberin"
out=sys.argv[2]
infiledf=pd.read_csv(infile,sep="\t")
infiledf.head()


# In[3]:


infiledf[['chrom','pos']] = infiledf.position.str.split(":",expand=True) 
infiledf['pos']=infiledf['pos'].astype(int)
infiledf.head()


# In[4]:


infiledf['start']=infiledf['pos']-1
infiledf['end']=infiledf['pos']+1
infiledf.head()


# In[5]:


infiledf=infiledf.drop(['position','pos'],axis=1)
infiledf.head()


# In[6]:


infiledf=infiledf[['chrom','start','end']]
infiledf.head()


# In[7]:


infiledf.to_csv(out,sep="\t",index=False,header=False)


