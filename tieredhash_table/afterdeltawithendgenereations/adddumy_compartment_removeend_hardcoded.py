#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/B22withLTME/v3_3steps/thirdstepanalysis/try3/towardsSM/test/activated_CD8TIL_all_matrixCin_nr0.5_imputed_rowmean_bg_othermean.txt_withend.txt_intwith_naive_myloid_CD8TIL_OthermeanIINTWITH_melCD8TIL_activatted-.1_intwith_CD8TL_melCD8TIL_-0.7CD8TIL_-0.7_onlypos'
outfile=sys.argv[2]  #infile+"_dummy.txt"




total_compartments=['chrom','start','CD8TIL-others','MelTumor-others','CD8PBL-others']

finalcompartmentshouldbe=len(total_compartments)
total_compartments_set=set(total_compartments)

indf=pd.read_csv(infile,sep="\t")
indf.head()


# In[2]:


indfcolumns=set(indf.columns.tolist())
indfcolumns


# In[3]:


missingcols=total_compartments_set-indfcolumns
missingcolslist=list(missingcols)
missingcolslist


# In[4]:


for micol in missingcolslist:
    indf[micol]=0.9
    


# In[5]:


indf.head()


# In[6]:


outdf=indf.drop(['end'], axis=1)
if outdf.shape[1]!=finalcompartmentshouldbe:
    print(infile)
    print("error. Exiting")
    sys.exit(1)


# In[7]:


outdf=outdf[total_compartments]
outdf.head()


# In[8]:


outdf.to_csv(outfile,sep="\t",index=False)

