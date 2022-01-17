#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from collections import defaultdict
import sys
import time
start_time = time.time()

infile=sys.argv[1] #"/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/B22withLTME/v3_3steps/thirdstepanalysis/try3/naive_myloid_CD8TIL_OthermeanIINTWITH_melCD8TIL_activatted-.5_intwith_CD8tilmel-.9"


outfile=sys.argv[2] #infile


##########when WG just chrom start, else chrom start end
indf=pd.read_csv(infile,sep="\t",index_col=['chrom','start','end']) #############



indf.head()


# In[2]:


negindf=-1*indf
negindf.head()


# In[3]:


alldelta=[.05,.1,.2,.3,.4,.5,.6,.7,.8,0.9]


# In[4]:


scorecolumns=negindf.columns


# In[5]:


celltypeStats=defaultdict(list)

allindex=defaultdict(list)
for score in scorecolumns:

    for delta in alldelta:
        tmpdf=negindf[negindf[score]>=delta]
        allindex[delta]=allindex[delta]+tmpdf.index.tolist()
        
        celltypeStats[score]=celltypeStats[score]+[tmpdf.shape[0]]
        
        
    


# In[6]:


celltypeStatsdf=pd.DataFrame.from_dict(celltypeStats, orient='index',columns=alldelta)
celltypeStatsdf.index.name = 'Celltype'
celltypeStatsdf.head()


# In[7]:


celltypeStatsdf.to_csv(outfile+"_stats.txt",sep="\t")


# In[8]:


alluniqueindexlen=defaultdict(list)
for key in allindex:
    alluniqueindexlen[key].append(len(set(allindex[key]))) 


# In[9]:


alluniqueindexlen


# In[10]:


alluniqueindexlendf=pd.DataFrame.from_dict(alluniqueindexlen)
alluniqueindexlendf.head()


# In[11]:


alluniqueindexlendf.to_csv(outfile+"_uniquecpgs.txt",sep="\t")


# In[12]:


end_time = time.time()

time_elapsed = (end_time - start_time)

print(time_elapsed)

