#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
largeSMfile = sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/rankspace_idea/CD8TIL/BLUgbio_CD14TIL/BLU_GBIO_withCD14TIL_SM_top1500_SM_unique'

infofile=sys.argv[2] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/rankspace_idea/CD8TIL/BLUgbio_CD14TIL/BLU_GBIO_withCD14TIL_index.txt'

largesmdf=pd.read_csv(largeSMfile,sep='\t',index_col=['chrom','start'])
largesmdf.head()


# In[2]:


largesmdf['mincolname']=largesmdf.idxmin(axis=1)
largesmdf.head()


# In[3]:


infodf=pd.read_csv(infofile,sep='\t')
#infodf['Unnamed: 0']
infodf.head()


# In[ ]:





# In[4]:


grouped=largesmdf.groupby('mincolname')
outlist=[]
for name, group in grouped:
   
    tempct=name.replace('-others','')
    corresnumber=(infodf[infodf['Unnamed: 0']==tempct]['Index']).tolist()[0]
   
    tempdf=group.head(n=corresnumber+1)
    
    outlist.append(tempdf)


# In[5]:


outdf=pd.concat(outlist)
outdf=outdf.drop(['mincolname'],axis=1)


# In[6]:


outdf.to_csv(infofile+"_inflectionSM.txt",sep='\t')

outdf.reset_index(inplace=True)
outdf[['chrom','start']].to_csv(infofile+"_inflectionSM_pos.txt",sep='\t')

