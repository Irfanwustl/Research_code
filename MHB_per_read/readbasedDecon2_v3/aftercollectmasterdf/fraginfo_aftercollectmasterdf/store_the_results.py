#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob, os


# In[2]:

import sys

result_folder=sys.argv[1] #"/Users/irffanalahi/Research/weekly/for_10_8_20/faltutryRnadomAgain/allpblsubset/runhere/outfolder/relativelonglist"#"/Users/irffanalahi/Research/Research_code/MHB_per_read/ReadBasedDecon/data/resultfolder"
outname=sys.argv[2] #result_folder+".txt"


# In[3]:


files = glob.glob(result_folder+'/*.txt')
#print (files)


# In[4]:


df = pd.concat([pd.read_csv(fp,sep="\t").assign(Mixture=os.path.basename(fp)) for fp in files])


# In[5]:


df=df.set_index('Mixture')
df.to_csv(outname,sep="\t",na_rep="NA")
#print("done")

