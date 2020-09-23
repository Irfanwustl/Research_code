#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:



##### param#####
import sys

infile=sys.argv[1]  #"/Users/irffanalahi/Research/Research_code/gitignorefolder/dataformonod2analysis/forchangingBlockValue/testinhead/CD4-PBMC-1382_head.bedgraph_rolled_pathological2.bedgraph"

outfile=sys.argv[2]  #infile+"_meanbased"



mincutoff=float(sys.argv[3])  #0.25  # if mhb <mincutoff set to 0
maxcutoff=float(sys.argv[4])  #0.75  #if mhb >maxcutoff set to 1

mincpg=int(sys.argv[5])   #3


# In[3]:


df=pd.read_csv(infile,sep="\t",header=None)

df.head()


# In[4]:


df = df.rename(columns={0: "CpGchr",1:"CpGstart",2:"CpGend",3:"CpGval",4:"MHBchr",5:"MHBstart",6:"MHBend" })
df.head()


# In[5]:


df=df.drop(["CpGchr","CpGstart","CpGend"],axis=1)
df.head()


# In[6]:


df=(df.groupby(["MHBchr","MHBstart","MHBend"]).filter(lambda x: len(x["CpGval"]) >= mincpg))
#print(df.head())
df=df.groupby(["MHBchr","MHBstart","MHBend"]).mean().reset_index()
df.head()


# In[7]:


df.loc[df["CpGval"]<mincutoff,"CpGval"]=0
df.loc[df["CpGval"]>maxcutoff,"CpGval"]=1
df.head()


# In[8]:


outdf=df[(df.CpGval == 1) | (df.CpGval == 0)]
outdf.head()


# In[9]:


outdf.to_csv(outfile,sep="\t",index=False,header = False)

