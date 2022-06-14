#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import os
import sys
infile=sys.argv[1]   #'/Users/irffanalahi/Research/Research_update/GENE/Someresults/Bcell_toxicity/downstream/melanoma_bg_BS_all_matrix_intesectedwith_Bcell_toxicity_promoter_singleValue.txt_Bcell_toxicity_promoter_singleValue.txt_prepared/IL10.txt'

outname=sys.argv[2]


na_Cutoff=0.8

indf=pd.read_csv(infile,sep='\t',index_col=['chrom','start','end'])

indf.head()



# In[2]:


indf.shape


# In[3]:


nathreshhold_count=indf.shape[0]*na_Cutoff
nathreshhold_count


# In[4]:


lessNAdf=indf.dropna( axis=1, thresh=nathreshhold_count)
lessNAdf.head()


# In[5]:


lessNAdf.shape


# In[6]:


gene=os.path.splitext(os.path.basename(infile))[0]

samplavg=lessNAdf.mean(axis=0)
samplmedian=lessNAdf.median(axis=0)
samplavgdf=pd.DataFrame({'Mixture':samplavg.index, gene+"_mean":samplavg.values})
samplmediandf=pd.DataFrame({'Mixture':samplmedian.index, gene+"_median":samplmedian.values})

samplmediandf.to_csv(outname+"_median.txt",sep="\t",index=False)
samplavgdf.to_csv(outname+"_mean.txt",sep="\t",index=False)

