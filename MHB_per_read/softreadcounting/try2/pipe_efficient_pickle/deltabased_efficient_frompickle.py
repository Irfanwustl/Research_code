#!/usr/bin/env python
# coding: utf-8

# In[1]:


###worksfor hypo only as calculated for 'confidence' 

#### need to handle, low mapq and dup

import pandas as pd
from statistics import mean
import time
import numpy as np
from collections import defaultdict
import sys

smfile=sys.argv[1]  #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/try2/try2_efficient/BL14_all_matrixCin_nr0.4_imputed_rowmean.txt_bg_intesectedwith_CD4DMRofBL14atleast.2SM_g1_CD4_3_g2_others_33.txt_othermean.txt'
finalfile=sys.argv[2] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/try2/try2_efficient/testempty.txt'

outpath=sys.argv[3]


acccol='hypolist'
noACCcol='hyperlist'

smdf=pd.read_csv(smfile,sep="\t",index_col=['position'])
finaldf=pd.read_pickle(finalfile)

finaldf=finaldf[~finaldf['assignedcelltype'].isin(['lowmapq', 'DupRead'])]

deltagreaterforpositive=0  ##############>0

deltasmallerfornegative=0 ############<0

smdf.head()


# In[2]:



allcolumns=smdf.columns.tolist()
allcollength=len(allcolumns)


allct=[item for item in allcolumns if '-others' not in item]
allctlen=len(allct)

if allcollength!=2*allctlen:
    print('wrong all ct inferred. EXITING')
    sys.exit(1)


# In[3]:


finaldf['#CpG']=-1

finaldf['deltabasedfragassignment']='NotAssigned'

score_columns=[]
for ct in allct:
    tempscorecol=ct+'-others'
    finaldf[tempscorecol]='NotAssigned'
    score_columns.append(tempscorecol)
finaldf.head()


# In[4]:









def deltacalculation(cpgsfordelta):
    
    
    
    deltafortheseCpGS=cpgsfordelta[score_columns].sum(axis=0)

    return deltafortheseCpGS



def processrow(aindex,arow):
   

    notacceptedCpGList=arow[noACCcol]
        

    acceptedCpGList=arow[acccol]
    

    
    
    
    
    accindex=smdf.index.intersection(acceptedCpGList) #acceptedCpGList ##### 
    
    

    
    
    
    
    ACCscore=0
    if len(accindex)>0:
        corresACCcpgs=(smdf.loc[accindex])*-1 
        ACCscore=deltacalculation(corresACCcpgs)
    

  
    
    rejindex=smdf.index.intersection(notacceptedCpGList)  #notacceptedCpGList ##########
    

    
    
    
    REJscore=0
    if len(rejindex)>0:
        corresREJcpgs=smdf.loc[rejindex]
        
        REJscore=deltacalculation(corresREJcpgs)
    

    
    finalscore=ACCscore+REJscore
    


    
    finaldf.loc[index,score_columns]=finalscore #.iloc[0]
 
    
    totalcpgs=len(accindex)+len(rejindex)
    
    finaldf.loc[index,'#CpG']=totalcpgs


# In[5]:


for index, row in finaldf.iterrows():
    

    processrow(index, row)


# In[6]:


finaldf.head()


# In[7]:



finaldf=finaldf[finaldf['#CpG']>0]

finaldf.head()


# In[8]:



ctpropdict= defaultdict(list)


for score in score_columns:
    

    
    posscore=finaldf.loc[finaldf[score]>deltagreaterforpositive,score]
    
    negscore=finaldf.loc[finaldf[score]<deltasmallerfornegative,score]
    
    
    
    poscpg=(finaldf.loc[finaldf[score]>deltagreaterforpositive,'#CpG']).sum()
    negcpg=(finaldf.loc[finaldf[score]<deltasmallerfornegative,'#CpG']).sum()
    
    
    poslen=len(posscore)
    neglen=len(negscore)
    
    posscoreSUM=sum(posscore)
    negscoreSUM=sum(negscore)
    
    
    
    ct_posnegscore=posscoreSUM/(posscoreSUM+abs(negscoreSUM))
    
    
    if poscpg>0:
        ct_posscorebyposcpg=posscoreSUM/poscpg
    else:
        ct_posscorebyposcpg=0
    
    ct_posscorebyallcpg=posscoreSUM/(poscpg+negcpg)
    
    ct_fragscore=poslen/(poslen+neglen)
    
    
    ctname=score.replace('-others','')
    
    ctpropdict[ctname+"_posnegscore"].append(ct_posnegscore)
    ctpropdict[ctname+"_posscorebyposcpg"].append(ct_posscorebyposcpg)
    ctpropdict[ctname+"_posscorebyallcpg"].append(ct_posscorebyallcpg)
    ctpropdict[ctname+"_fragscore"].append(ct_fragscore)
    
    
    
    
    
    


# In[9]:


ctpropdf=pd.DataFrame.from_dict(ctpropdict)
ctpropdf.to_csv(outpath+"_softRD_result.txt",sep="\t",index=False)


# In[10]:


finaldf.to_pickle(outpath+"_softRD.pkl")




