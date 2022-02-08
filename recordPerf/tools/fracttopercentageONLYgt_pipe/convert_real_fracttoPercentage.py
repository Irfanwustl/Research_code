#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as  pd
import sys

infile=sys.argv[1]  #'/Users/irffanalahi/Research/Research_update/SoftRD/largerEXP/BL22genepromdelta.7/Realdata/corr/Morecelltypes/divbyCTFRAG/perctcorr/try2/BL22_genepromSM_0.7.txt_TRAININGbestref.txt_result_dupindex_binnedstats.pkladjustedScore_minus_avg_CSxOut.txt_1stflow_7samples_fixedDCm4trfixed_morect_8subsetANDPCfromcytof.txt'
outfile=sys.argv[2]


suffix='_real'


indf=pd.read_csv(infile,sep='\t')
indf.head()


# In[2]:


allcols=indf.columns
allcols


# In[3]:


for acol in allcols:
    if suffix in acol:
        indf[acol]=indf[acol]*100

        
indf.head()


# In[4]:


indf.to_csv(outfile,sep='\t',index=False)

