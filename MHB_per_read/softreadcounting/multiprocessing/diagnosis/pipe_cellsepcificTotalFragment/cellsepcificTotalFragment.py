#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from collections import defaultdict
import sys

infile=sys.argv[1]  #'/Users/irffanalahi/Research/Research_update/SoftRD/melresponse_using_oldsm_withsoftRC/AUC1fullcohort/deconprepare/BL22_TILAUC1_dummyfull.txt_result_dupindex_binnedstats.pkl'

outfile=sys.argv[2]

####BL22#####
#scorecolumns=['NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','PC-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others']



####BL22LTME#####
scorecolumns=['NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','PC-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others','TIL-others','MelTumor-others']


####mel 3 compartment####
#scorecolumns=['PBL-others','TIL-others','MEL_TUMOR-others']




indf=pd.read_pickle(infile)

indf.head()


# In[2]:


set(indf['deltabasedfragassignment'].tolist())


# In[3]:


len(set(indf['deltabasedfragassignment'].tolist()))


# In[4]:


allassigned=indf.copy()


# In[5]:



allassigned.loc[indf['deltabasedfragassignment']=='NotAssigned','deltabasedfragassignment']=allassigned.loc[indf['deltabasedfragassignment']=='NotAssigned','maxscoredCT_beforeCpGweight']


# In[6]:


set(allassigned['deltabasedfragassignment'].tolist())


# In[7]:


len(set(allassigned['deltabasedfragassignment'].tolist()))


# In[8]:


def calctfrag(fgrouped,fname):
    ctfragdict= defaultdict(list)
    for score in scorecolumns:
        tmpdf=fgrouped[fgrouped['deltabasedfragassignment']==score]
        
        ctname=score.replace('-others','')
        ctfragdict[ctname].append(tmpdf.shape[0])
    
    ctfragdf=pd.DataFrame.from_dict(ctfragdict) 
    ctfragdf['Mixture']=fname
    
    return ctfragdf
    


# In[9]:


filegrouped=allassigned.groupby('filename')

totalfragdictlist=[]

for name, group in filegrouped:
    totalfragdictlist.append(calctfrag(group,name))
    


# In[10]:


totalfragdictlistDF=pd.concat(totalfragdictlist)
totalfragdictlistDF.set_index('Mixture',inplace=True)


# In[11]:


totalfragdictlistDF.head()


# In[12]:


totalfragdictlistDF.to_csv(outfile,sep="\t")


# In[13]:


#print('done')

