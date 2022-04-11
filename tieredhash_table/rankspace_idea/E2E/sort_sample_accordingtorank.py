#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import glob
import sys

inputfol=sys.argv[1] #'BL22promfolder_int_rankedbasedtry1'
indexfol=sys.argv[2] #'rankedbasedtry1'

outdir=sys.argv[3] #inputfol+"_sortedby_"+os.path.basename(indexfol)
os.mkdir(outdir)


# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[3]:


inputfiles=listdir_nohidden(inputfol)
indexfiles=listdir_nohidden(indexfol)


# In[4]:


for indexfile in indexfiles:
    res = [i for i in inputfiles if os.path.basename(indexfile) in i]
   
    
    if len(res)!=1:
        print("error")
        sys.exit(1)
        
    indexdf=pd.read_csv(indexfile,sep="\t",header=None)
    indexdf.rename(columns={0:'chrom',1:'start',2:'end'},inplace=True)
    indexdf.set_index(['chrom','start','end'],inplace=True)
    resdf=pd.read_csv(res[0],sep="\t",index_col=['chrom','start','end'])
    
    
    
    


    
    if indexdf.shape[0]!=resdf.shape[0]:
        print("error2")
        sys.exit(1)
    
    sortedres=resdf.reindex(indexdf.index)
    
    sortedres.to_csv(outdir+"/"+os.path.basename(res[0])+"_sorted.txt",sep="\t",na_rep='NA')
    
    

