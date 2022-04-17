#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pandas as pd
from collections import defaultdict
from sklearn import metrics
import numpy as np
import sys
import time

start_time = time.time()

inbinfile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/largerEXP/genepromdelta.7/defaultsm/CD4geneprom.7mixture_output_mdadded_sorted_softMultiprocessing_binnedstats.pkl'

outfile=sys.argv[2]

scorecolumns=sys.argv[3:]


consideringALLheyper=True


inbindf=pd.read_pickle(inbinfile)



####BL22#####
#scorecolumns=['NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','PC-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others']


####BL22LTME#####
#scorecolumns=['NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','PC-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others','TIL-others','MelTumor-others']

###em4_cm4
#scorecolumns=['cm4-others','em4-others','Tcell-others']



###bL14######
#scorecolumns=['CD4-others','CD8-others','nB-others','NK-others','Mn-others','mNeu-others','m8-others','DC-others','Eo-others','Tr-others','m4-others','Mg-others','Er-others','mB-others']

inbindf=inbindf.reset_index()
inbindf.head()


# In[2]:


if consideringALLheyper==True:
    allassigned=inbindf.copy()


elif consideringALLheyper==False:
    allassigned=inbindf[inbindf['deltabasedfragassignment']!='NotAssigned'].copy()
    
else:
    print("wrong input")
    sys.exit(1)
#
allassigned.head()


# In[3]:


allassigned.loc[inbindf['deltabasedfragassignment']=='NotAssigned','deltabasedfragassignment']=allassigned.loc[inbindf['deltabasedfragassignment']=='NotAssigned','maxscoredCT_beforeCpGweight']


# In[4]:


allassigned['secondmaxScore']='Notassigned'
allassigned['secondmaxScoreCT']='Notassigned'
allassigned.head()


# In[5]:


grouped=allassigned.groupby('maxscoredCT')

for name, group in grouped:
    
    
    tempscorecolumns=scorecolumns.copy()
    
    tempscorecolumns.remove(name)
    
    allassigned.loc[group.index,'secondmaxScore']=group[tempscorecolumns].max(axis=1)
    allassigned.loc[group.index,'secondmaxScoreCT']=(group[tempscorecolumns]).idxmax(axis=1)


# In[6]:


allassigned['adjustedScore_minus']=allassigned['maxscore']-allassigned['secondmaxScore']
allassigned['adjustedScore_minus_avg']=(allassigned['maxscore']+(allassigned['maxscore']-allassigned['secondmaxScore']))/2
allassigned.head()


# In[7]:


allassigned.columns


# In[8]:


adjustedScore_minus0val=list(set(allassigned[allassigned['LENhypoCpG_BY_total_cpg']==0]['adjustedScore_minus'].tolist()))
if len(adjustedScore_minus0val)==0:
    pass
elif len(adjustedScore_minus0val)!=1 or adjustedScore_minus0val[0]!=0:
    print(adjustedScore_minus0val)
    sys.exit(1)
    


# In[9]:


adjustedScore_minus_avg0val=list(set(allassigned[allassigned['LENhypoCpG_BY_total_cpg']==0]['adjustedScore_minus_avg'].tolist()))


if len(adjustedScore_minus_avg0val)==0:
    pass

elif len(adjustedScore_minus_avg0val)!=1 or adjustedScore_minus_avg0val[0]!=0:
    print(adjustedScore_minus_avg0val)
    sys.exit(1)
    


# In[10]:


allassigned['LENhypoCpG_0.8']=0
allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.8,'LENhypoCpG_0.8']=allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.8,'LENhypoCpG']


# In[11]:


allassigned['LENhypoCpG_0.5']=0
allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.5,'LENhypoCpG_0.5']=allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.5,'LENhypoCpG']


# In[12]:


allassigned.head()


# In[13]:


def calposscore(fgrouped,whichmethod,fname):
    ctposscoredict= defaultdict(list)
    for score in scorecolumns:
        deltabasedfragassigned=fgrouped['deltabasedfragassignment'].tolist()
        if score in deltabasedfragassigned:
            temp_posscore=fgrouped.loc[fgrouped['deltabasedfragassignment']==score,whichmethod].tolist()
            temptotal_posscore=sum(temp_posscore)
            temp_posfrag=len(temp_posscore)

        else:
            temptotal_posscore=0
            temp_posfrag=0

        ctname=score.replace('-others','')

        ctposscoredict[ctname].append(temptotal_posscore)
    ctposscoredf=pd.DataFrame.from_dict(ctposscoredict)
    ctposscoredf['Mixture']=fname

   
    return ctposscoredf
        


# In[14]:


filegrouped=allassigned.groupby('filename')

maxscorelist=[]
adjustedScore_minuslist=[]
adjustedScore_minus_avglist=[]

for name, group in filegrouped:
    maxscorelist.append(calposscore(group,'maxscore',name))
    adjustedScore_minuslist.append(calposscore(group,'adjustedScore_minus',name))
    adjustedScore_minus_avglist.append(calposscore(group,'adjustedScore_minus_avg',name))
    


# In[15]:


maxscorelistDF=pd.concat(maxscorelist)
maxscorelistDF.set_index('Mixture',inplace=True)
adjustedScore_minuslistDF=pd.concat(adjustedScore_minuslist)
adjustedScore_minuslistDF.set_index('Mixture',inplace=True)
adjustedScore_minus_avglistDF=pd.concat(adjustedScore_minus_avglist)
adjustedScore_minus_avglistDF.set_index('Mixture',inplace=True)


# In[16]:


maxscorelistDF.to_csv(outfile+'_maxscore_CSxOut.txt',sep="\t")
adjustedScore_minuslistDF.to_csv(outfile+'adjustedScore_minus_CSxOut.txt',sep="\t")
adjustedScore_minus_avglistDF.to_csv(outfile+'adjustedScore_minus_avg_CSxOut.txt',sep="\t")


# In[17]:


end_time = time.time()

time_elapsed = (end_time - start_time)

#print(time_elapsed)

