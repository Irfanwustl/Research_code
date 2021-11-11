#!/usr/bin/env python
# coding: utf-8

# In[1]:


###worksfor hypo only as calculated for 'confidence' 

import pandas as pd
from statistics import mean
import time
import sys

#start_time = time.time()


smfile=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/BL14_all_matrixCin_nr0.4_imputed_rowmean.txt_bg_intesectedwith_CD4DMRofBL14atleast.2SM.txt_formatted.txt'
finalfile=sys.argv[2] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/CD4allrange_NR_1000000_insilmix60_sorted_howsm_single_mode_pp_masterdf.txt_rej-99999.0_mincpg1_rejmode_nov_final.txt'
outfile=sys.argv[3]

smdf=pd.read_csv(smfile,sep="\t")
finaldf=pd.read_csv(finalfile,sep="\t")
celltype=sys.argv[4] #'CD4'
smdf.head()


# In[2]:


set(finaldf['finalrejectedfor'].tolist())


# In[3]:


finaldf=finaldf[(finaldf['finalacceptedfor']==celltype) | (finaldf['finalrejectedfor'].str.contains(celltype))]


# In[4]:


preveresult=finaldf[finaldf['finalacceptedfor']==celltype].shape[0]/finaldf.shape[0]
preveresult


# In[5]:


finaldf.shape


# In[6]:


finaldf.to_csv(outfile+"_informative.txt",sep="\t",index=False)


# In[7]:


finaldf.head()


# In[8]:



finaldf['acceptedCpG']=finaldf.acceptedCpG.apply(lambda x: x[1:-1].split(','))
finaldf['notacceptedCpG']=finaldf.notacceptedCpG.apply(lambda x: x[1:-1].split(','))
finaldf['mismatchCpG']=finaldf.mismatchCpG.apply(lambda x: x[1:-1].split(','))

finaldf['nonnormalized_thatct_proportion']=-1
finaldf['nonnormalized_otherct_proportion']=-1
finaldf['normalized_thatct_proportion']=-1
finaldf['normalized_otherct_proportion']=-1

finaldf['#CpG']=-1
finaldf['confidence']=-1
finaldf.head()


# In[9]:


def processrow(aindex,arow):
   
    notacceptedCpGList=arow['notacceptedCpG']
    acceptedCpGList=arow['acceptedCpG']
    thatctproblist=[]
    otherproblist=[]
    
    confidencelist=[]

    for notacceptedCpG in notacceptedCpGList:
  
        if not eval(notacceptedCpG):
            continue
        chrom,start=eval(notacceptedCpG).split(':')
        corressSMrow=smdf[(smdf['chrom']==chrom) & (smdf['start']==int(start))]
        if corressSMrow.shape[0]!=1:
            print("sm problem. Exiting")
            sys.exit(1)
        thatctprob=(corressSMrow[celltype]).tolist()[0]
        otherprob=(corressSMrow['othermean']).tolist()[0]
        
        
 
        thatctprob=thatctprob/(thatctprob+otherprob)
        otherprob=otherprob/(thatctprob+otherprob)
        
        thatctproblist.append(thatctprob)
        otherproblist.append(otherprob)
        
        confidencelist.append(abs(corressSMrow[celltype+"-othermean"].tolist()[0]))
    for acceptedCpG in acceptedCpGList:
        
        if not eval(acceptedCpG):
            continue
        
        chrom,start=eval(acceptedCpG).split(':')
        corressSMrow=smdf[(smdf['chrom']==chrom) & (smdf['start']==int(start))]
        if corressSMrow.shape[0]!=1:
            print("sm problem. Exiting")
            sys.exit(1)
        thatctprob=(corressSMrow['1-'+celltype]).tolist()[0]
        otherprob=(corressSMrow['1-othermean']).tolist()[0]
        thatctprob=thatctprob/(thatctprob+otherprob)
        otherprob=otherprob/(thatctprob+otherprob)
        
        thatctproblist.append(thatctprob)
        otherproblist.append(otherprob)
        
        confidencelist.append(abs(corressSMrow[celltype+"-othermean"].tolist()[0]))
    
    totalcpg=len(thatctproblist)
    finaldf.loc[aindex,'#CpG']=totalcpg
    
    if totalcpg==0:  ###how many times it is happening and why? Is the problem in RD or masterDF? consider for the final result
        return
    

    finalthatctprob=mean(thatctproblist)
    finalotherctprob=mean(otherproblist)
    
    finalconfidence=mean(confidencelist)
    
    
    finaldf.loc[aindex,'nonnormalized_thatct_proportion']=finalthatctprob
    finaldf.loc[aindex,'nonnormalized_otherct_proportion']=finalotherctprob
    finaldf.loc[aindex,'confidence']=finalconfidence
    
    


# In[10]:


for index, row in finaldf.iterrows():
    

    processrow(index, row)
    
    


# In[11]:


finaldf.head()


# In[18]:


finaldf['normalized_thatct_proportion']=finaldf['nonnormalized_thatct_proportion']/(finaldf['nonnormalized_thatct_proportion']+finaldf['nonnormalized_otherct_proportion'])
finaldf['normalized_otherct_proportion']=finaldf['nonnormalized_otherct_proportion']/(finaldf['nonnormalized_thatct_proportion']+finaldf['nonnormalized_otherct_proportion'])
finaldf['normalized_thatct_proportion_cpgWeighted']=finaldf['normalized_thatct_proportion']*finaldf['#CpG']
finaldf.head()


# In[24]:


justresult=finaldf['normalized_thatct_proportion'].mean()
fragweightedresult=finaldf['normalized_thatct_proportion_cpgWeighted'].sum()/finaldf['#CpG'].sum()

resultdf=pd.DataFrame({'justresult':[justresult],'fragweightedresult':[fragweightedresult]})
resultdf.to_csv(outfile+"_softRD_result.txt",sep="\t",index=False)


# In[25]:


finaldf.to_csv(outfile+"_softRD.txt",sep="\t",index=False)


# In[13]:




