#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from collections import defaultdict
import sys


posscorefile=sys.argv[1] #'CD8TIL_pbl_tum_all_matrix_allout_ranked_SM_top50_maxscore_CSxOut_withoutextrenous3.txt' #sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/pipe_maxpossiblescore_idea/oldsmset2_toy_somesamples_globalout_binnedstats.pkl_onlydup_softRC/BL22_TILAUC1_dummyfull.txt_result_dupindex_binnedstats.pkl_maxscore_CSxOut.txt'

outfile=sys.argv[2] #'m1weighted_jupyter'+posscorefile  #sys.argv[2] #posscorefile+"_proportion.txt"

smfile=sys.argv[3]  #'CD8TIL_pbl_tum_all_matrix_allout_ranked_SM_top50_SM_unique' #sys.argv[3] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/pipe_maxpossiblescore_idea/oldsmset2_toy/BL22_TILAUC1_dummy_partialCauseBL22impute.txt'

posscoredf=pd.read_csv(posscorefile,sep="\t",index_col='Mixture')



smdf=pd.read_csv(smfile,sep="\t",index_col=['chrom','start'])
smdf.head()


# In[2]:


smdf['mincolname']=smdf.idxmin(axis=1)
smdf.head()


# In[3]:


grouped=smdf.groupby('mincolname')
outlist=defaultdict(list)
for name, group in grouped:
    tempct=name.replace('-others','')
    outlist[tempct].append(group.shape[0])
    
    outlist[tempct].append(group[name].mean())
    


# In[4]:


outdf=pd.DataFrame.from_dict(outlist,orient='index',columns=['#CpG','delta'])
outdf.index.name='Celltype'
ct_cpgdf=outdf.copy()
ct_cpgdf.reset_index(inplace=True)

ct_cpgdf['delta']=-1*ct_cpgdf['delta']
ct_cpgdf['cpg_weightedby_delta']=ct_cpgdf['delta']*ct_cpgdf['#CpG']
ct_cpgdf


# In[5]:


posscoredf.head()


# In[6]:



allct=ct_cpgdf['Celltype'].tolist()
allct=list(set(allct).intersection(set(list(posscoredf.columns))))
len(allct)


# In[7]:


for ct in allct:
    posscoredf[ct]=posscoredf[ct]/float(ct_cpgdf.loc[ct_cpgdf['Celltype']==ct,'cpg_weightedby_delta'])


# In[8]:


posscoredf.head()


# In[9]:



sumofnormalizedctscore=posscoredf[allct].sum(axis=1)


# In[10]:


for ct in allct:
    posscoredf[ct]=posscoredf[ct]/sumofnormalizedctscore*100


# In[11]:


posscoredf.head()


# In[12]:


posscoredf.to_csv(outfile,sep='\t')
