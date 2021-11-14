#!/usr/bin/env python
# coding: utf-8

# In[1]:



import pandas as pd
import glob, os
import sys



infolder=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/try2"
outname=sys.argv[2]

celltype=sys.argv[3] #"CD4"
files = glob.glob(infolder+'/*softRD_result.txt')
df = pd.concat([pd.read_csv(fp,sep="\t").assign(Mixture=os.path.basename(fp)) for fp in files])
df=df.set_index('Mixture')
df.head()


# In[2]:


colnames=df.columns.tolist()
for cname in colnames:
    
    tempdf=(df[cname]).to_frame(name=celltype)
    tempdf.to_csv(outname+"/"+'result_'+cname+"_CSxOut.txt",sep="\t")
  

