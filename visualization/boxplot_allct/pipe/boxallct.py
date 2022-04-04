#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import sys
infile=sys.argv[1] # '/Users/irffanalahi/Research/Research_update/SoftRD/largerEXP/BL22_tiered_rankedidea/cellular_fraction/perctcorr/maxscore_ct_flow/maxscorFract_allct_towardsSM_dummy_mean_SM.txt_unique_result_dupindex_binnedstats.pkl_maxscore_CSxOut.txt_1stflow.txt' #'allct_towardsSM_dummy_mean_SM.txt_unique_withmincol.txtEPCAM_mean_SM_top1000.txt_result_dupindex_binnedstats.pkl_maxscore_ctporportion_CSxOut_per.txt_ctrename.txt'

outfile=sys.argv[2] # infile

indf=pd.read_csv(infile,sep='\t',index_col=0)
indf.head()


order=['Naive CD4 T','Tregs','CD4 TEM','CD4 TCM','Naive CD8 T','CD8 TEM','CD8 TCM','CD8 TEMRA','Naive B','Memory B','NK','Mono','Mac (M0)','Mac (M1)','Mac (M2)','iDC','mDC','PMN','Eosinophil','Megakaryocyte','Erythrocyte']
#indf=indf[['Naive CD4 T','Naive CD8','Naive B','NK','Mono','Mac (M0)','Mac (M1)','Mac (M2)','iDC','mDC','PMN','CD8 TCM','CD8 TEM','Eosinophil','Tregs','CD4 TEM','CD8 TEMRA','Megakaryocyte','CD4 TCM','Erythrocyte','Memory B','EPCAM']]


# In[2]:


standardnamedict={"M0":"Mac (M0)","M1":"Mac (M1)","M2":"Mac (M2)","NaiveCD4":"Naive CD4 T","NaiveCD8":"Naive CD8 T","CD4": "Naive CD4", "CD8": "Naive CD8 T","mB":"Memory B",'Mn':'Mono','CD14':'Mono','CD19':'B Cell','nB':'Naive B','PC':'PC','cm8':'CD8 TCM','em8':'CD8 TEM','m8':'CD8 memory','ed8':'CD8 TEMRA','cm4':'CD4 TCM','em4':'CD4 TEM','m4':'CD4 memory','mNeu':'PMN','Eo':'Eosinophil','Tr':'Tregs','Mg':'Megakaryocyte','Er':'Erythrocyte'}


# In[3]:


indf.rename(columns=standardnamedict,inplace=True)


# In[4]:


indf=indf[order]


# In[6]:


indf.boxplot(rot=90)
plt.savefig(outfile+'.pdf',bbox_inches='tight')

