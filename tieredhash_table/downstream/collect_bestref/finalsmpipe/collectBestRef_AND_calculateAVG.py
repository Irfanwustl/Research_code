#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import os
import sys
import shutil

bestreffile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/BL22_groupv2/All/Alllinked/fromBilge/allct_subset_linecount_txt_filelist.txt'


groupnumber=int(sys.argv[2])  #4
#####it can be both position and final SM like locations
locationofrefs=sys.argv[3]   #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/BL22_groupv2/All/Alllinked/towardsFinalRef/input'
outdir=sys.argv[4]     #locationofrefs+"_bestref"
os.mkdir(outdir)

bestreffiledf=pd.read_csv(bestreffile,sep='\t')
bestreffiledf.head()


# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[3]:


locationofrefSubDir=listdir_nohidden(locationofrefs)
len(locationofrefSubDir)


# In[28]:


def combinedelta(samectfile,currentCT):
    allsamect=[]
    for asctfile in samectfile:
        tdf=pd.read_csv(asctfile,sep='\t',index_col=['chrom','start','end'])
        allsamect.append(tdf)
    
    
    allsamectDF=pd.concat(allsamect,axis=1)
    allsamectDF=allsamectDF[[currentCT+'-others']]
    allsamectDFmean=allsamectDF.mean(axis=1)
    allsamectDFmean=allsamectDFmean.to_frame(name=currentCT+'-others')
    
    allsamectDFmin=allsamectDF.min(axis=1)
    
    allsamectDFmin=allsamectDFmin.to_frame(name=currentCT+'-others')
    
    allsamectDFmax=allsamectDF.max(axis=1)
    allsamectDFmax=allsamectDFmax.to_frame(name=currentCT+'-others')
    
    
    allsamectDFmean.to_csv(outdir+"/"+currentCT+"_mean",sep='\t')
    allsamectDFmin.to_csv(outdir+"/"+currentCT+"_min",sep='\t')
    allsamectDFmax.to_csv(outdir+"/"+currentCT+"_max",sep='\t')
    
    
   


# In[31]:


for asubdir in locationofrefSubDir:
    whichct=os.path.basename(asubdir).split('_')[0]
    
    
    
    
    corressbestref=bestreffiledf[bestreffiledf['Cells']==whichct]['Files'].tolist()[0]
    
    
    
    
    allfiles=listdir_nohidden(asubdir)
    
    
    
    
    matching = [s for s in allfiles if corressbestref in s]
    
    
    if len(matching)!=groupnumber:
        print(len(matching))
        print("Error.Exit")
        sys.exit(1)
        
    #################
    
    combinedelta(matching,whichct)
    
    
    
   


# In[ ]:


print('done')

