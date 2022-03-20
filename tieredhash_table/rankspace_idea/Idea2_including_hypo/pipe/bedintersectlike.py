#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

rowmeanfile = sys.argv[1] #'BL22_all_matrix_promdataCin_nr0.9_imputed_rowmean_bg_head1000.txt'
deltainfofile = sys.argv[2] #'deltainfofolder/Tregs_CpGdelta_info_faster_head1000.txt'

outfile=sys.argv[3] #'merged.txt'

rowmeandf=pd.read_csv(rowmeanfile,sep='\t')
rowmeandf.set_index(['chrom','start','end'],inplace=True)
rowmeandf=rowmeandf.drop(['shouldbechrom','pos'],axis=1)
rowmeandf.head()


# In[2]:


deltinfodf=pd.read_csv(deltainfofile,sep='\t')
deltinfodf.set_index(['chrom','start','end'],inplace=True)
deltinfodf.head()


# In[3]:


mergeddf=deltinfodf.merge(rowmeandf,left_index=True,right_index=True)


# In[4]:


mergeddf.head()


# In[5]:


mergeddf.reset_index(inplace=True)
mergeddf.head()


# In[6]:


mergeddf.to_csv(outfile,sep='\t',index=False)

