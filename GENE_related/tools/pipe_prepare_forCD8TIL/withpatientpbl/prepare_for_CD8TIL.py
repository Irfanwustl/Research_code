#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/B22withLTME/v3_3steps/thirdstepanalysis/try3/towardsSM/heatmaps/preparefrom_patient_pbl/test/BL22LTME_patientPBL_all_matrix_intwith_naive_myloid_CD8TIL_OthermeanIINTWITH_melCD8TIL_activatted-.1_intwith_CD8TL_melCD8TIL_-0.7CD8TIL_-0.7_onlypos'
outfile=sys.argv[2]   #infile+"_ready.txt"


indf=pd.read_csv(infile,sep="\t")
indf.head()


# In[2]:


outdf=indf.drop(['ymel-1254-T-CD14.bedgraph_rolled','ymel-1254-T-CD4.bedgraph_rolled','ymel-1457-T-CD14.bedgraph_rolled','ymel-1457-T-CD4.bedgraph_rolled','ymel-960-T-CD14.bedgraph_rolled','ymel-960-T-CD4.bedgraph_rolled'],axis=1)


# In[3]:


outdf.to_csv(outfile,sep="\t",na_rep="NA",index=False)

