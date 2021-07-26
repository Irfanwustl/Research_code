#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob, os
import seaborn as sns; sns.set()
#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import sys

infolder=sys.argv[1] #"/Users/irffanalahi/Research/Research_update/SM/ShowcaseSM/BL19_V2/forfig/myversion/BL19v2metin_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.6"
celllist=['CD4','em4','cm4','Tr','CD8','cm8','em8','ed8','nB','cB','mB','NK','Mn','Macs','mNeu','DC','Eo','Mg','Er']


# In[2]:


files = glob.glob(infolder+'/*.txt')
key = {next((s for s in files if v in s), None): i for i, v in enumerate(celllist)}
files=sorted(files, key=key.get)
#files


# In[3]:


filesdf=[pd.read_csv(fp,sep="\t") for fp in files]


# In[4]:


df_combined = pd.concat(filesdf, axis=0,sort=False)
df_combined.head()


# In[5]:


df_combined = df_combined[df_combined.columns.drop(list(df_combined.filter(regex='-')))]
df_combined.head()


# In[6]:


df_combined.columns


# In[7]:


(df_combined[df_combined['em4'].isnull()]).shape


# In[8]:


len(celllist)


# In[9]:


poscols = ['chrom', 'start', 'end']
outdf=df_combined[poscols+celllist]


#df['combined'] = df[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)


# In[10]:


outdf.head()


# In[11]:


outdf=outdf.copy()
outdf['position']=outdf[poscols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
outdf=outdf.drop(poscols, axis=1)

outdf=outdf.set_index('position')
outdf.head()


# In[12]:


outdf.shape

outdf.to_csv(infolder+"_forheat"+".txt",sep="\t")

print("underlying txt saved. Now heatmap")


# In[16]:


sns.set(font_scale=1.5)
plt.figure(figsize=(30,10))
mycmap = plt.cm.viridis
mycmap.set_bad("dimgrey")
aaa=sns.heatmap(outdf, cmap=mycmap,vmin=0, vmax=1, yticklabels=False)
aaa.xaxis.tick_top() # x axis on top

heatname=infolder+"_heat"+".pdf"
plt.savefig(heatname,bbox_inches = "tight")
#plt.show()

