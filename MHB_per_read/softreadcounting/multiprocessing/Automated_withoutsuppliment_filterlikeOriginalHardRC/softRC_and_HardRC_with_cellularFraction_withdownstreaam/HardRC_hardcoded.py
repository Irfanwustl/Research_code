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
import os

start_time = time.time()

inbinfile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/reproduce_goodmelresult_withHardRC_new_implementation/AUC1fullcohort/BL22_TILAUC1_dummyfull.txt_result_dupindex_binnedstats.pkl'




outfile=sys.argv[2]

scorecolumns=sys.argv[3:]

#######outfile=inbinfile


mincpgLIST=[2,3]

consideringALLheyper=True


inbindf=pd.read_pickle(inbinfile)



#scorecolumns=['CD4-others','CD8-others','nB-others','NK-others','Mn-others','mNeu-others','m8-others','DC-others','Eo-others','Tr-others','m4-others','Mg-others','Er-others','mB-others']


#13ctref
#scorecolumns=['CD4-others','CD8-others','nB-others','NK-others','PC-others','Mn-others','iDC-others','mDC-others','M1-others','M0-others','mN-others','M2-others','cB-others']


#BL22LTME
#scorecolumns=['NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','PC-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others','TIL-others','MelTumor-others']

#CD8TIL_mel_naiveMylid_activated
#scorecolumns=['CD8TIL-others','MelTumor-others','activated-others','NaiveMyloid-others']

#old 3 compartment LTME good SM
#scorecolumns=['PBL-others','TIL-others','MEL_TUMOR-others']


#em4_cm4
#scorecolumns=['cm4-others','em4-others','Tcell-others']



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


allassigned['LENhypoCpG_0.65']=0
allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.65,'LENhypoCpG_0.65']=allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.65,'LENhypoCpG']


# In[12]:


allassigned['LENhypoCpG_0.5']=0
allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.5,'LENhypoCpG_0.5']=allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.5,'LENhypoCpG']


# In[13]:


allassigned.head()


# In[14]:


def hardRC(fgrouped,targetmincpg,cpgpatternratecolumn,fname):
    ctproportiondict=defaultdict(list)
    for score in scorecolumns:
        
     
        
        totalfragments=fgrouped[(fgrouped['deltabasedfragassignment']==score) & (fgrouped['total_cpg']>=targetmincpg)].shape[0]
        positivefragments=fgrouped[(fgrouped['deltabasedfragassignment']==score) & (fgrouped[cpgpatternratecolumn]>=targetmincpg)].shape[0]
        

        

        
        if totalfragments==0:
            tempctproportion=0
        
        else:
            tempctproportion=1.0*positivefragments/totalfragments
        
        ctname=score.replace('-others','')
        
        ctproportiondict[ctname].append(tempctproportion)
        
    ctproportionDF=pd.DataFrame.from_dict(ctproportiondict)
    
    ctproportionDF['Mixture']=fname
        
    return  ctproportionDF
    
  


# In[15]:


filegrouped=allassigned.groupby('filename')

for mincpg in mincpgLIST:
    allfileresultfiftypercent=[]
    allfileresultsixtyfivepercent=[]
    allfileresulteightypercent=[]
    for name, group in filegrouped:
        allfileresultfiftypercent.append(hardRC(group,mincpg,'LENhypoCpG_0.5',name))
        allfileresultsixtyfivepercent.append(hardRC(group,mincpg,'LENhypoCpG_0.65',name))
        allfileresulteightypercent.append(hardRC(group,mincpg,'LENhypoCpG_0.8',name))
        
        
        
     

    allfileresultfiftypercentDF=pd.concat(allfileresultfiftypercent)
    allfileresultfiftypercentDF.set_index('Mixture',inplace=True) 
    
    allfileresultsixtyfivepercentDF=pd.concat(allfileresultsixtyfivepercent)
    allfileresultsixtyfivepercentDF.set_index('Mixture',inplace=True) 
    
    
    allfileresulteightypercentDF=pd.concat(allfileresulteightypercent)
    allfileresulteightypercentDF.set_index('Mixture',inplace=True)
    
    
    
    allfileresultfiftypercentDF.to_csv(outfile+"_pattern"+".5_mincpg"+str(mincpg)+"_CSxOut.txt",sep="\t")
    
    allfileresultsixtyfivepercentDF.to_csv(outfile+"_pattern"+".65_mincpg"+str(mincpg)+"_CSxOut.txt",sep="\t")
    
    allfileresulteightypercentDF.to_csv(outfile+"_pattern"+".8_mincpg"+str(mincpg)+"_CSxOut.txt",sep="\t")
    


# In[16]:


end_time = time.time()

time_elapsed = (end_time - start_time)

#print(time_elapsed)

