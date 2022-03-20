#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/rankspace_idea/ALLct/heatmaps/BL22promfolder_int_rankedtry2_pos_sortedby_rankedtry2_pos/BL22_all_matrix_promdata_intwith_cm4_CpGdelta_info_faster.txt_5000_forheatunderlyingdata_ranked_pos.txt_sorted.txt'
outfile=sys.argv[2]
numofline=int(sys.argv[3])

indf=pd.read_csv(infile,sep='\t')


# In[2]:


headdf=indf.head(n=numofline)
taildf=indf.tail(n=numofline)


# In[3]:


headdf.to_csv(outfile+"_head_"+str(numofline),sep='\t',index=False,na_rep='NA')
taildf.to_csv(outfile+"_tail_"+str(numofline),sep='\t',index=False,na_rep='NA')

