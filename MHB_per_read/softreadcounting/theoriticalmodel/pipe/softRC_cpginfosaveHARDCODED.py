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

###should be the final one###
inbinfile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/for_backgroundcalculation/EM-Seq_07-no-spike.bedgraph_rolled.bedgraph_randomSM_0.txt_result_dupindex_binnedstats.pkl_FINAL_binnedstats.pkl'

outfile=sys.argv[2] #inbinfile


consideringALLheyper=True


inbindf=pd.read_pickle(inbinfile)
####BL22#####
#scorecolumns=['NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others','EPCAM-others']


scorecolumns=['EPCAM-others']

#BL14
#scorecolumns=['CD4-others','CD8-others','nB-others','NK-others','Mn-others','mNeu-others','m8-others','DC-others','Eo-others','Tr-others','m4-others','Mg-others','Er-others','mB-others']


allassigned=inbindf.copy()
allassigned.head()


# In[2]:


####considering only positive fragment#########

#allassigned=allassigned[allassigned['maxscore']>0]


# In[3]:


allassigned.loc[allassigned['LENhypoCpG']==0,'maxscore_beforeCpGweight']=0


# In[4]:


allassigned[allassigned['LENhypoCpG']==0].head()


# In[5]:


allassigned[allassigned['maxscore_beforeCpGweight']<allassigned['maxscore']]


# In[6]:


def calposscore(fgrouped,whichmethod,fname):
    ctposscoredict= defaultdict(list)
    totalcpgdict=defaultdict(list)
    hypocpgdict=defaultdict(list)
    hypercpgdict=defaultdict(list)
    
    TPposscoredict=defaultdict(list)
    FPposscoredict=defaultdict(list)
    
    for score in scorecolumns:
        ctname=score.replace('-others','')
        deltabasedfragassigned=fgrouped['deltabasedfragassignment'].tolist()
        if score in deltabasedfragassigned:
            
            runningDF=fgrouped[fgrouped['deltabasedfragassignment']==score]
            
            temp_posscore=runningDF[whichmethod].tolist()
            temptotal_posscore=sum(temp_posscore)
            temp_posfrag=len(temp_posscore)
            
            runningDF_TP=runningDF[runningDF['index'].str.contains(ctname)]
            
            tempTP_score=runningDF_TP[whichmethod].tolist()
            tempTP_totalposscore=sum(tempTP_score)
            
            runningDF_FP=runningDF[~runningDF['index'].str.contains(ctname)]
            
            tempFP_score=runningDF_FP[whichmethod].tolist()
            tempFP_totalposscore=sum(tempFP_score)
            
           
            
            #runningDF_FP=

        else:
            temptotal_posscore=0
            temp_posfrag=0

        

        ctposscoredict[ctname].append(temptotal_posscore)
        
        TPposscoredict[ctname].append(tempTP_totalposscore)
        FPposscoredict[ctname].append(tempFP_totalposscore)
        
 
        
        totalcpgdict[ctname].append(runningDF['total_cpg'].sum())
        hypocpgdict[ctname].append(runningDF['LENhypoCpG'].sum())
        hypercpgdict[ctname].append(runningDF['LENhyperCpG'].sum())
        
        
    ctposscoredf=pd.DataFrame.from_dict(ctposscoredict)
    ctposscoredf['Mixture']=fname

    totalcpgdf=pd.DataFrame.from_dict(totalcpgdict)
    totalcpgdf['Mixture']=fname
    
    hypocpgdf=pd.DataFrame.from_dict(hypocpgdict)
    hypocpgdf['Mixture']=fname
    
    hypercpgdf=pd.DataFrame.from_dict(hypercpgdict)
    hypercpgdf['Mixture']=fname
    
    TPposscoreDF=pd.DataFrame.from_dict(TPposscoredict)
    FPposscoreDF=pd.DataFrame.from_dict(FPposscoredict)
    
    TPposscoreDF['Mixture']=fname
    FPposscoreDF['Mixture']=fname
    
    
   
    return ctposscoredf,totalcpgdf,hypocpgdf,hypercpgdf,TPposscoreDF,FPposscoreDF


# In[7]:


filegrouped=allassigned.groupby('filename')

maxscorelist=[]



alltotalcpg=[]
allhypocpg=[]
allhypercpg=[]


TPscorelist=[]
FPscorelist=[]

for name, group in filegrouped:
    #maxscorelist.append(calposscore(group,'maxscore',name))
    #adjustedScore_minuslist.append(calposscore(group,'adjustedScore_minus',name))
    
    r1,r2,r3,r4,r5,r6=calposscore(group,'maxscore',name)
    maxscorelist.append(r1)
    
    alltotalcpg.append(r2)
    allhypocpg.append(r3)
    allhypercpg.append(r4)
    
    TPscorelist.append(r5)
    FPscorelist.append(r6)


# In[8]:


###without weighting by CpG score
maxscoreBeefoeCpGwiightlist=[]
for name, group in filegrouped:
    #maxscorelist.append(calposscore(group,'maxscore',name))
    #adjustedScore_minuslist.append(calposscore(group,'adjustedScore_minus',name))
    
    rbefore1,_,_,_,_,_=calposscore(group,'maxscore_beforeCpGweight',name)
    maxscoreBeefoeCpGwiightlist.append(rbefore1)


# In[9]:


maxscoreBeefoeCpGwightlistDF=pd.concat(maxscoreBeefoeCpGwiightlist)
maxscoreBeefoeCpGwightlistDF.set_index('Mixture',inplace=True)
maxscoreBeefoeCpGwightlistDF.head()


# In[10]:


maxscorelistDF=pd.concat(maxscorelist)
maxscorelistDF.set_index('Mixture',inplace=True)


# In[11]:


maxscorelistDF.head()


# In[12]:


alltotalcpgDF=pd.concat(alltotalcpg)
allhypocpgDF=pd.concat(allhypocpg)
allhypercpgDF=pd.concat(allhypercpg)

alltotalcpgDF.set_index('Mixture',inplace=True)
allhypocpgDF.set_index('Mixture',inplace=True)
allhypercpgDF.set_index('Mixture',inplace=True)


# In[13]:


alltotalcpgDF.to_csv(outfile+"_totalcpg.txt",sep='\t')


# In[14]:


allhypocpgDF.to_csv(outfile+"_hypocpg.txt",sep='\t')


# In[15]:


allhypercpgDF.to_csv(outfile+"_hypercpg.txt",sep='\t')

