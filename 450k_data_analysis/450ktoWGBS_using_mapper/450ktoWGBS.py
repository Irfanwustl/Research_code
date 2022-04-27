#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

four50kfile=sys.argv[1] #'test_head/2e21525a-20a5-4b57-92df-d1c22c95a14a.methylation_array.sesame.level3betas.txt'




mapperfile='HM450.hg38.manifest.txt'
outfile=sys.argv[2]




mapperdf=pd.read_csv(mapperfile,sep='\t',dtype='str')
mapperdf.head()


# In[2]:


four50kdf=pd.read_csv(four50kfile,sep='\t',header=None,names=['probeID','value'],dtype='str')

four50kdf.head()


# In[3]:


four50kdfmerged=four50kdf.merge(mapperdf,on='probeID',how='inner')


# In[4]:


outdf=four50kdfmerged[['CpG_chrm','CpG_beg','CpG_end','value']]
outdf=outdf.dropna()
outdf.head()


# In[5]:


outdf.to_csv(outfile,sep='\t',index=False,header=False)

