#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ruptures as rpt  # our package
from ruptures.metrics import hausdorff
import pandas as pd
import concurrent.futures
import sys
infile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/ITGAE_patternrecognition/changepointtest/preproocess_Develop/ITGAEandERICH1_cin_nr0.5_imputed_rowmean.txt_compdeltafor_CD8TIL.txt"
minCpG=3
outfile=infile+"_mincpg_"+str(minCpG)+"pelt.txt"
penalty_value = 1 
indf=pd.read_csv(infile,sep="\t",index_col=0)

indf.head()


# In[2]:


def segment_generator():
    allindex=indf.index.tolist()
    allindexchrom=list(set([i.split(':', 1)[0] for i in allindex]))
    segmentlist=[]
    for indexchrom in allindexchrom:
        segmentlist.append(indf[indf.index.str.contains(indexchrom)])
    
    return segmentlist
def pelt_result(signal_pelt):
    algo_python = rpt.Pelt(model="rbf", jump=1, min_size=minCpG).fit(signal_pelt)
    bkps_python = algo_python.predict(pen=penalty_value)
    forindexgenerate=bkps_python
    if forindexgenerate[-1]==len(signal_pelt.index):
        forindexgenerate[-1]=forindexgenerate[-1]-1
    return (signal_pelt.index[forindexgenerate]).tolist()


# In[3]:


signallist=segment_generator()
multiresult = []

with concurrent.futures.ProcessPoolExecutor() as executor:
    processlist=[]
    for signal in signallist:
        processlist.append(executor.submit(pelt_result,signal))
        #algo_python = rpt.Pelt(model="rbf", jump=1, min_size=minCpG).fit(signal)  # written in pure python
    for process in concurrent.futures.as_completed(processlist):
        multiresult.append(process.result())


# In[4]:


flat = [x for sublist in multiresult for x in sublist]

with open(outfile, 'w') as f:
    for item in flat:
        f.write("%s\n" % item)

