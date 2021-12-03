#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import os

import sys

infol=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/softRD_pileup/cd4bams_softRDpileup/forbin'

suffix='posscore.txt'

posscorefiles=glob.glob(infol+"/*"+suffix)

posscorefiles


# In[2]:



outdflist=[]
for posscorefile in posscorefiles:
    currentdf=pd.read_csv(posscorefile,sep="\t")
    
    currentdf['Mixture']=os.path.basename(posscorefile)
    
   

    outdflist.append(currentdf)
    


# In[3]:


outdf=pd.concat(outdflist)
outdf=outdf.set_index('Mixture')
outdf.to_csv(infol+"_"+suffix+"_CSxOut.txt",sep="\t")

