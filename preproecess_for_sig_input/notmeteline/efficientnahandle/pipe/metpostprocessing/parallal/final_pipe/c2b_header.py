#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys


infile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/metpostprocess/troubleshhoting/BLthirteen_all_matrixCin_nr0.5_imputed_rowmean_head1000.txt"
out=sys.argv[2] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/metpostprocess/troubleshhoting/BLthirteen_all_matrixCin_nr0.5_imputed_rowmean_head1000.bg"
infiledf=pd.read_csv(infile,sep="\t")
infiledf.head()


# In[2]:


infiledf[['anotherchrom','anotherpos']] = infiledf.position.str.split(":",expand=True) 
infiledf['anotherpos']=infiledf['anotherpos'].astype(int)
infiledf.head()


# In[3]:


infiledf['start']=infiledf['anotherpos']-1
infiledf['end']=infiledf['anotherpos']+1
infiledf.head()


# In[4]:


infiledf=infiledf.drop(['position','anotherpos'],axis=1)
infiledf.head()


# In[5]:


first_column = infiledf.pop('anotherchrom')
second_column = infiledf.pop('start')
third_column = infiledf.pop('end')
infiledf.rename(columns={"chrom": "shouldbechrom"},inplace=True)
infiledf.head()


# In[6]:


infiledf.shape


# In[7]:


infiledf.insert(0, 'chrom', first_column)
infiledf.insert(1, 'start', second_column)
infiledf.insert(2, 'end', third_column)
infiledf.head()


# In[8]:


infiledf.shape


# In[9]:


infiledf.to_csv(out,sep="\t",index=False)
print("done")

