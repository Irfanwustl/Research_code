#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import glob, os
import sys

infolder=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/for_backgroundcalculation/hyper.9/BSseq'
out=sys.argv[2] #infolder+"_avg.txt"


# In[2]:


files = glob.glob(infolder+'/*.txt')
filesdf=[]
for fp in files:
    tmpdf=pd.read_csv(fp,sep="\t")
    tmpdf['filename']=os.path.basename(fp)
    filesdf.append(tmpdf)


# In[3]:


df_combined = pd.concat(filesdf, axis=0)
df_combined.head()


# In[4]:


df_combined.to_csv(out+"_combined.txt",sep='\t',index=False)


# In[5]:


df_combined.mean()


# In[6]:


df_combined.median()


# In[7]:





# In[8]:


set(df_combined['Mixture'].tolist())


# In[9]:


dfbs=df_combined[df_combined['Mixture']=='BS-Seq_07-no-spike_sorted_binnedstats.pkl']
dfbsmean=dfbs.mean()
dfbsmeandf=dfbsmean.to_frame(name='BSseq')


# In[10]:


dfbs.to_csv(out+"_combined_bs.txt",sep='\t',index=False)
#dfbsmean.to_csv(out+"_combined_bs_mean.txt",sep='\t',index=False)


# In[11]:


dfbs.median()


# In[12]:


dfem=df_combined[df_combined['Mixture']=='EM-Seq_07-no-spike_sorted_binnedstats.pkl']
dfemmean=dfem.mean()
dfemmeanDF=dfemmean.to_frame(name='EMseq')


dfem.to_csv(out+"_combined_em.txt",sep='\t',index=False)
#dfemmean.to_csv(out+"_combined_em_mean.txt",sep='\t',index=False)


meaandf=pd.concat([dfbsmeandf,dfemmeanDF],axis=1)

meaandf.to_csv(out+"_mean.txt",sep='\t')











