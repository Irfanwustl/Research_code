#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import os
import time
import sys
start_time = time.time()

infol=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/softRD_pileup/CD4mixture_output_81205_sorted_softMultiprocessing'

outprefix=sys.argv[2]

suffix=sys.argv[3]  #'binnedstats.pkl'

allstatfiles=glob.glob(infol+"/*"+suffix)





# In[2]:


filesdf=[]
for fp in allstatfiles:
    tmpdf=pd.read_pickle(fp)
    tmpdf['filename']=os.path.basename(fp)
    filesdf.append(tmpdf)


# In[3]:


df_combined = pd.concat(filesdf, axis=0)
df_combined.head()


# In[4]:


df_combined.shape


# In[5]:


nodupindex = df_combined[~df_combined.index.duplicated(keep='first')]


# In[6]:


nodupindex.shape


# In[7]:


df_combined.to_pickle(outprefix+"_dupindex_"+suffix)
nodupindex.to_pickle(outprefix+"_nodupindex_"+suffix)


# In[8]:


end_time = time.time()

time_elapsed = (end_time - start_time)

print(time_elapsed)

