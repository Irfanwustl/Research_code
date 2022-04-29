#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/TissuTypes/heatmaps/ENCODE_otherct_atleastBeta_0.5_MYtcga_all_matrix_folder_int_ENCODE_otherct_atleastBeta_0.5_all_matrix_allout_ranked_inflectionpos_sortedby_ENCODE_otherct_atleastBeta_0.5_all_matrix_allout_ranked_inflectionpos/ENCODE_otherct_atleastBeta_0.5_MYtcga_all_matrix_intwith_UpperLobeOfLeftLung_CpGdelta_info_faster.txt_5000_forheatunderlyingdata_ranked.txt_pos.txt_sorted.txt'
outfile=sys.argv[2] #infile+"_namefixed.txt"
indf=pd.read_csv(infile,sep='\t',index_col=['chrom','start','end'])
indf.head()


# In[2]:


namingdict={}

allcolumns=indf.columns
for acol in allcolumns:
    firstpart=acol.split("_")[0]
    if firstpart=='z':
        newname=acol.split("_")[1]
    
        namingdict[acol]=newname
   
        


# In[3]:


indf.rename(columns=namingdict,inplace=True)
indf.head()


# In[4]:


indf.to_csv(outfile,sep='\t',na_rep='NA')

