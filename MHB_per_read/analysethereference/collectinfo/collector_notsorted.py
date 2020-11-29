#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
largerfile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/moretest/diagnosisthesm/NeuPBLpoormanHypo"#ciberin
reffile=sys.argv[2] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/moretest/diagnosisthesm/blwithneu_hypo_stat.txt_0.01_2_g100.txtWithSurrounding.txt_1cpgnc_withoutheader_sorted_headeradded.txt_cyberin"#ciberin

largedf=pd.read_csv(largerfile,sep="\t",index_col=0)
refdf=pd.read_csv(reffile,sep="\t",index_col=0)


# In[2]:


largedf.head()


# In[3]:


refdf.head()


# In[5]:


subsetoflarger=largedf[largedf.index.isin(refdf.index)]
subsetoflarger.head()


# In[7]:


#subsetoflargersorted=subsetoflarger.reindex(refdf.index)
#subsetoflargersorted.head()


# In[8]:


print(largedf.shape)
print(refdf.shape)
print(subsetoflarger.shape)
print(subsetoflargersorted.shape)


# In[10]:


subsetoflargersorted.to_csv(largerfile+"_subset_notsorted.txt",sep="\t")
print("done")

