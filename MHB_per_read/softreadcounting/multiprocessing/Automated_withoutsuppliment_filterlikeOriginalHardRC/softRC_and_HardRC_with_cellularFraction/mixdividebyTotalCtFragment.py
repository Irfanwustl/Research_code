#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

totalctfragfile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/melresponse_using_oldsm_withsoftRC/AUC1fullcohort/deconprepare/forrename2/BL22_TILAUC1_dummyfull.txt_result_dupindex_binnedstats.pkl_ctTotalFrag.txt'
deconfile=sys.argv[2] #'/Users/irffanalahi/Research/Research_update/SoftRD/melresponse_using_oldsm_withsoftRC/AUC1fullcohort/deconprepare/forrename2/BL22_TILAUC1_dummyfull.txt_result_dupindex_binnedstats.pkladjustedScore_minus_avg_CSxOut.txt'

outfile=sys.argv[3]


totalctfragDF=pd.read_csv(totalctfragfile,sep="\t",index_col=0)

deconDF=pd.read_csv(deconfile,sep="\t",index_col=0)




totalctfragDF.head()


# In[2]:


deconDF.head()


# In[3]:



##must be same
if totalctfragDF.shape!=deconDF.shape:
    print("ERRORRR. Exitinig")
    sys.exit(1)


# In[4]:


outdf=deconDF/totalctfragDF
outdf.head()


# In[5]:


outdf.to_csv(outfile,sep="\t",na_rep='NA')


# In[6]:


#print('done')

