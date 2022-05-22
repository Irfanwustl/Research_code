#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import pybedtools
import sys

file =sys.argv[1]
outfol =sys.argv[2]
interfol =sys.argv[3]
a = pybedtools.BedTool(file)


# In[2]:


c = a.merge(c=11, o='mean')
file_name = interfol + '/' + file.split('/')[-1]
d = c.saveas(file_name)


# In[3]:


df = pd.read_csv(file_name, sep='\t', names=['chr', 'start', 'end', 'met'])


# In[4]:


#df.head()


# In[5]:


#a.head()


# In[6]:


adf = pd.read_table(a.fn,header=None)
#adf.head()


# In[7]:


bothdfmerged=df.merge(adf,left_on=['chr','start','end'],right_on=[0,1,2],how='left')
#bothdfmerged.head(n=15)


# In[8]:


bothdfmerged[bothdfmerged[5]=='-']


# In[9]:


adf.shape


# In[10]:


df.shape


# In[11]:


bothdfmerged.shape


# In[12]:


bothdfmerged.rename(columns={5:'strand'},inplace=True)


# In[13]:


#bothdfmerged.loc[bothdfmerged[bothdfmerged[5]=='+'],'end']=bothdfmerged.loc[bothdfmerged[bothdfmerged[5]=='+'],'end']+1
#bothdfmerged.loc[bothdfmerged[bothdfmerged['strand']=='+']]
bothdfmerged.loc[bothdfmerged['strand']=='+','end']=bothdfmerged.loc[bothdfmerged['strand']=='+','end']+1
bothdfmerged.loc[bothdfmerged['strand']=='-','start']=bothdfmerged.loc[bothdfmerged['strand']=='-','start']-1


# In[14]:


df=bothdfmerged[['chr', 'start', 'end', 'met']].copy()


# In[15]:



df['met'] = np.array(df['met']) / 100


# In[16]:


df.to_csv(outfol + '/' + file.split('/')[-1], sep='\t', index=None, header=None)

