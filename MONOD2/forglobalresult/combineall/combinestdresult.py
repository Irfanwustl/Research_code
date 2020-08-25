#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import os.path 


# In[2]:

import sys
path = sys.argv[1]  #"/Users/irffanalahi/Research/Research_code/gitignorefolder/dataformonod2analysis/test/toy" # use your path

outfilename=sys.argv[2]  #"/Users/irffanalahi/Research/Research_code/gitignorefolder/dataformonod2analysis/test/toyout"

all_files = glob.glob(path + "/*std")


# In[3]:


li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=0, header=None,sep="\t")
    df = df.rename(columns={1: os.path.basename(filename),2:"cpg" })
    
    df=df.drop("cpg",axis=1)
   
    li.append(df)

frame = pd.concat(li, axis=1)

frame.to_csv(outfilename+"withna.txt",sep="\t",na_rep='NA')


# In[4]:


outdf=frame.dropna()
outdf.to_csv(outfilename+"nona.txt",sep="\t")

