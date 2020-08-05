#!/usr/bin/env python
# coding: utf-8

# In[1]:


from scipy.stats import pearsonr
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


####param
import sys
mergedfile=sys.argv[1]  #"data/py_50_merged_gt3.txt"
outname=sys.argv[2]  #mergedfile+"_onefile"
gt_suffix="real"
prdictedlist=["CD14","CD19","CD56","CD4","CD8"] ###
mergeddf=pd.read_csv(mergedfile,sep="\t")


# In[3]:


def genRealList(plist,suffix):
    glist=[]
    for cell in plist:
        glist.append(cell+"_"+suffix)
    return glist


# In[4]:


def gencolums(df,plist,glist):
    r,c=df.shape
    
   
    
    pcolum=[]
    gcolum=[]
    celltype=[]
    
    
    for index in range(len(plist)):
        
        pcolum.append(df[plist[index]].tolist())
        gcolum.append(df[glist[index]].tolist())
        for i in range(r):
            celltype.append(plist[index])
            
        
        
    flatpcolum = [x for sublist in pcolum for x in sublist] 
    flatgcolum= [x for sublist in gcolum for x in sublist] 
    
    return flatpcolum,flatgcolum,celltype
        



def generateonefile(df,plist,glist):
    pcolum,gcolum,celltype=gencolums(df,plist,glist)
    
    dic={"predicted":pcolum,"ground_truth":gcolum,"celltype":celltype}
    resultdf=pd.DataFrame(dic)
    return resultdf
 
    
    


# In[5]:



groundtruthlistList=genRealList(prdictedlist,gt_suffix)
outdf=generateonefile(mergeddf,prdictedlist,groundtruthlistList)
outdf.to_csv(outname,sep="\t",index=False)

