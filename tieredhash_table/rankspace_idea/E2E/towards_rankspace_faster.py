#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import os
import sys
import re
import time
start_time = time.time()

infol=sys.argv[1] #'tr_sub'

outname=sys.argv[2] #infol+"_CpGdelta_info_faster.txt"


# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[3]:


allfiles=listdir_nohidden(infol)
allfiles


# In[4]:



def whichCTs(inputfile):
    m = re.search('g1_(.+?)_g2_(.+?)$', inputfile)
    if m:
        found1 = m.group(1)
        found2=m.group(2)

    else:
        print("found=",found)
        print("exiting")

        sys.exit(1)




    celltype1=found1
    celltype2=found2
    
    return celltype1,celltype2


# In[5]:


filesdf=[]

for fp in allfiles:
    
    basefp=os.path.basename(fp)
    
    c1,c2=whichCTs(basefp)
    
    tmpdf=pd.read_csv(fp,sep="\t")
    #tmpdf['filename']=basefp
    
    tmpdf.rename(columns={c1+"-others": c1+"-"+c2},inplace=True,errors='raise')
    
    tmpdf=tmpdf[['chrom','start','end',c1+"-"+c2]]
    
    filesdf.append(tmpdf)
    


# In[6]:


df_combined = pd.concat(filesdf, axis=0)
df_combined.set_index(['chrom','start','end'],inplace=True)
df_combined.head()


# In[7]:


outdf=df_combined.groupby(df_combined.index).sum()
outdf.head()


# In[8]:


outdf.reset_index(inplace=True)


# In[9]:


outdf[['chrom', 'start','end']] = pd.DataFrame(outdf['index'].tolist(), index=outdf.index)


# In[10]:


outdf=outdf.drop(['index'],axis=1)


# In[11]:


outdf=outdf.set_index(['chrom','start','end'])
outdf.shape


# In[12]:


outdf=outdf[(outdf != 0).all(axis=1)]
outdf.shape


# In[13]:


outdf.head()


# In[14]:


scorecols=outdf.columns
scorecols


# In[15]:



outdf['maxdelta']=outdf[scorecols].max(axis=1)
outdf['mindelta']=outdf[scorecols].min(axis=1)
outdf['Avgdelta']=outdf[scorecols].mean(axis=1)

outdf.head()


# In[16]:


outdf.reset_index(inplace=True)


outdf.to_csv(outname,sep="\t",index=False)


# In[17]:


end_time = time.time()

time_elapsed = (end_time - start_time)

print(time_elapsed)

