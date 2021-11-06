#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import glob
import sys

grandfatherfolder=sys.argv[1]  #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/ReadBaseddeocn10/sm_bamreadysorted_globalout'

outfolderWCP=grandfatherfolder+"_weightedCellProportion_mincpg1"
os.mkdir(outfolderWCP)


outfolderWFrag=grandfatherfolder+"_weightedFragment_mincpg1"
os.mkdir(outfolderWFrag)



# In[2]:


allsmresult=[x[0] for x in os.walk(grandfatherfolder)]

allsmresult.remove(grandfatherfolder)


# In[3]:


for smresult in allsmresult:
   
    resultfile=glob.glob(smresult+"/*"+"weightedCellProportion_mincpg1.txt")
    
    resultdf = pd.concat([pd.read_csv(fp,sep="\t").assign(Mixture=os.path.basename(fp)) for fp in resultfile])
    resultdf=resultdf.set_index('Mixture')
    
    resultdf.to_csv(outfolderWCP+"/"+os.path.basename(smresult)+'_weightedCellProportion_mincpg1_CSxOut.txt',sep="\t")
    
    
    
    resultWF=glob.glob(smresult+"/*"+"weightedFragmentResult_mincpg1.txt")
    resultWFdf=pd.concat([pd.read_csv(fp,sep="\t").assign(Mixture=os.path.basename(fp)) for fp in resultWF])
    resultWFdf=resultWFdf.set_index('Mixture')
    resultWFdf.to_csv(outfolderWFrag+"/"+os.path.basename(smresult)+'_weightedFragmentResult_mincpg1_CSxOut.txt',sep="\t")
    
    

