#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from scipy.stats import pearsonr
import os



# In[2]:


#param
import sys
allinonefile=sys.argv[1] #"data/diffDataExpanded_SigMatrixpy_g50Onlyposition_intersected_cyberin_scaled_inverted_selectedinverted_CSxOut.txt_rendata_gt3.txt_oneline"
gtpath=sys.argv[2] #"dummyfolder/gtfolder"
allgtlist=[f for f in os.listdir(gtpath) if not f.startswith('.')] #["blueprint_rein_our_pbmc_puregt.txt","rendata_gt3.txt"]
gtfilename=sys.argv[3] #"rendata_gt3.txt"
purgtfilename=["blueprint_rein_our_pbmc_puregt.txt","blueprint_puregt.txt","our_pbmc_puregt.txt","rein_puregt.txt"]
masterfilename=sys.argv[4] #"data/Masterperf.txt"
allinonedf=pd.read_csv(allinonefile,sep="\t")
#print(allgtlist)


# In[3]:


def metric_for_mixture(df):
    corr = pearsonr(df['ground_truth'], df['predicted'])
    return corr[0]


# In[4]:


def metric_for_pure(df):
    diff=df['ground_truth']-df['predicted']
    
    
    result=1-(diff.abs()).mean()
    return result


# In[5]:


def savetomastermat(df,gtfilename,purgtfilename,masterperf,dffilename):
    
    
    if gtfilename in purgtfilename:
        metric=metric_for_pure(df)
    else:
        metric=metric_for_mixture(df)
        
        
    smname=os.path.basename(dffilename)
    
    smname,sep, tail=smname.partition('_CSxOut')
    
    if os.path.exists(masterperf):
        masterperfdf=pd.read_csv(masterperf,sep="\t")
        
        
        if smname in masterperfdf["Sm"].tolist():
            
            
            masterperfdf.loc[masterperfdf["Sm"]==smname,gtfilename]=metric

        
        else:
            
            dic={}
            dic["Sm"]=smname

            for cl in allgtlist:
                dic[cl]="NA"


            masterperfdf=masterperfdf.append(dic,ignore_index=True)

            masterperfdf.loc[masterperfdf["Sm"]==smname,gtfilename]=metric
        
        
    else:
        masterperfdf=pd.DataFrame(columns=["Sm"]+allgtlist)
        dic={}
        dic["Sm"]=smname
        
        for cl in allgtlist:
            dic[cl]="NA"
            
        
        masterperfdf=masterperfdf.append(dic,ignore_index=True)
        
       
        masterperfdf.loc[masterperfdf["Sm"]==smname,gtfilename]=metric
        

        
        
        
      
    masterperfdf.to_csv(masterperf,sep="\t",index=False)


# In[6]:


savetomastermat(allinonedf,gtfilename,purgtfilename,masterfilename,allinonefile)

