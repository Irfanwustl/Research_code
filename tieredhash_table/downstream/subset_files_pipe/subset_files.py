#!/usr/bin/env python
# coding: utf-8

# In[62]:


import pandas as pd
import os
import numpy as np
import time
import sys


# In[63]:


fol = sys.argv[1] #'PMN_thresholdpos_allthresholdcombinations'
outfol = fol + '_subset'
files = os.listdir(fol)
cutoff = 100
cpgs = 2
os.mkdir(outfol)


# In[64]:


def subset(file):
    path = fol + '/' + file
    data = pd.read_csv(path, sep='\t', header=None, names=['Chrom', 'Start', 'End'])
    df = pd.DataFrame(data)
    df_new = pd.DataFrame(columns=list(df.columns))
    for ch in np.unique(df['Chrom']):
        df_ch = df[df['Chrom'] == ch]
        for i in df_ch.index:
            start = df_ch.at[i, 'Start']
            low = int(start) - cutoff
            high = int(start) + cutoff
            df_sub = df_ch[(df_ch['Start'] > low) & (df_ch['Start'] < high)]
            if len(df_sub) >= cpgs:
                df_new = df_new.append(df_ch[df_ch['Start'] == start])
    df_new.to_csv(outfol + '/' + file, sep='\t', index=None,header=None)


# In[65]:


from joblib import Parallel, delayed
start_time = time.time()
results = Parallel(n_jobs=-1)(delayed(subset)(file) for file in files)
print(time.time() - start_time)


# In[ ]:




