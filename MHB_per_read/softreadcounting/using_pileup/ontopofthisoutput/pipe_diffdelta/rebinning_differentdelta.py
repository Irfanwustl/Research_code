#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from collections import defaultdict
import numpy as np
import sys

infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/softRD_pileup/cd4bams_softRDpileup/CD4allrange_NR_1000000_insilmix41_sorted_binnedstats.txt'


outfile=sys.argv[2] 
indf=pd.read_csv(infile,sep="\t",index_col=0)

scorecolumns=['CD4-others','CD8-others','nB-others','NK-others','Mn-others','mNeu-others','m8-others','DC-others','Eo-others','Tr-others','m4-others','Mg-others','Er-others','mB-others']


scorethresh=0

indf.head()


# In[2]:


outdfcpgweighted=indf[indf['maxscore']>scorethresh]
outdfcpgweighted.head()


# In[3]:


print(indf.shape)
print(outdfcpgweighted.shape)


# In[4]:


outdfcpgweighted['secondmaxScore']='Notassigned'
outdfcpgweighted['secondmaxScoreCT']='Notassigned'
outdfcpgweighted.head()


# In[5]:


grouped=outdfcpgweighted.groupby('maxscoredCT')

for name, group in grouped:
    
    
    tempscorecolumns=scorecolumns.copy()
    
    tempscorecolumns.remove(name)
    
    outdfcpgweighted.loc[group.index,'secondmaxScore']=group[tempscorecolumns].max(axis=1)
    outdfcpgweighted.loc[group.index,'secondmaxScoreCT']=(group[tempscorecolumns]).idxmax(axis=1)
   


# In[6]:


outdfcpgweighted.head()


# In[7]:


set(outdfcpgweighted['deltabasedfragassignment'].tolist())


# In[8]:


outdfcpgweighted['adjustedScore_minus']=outdfcpgweighted['maxscore']-outdfcpgweighted['secondmaxScore']
outdfcpgweighted['adjustedScore_minus_avg']=(outdfcpgweighted['maxscore']+(outdfcpgweighted['maxscore']-outdfcpgweighted['secondmaxScore']))/2
outdfcpgweighted.head()


# In[9]:


def finalscore_cal(finalscorecolumn):
    ctposscoredict= defaultdict(list)
    ctposfragdict= defaultdict(list)
    for score in scorecolumns:
        deltabasedfragassigned=outdfcpgweighted['deltabasedfragassignment'].tolist()
        if score in deltabasedfragassigned:
            temp_posscore=outdfcpgweighted.loc[outdfcpgweighted['deltabasedfragassignment']==score,finalscorecolumn].tolist()
            temptotal_posscore=sum(temp_posscore)
            temp_posfrag=len(temp_posscore)

        else:
            temptotal_posscore=0
            temp_posfrag=0

        ctname=score.replace('-others','')

        ctposscoredict[ctname].append(temptotal_posscore)

        ctposfragdict[ctname].append(temp_posfrag)
    ctposscoredf=pd.DataFrame.from_dict(ctposscoredict)
    ctposfragdf=pd.DataFrame.from_dict(ctposfragdict)
    return ctposscoredf #,ctposfragdf


# In[10]:




adjustedScore_minus_df=finalscore_cal('adjustedScore_minus')
adjustedScore_minus_avgdf=finalscore_cal('adjustedScore_minus_avg')


# In[11]:

outdfcpgweighted.to_csv(outfile+"_rebinstats.txt",sep="\t")
adjustedScore_minus_df.to_csv(outfile+"_adjustedScore_minus.txt",sep="\t",index=False)


# In[12]:


adjustedScore_minus_avgdf.to_csv(outfile+"_adjustedScore_minus_avg.txt",sep="\t",index=False)

