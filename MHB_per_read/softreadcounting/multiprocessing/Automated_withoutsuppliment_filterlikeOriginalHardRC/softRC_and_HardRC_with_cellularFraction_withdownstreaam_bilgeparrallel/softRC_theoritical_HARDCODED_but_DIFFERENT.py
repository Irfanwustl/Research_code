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



###should be the final one###
inbinfile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/largerEXP/spike_EXP/cellularfraction/ThatMaxScoreIdea/consider_pending2/withheldoutSM/heldoutvalue_again/allct_towardsSM_dummy_mean_SM.txt_unique_withmincol.txtEPCAM_mean_SM_top1000_heldoutvalue.txt_result_dupindex_binnedstats.pkl_FINAL_binnedstats.pkl'
softCresult=sys.argv[2] #'/Users/irffanalahi/Research/Research_update/SoftRD/largerEXP/spike_EXP/cellularfraction/ThatMaxScoreIdea/consider_pending2/withheldoutSM/heldoutvalue_again/allct_towardsSM_dummy_mean_SM.txt_unique_withmincol.txtEPCAM_mean_SM_top1000_heldoutvalue.txt_result_dupindex_binnedstats.pkl_maxscore_CSxOut.txt'
smfile=sys.argv[3] #'/Users/irffanalahi/Research/Research_update/SoftRD/largerEXP/spike_EXP/cellularfraction/ThatMaxScoreIdea/consider_pending2/withheldoutSM/heldoutvalue_again/allct_towardsSM_dummy_mean_SM.txt_unique_withmincol.txtEPCAM_mean_SM_top1000_heldoutvalue.txt'
outfile=sys.argv[4] #inbinfile

scorecolumns=sys.argv[5:]


consideringALLheyper=True


inbindf=pd.read_pickle(inbinfile)
####BL22withEPCAM#####
#scorecolumns=['NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others','EPCAM-others']


####BL22#####
#scorecolumns=['NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','PC-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others']


#scorecolumns=['em4-others']

#scorecolumns=['EPCAM-others']

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
    
   # print(scorecolumns)



    for score in scorecolumns:
       # print(score)
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
            tempTP_totalposscore=0
            tempFP_totalposscore=0

        

        ctposscoredict[ctname].append(temptotal_posscore)
        
        TPposscoredict[ctname].append(tempTP_totalposscore)
        FPposscoredict[ctname].append(tempFP_totalposscore)
        
 
        try:
            totalcpgdict[ctname].append(runningDF['total_cpg'].sum())
        except:
            #means this is not in deltabasedfragassigned
            totalcpgdict[ctname].append(1)

        try:

            hypocpgdict[ctname].append(runningDF['LENhypoCpG'].sum())
        except:
            #means this is not in deltabasedfragassigned
            hypocpgdict[ctname].append(0)
        
        try:
            hypercpgdict[ctname].append(runningDF['LENhyperCpG'].sum())
        except:
            #means this is not in deltabasedfragassigned
            hypercpgdict[ctname].append(0)

        
        
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


alltotalcpgDF.head()


# In[14]:


allhypocpgDF.head()


# In[15]:


allhypercpgDF.head()


# In[16]:



smdf=pd.read_csv(smfile,sep="\t",index_col=['chrom','start'])
smdf.head()


# In[17]:


smdf['mincolname']=smdf.idxmin(axis=1)
grouped=smdf.groupby('mincolname')
outlist=defaultdict(list)
for name, group in grouped:
    tempct=name.replace('-others','')
    outlist[tempct].append(group.shape[0])
outdf=pd.DataFrame.from_dict(outlist,orient='index',columns=['#CpG'])
outdf.index.name='Celltype'
outdf.head()


# In[18]:


smdfPMN=smdf[smdf['mincolname']=='EPCAM-others']
smdfPMN.shape


# In[19]:


#alltotalcpgDF['EPCAM']


# In[20]:


#allhypocpgDF['EPCAM']


# In[21]:


###prepare maxpossible score###
from scipy.stats import binom
def maxpossiblescore(fgroupedTotalCpG,fname,smwithmincol):
    ctposscoredict= defaultdict(list)
    
    
    for score in scorecolumns:
        ctname=score.replace('-others','')
        
        currenttotalCpG=fgroupedTotalCpG[ctname] ###############check. needs to be float, not series
       
        
        corressSM=smwithmincol[smwithmincol['mincolname']==score]
        corressampled=corressSM.sample(n=int(currenttotalCpG),replace=True)
        
        corressscore=-1*corressampled[score].sum()
        
        ctposscoredict[ctname].append(corressscore)
        
        
        
        
        ####tryung to include binomial. Not working yet#####
        '''
        prob = 1 - binom.cdf(0, currenttotalCpG, 0.001)
        expectedCpG=prob*currenttotalCpG
        print(prob)
        print(expectedCpG)
        print(currenttotalCpG)
        sys.exit(1)
        '''
        
        
        
        
        
        
        
    ctposscoredf=pd.DataFrame.from_dict(ctposscoredict)
    ctposscoredf['Mixture']=fname
    
   

    
   
    return ctposscoredf


# In[22]:





maxscorepossible=[]


    
for index, row in alltotalcpgDF.iterrows():
    maxscorepossible.append(maxpossiblescore(row,index,smdf))

maxscorepossibleDF=pd.concat(maxscorepossible)
maxscorepossibleDF.set_index('Mixture',inplace=True)


#maxscorepossibleDF['EPCAM']
 


# In[23]:


maxscorepossibleDF.head()


# In[24]:



softCresultDF=pd.read_csv(softCresult,sep='\t',index_col=0)
softCresultDF.head()


# In[25]:


resultpredicetdfrommaxscore=softCresultDF/maxscorepossibleDF*100
resultpredicetdfrommaxscore.to_csv(outfile,sep='\t')


# In[26]:


#resultpredicetdfrommaxscore_usingbeforecpgweight=maxscoreBeefoeCpGwightlistDF/maxscorepossibleDF*100
#resultpredicetdfrommaxscore_usingbeforecpgweight.to_csv(inbinfile+"_maxscorebased_ct_withoutCpGweight.txt",sep='\t')


# In[27]:


maxscoreBeefoeCpGwightlistDF.head()


# In[28]:


maxscorepossibleDF.head()

