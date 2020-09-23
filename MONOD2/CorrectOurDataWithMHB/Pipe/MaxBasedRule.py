#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys


# In[2]:



##### param#####

infile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/dataformonod2analysis/forchangingBlockValue/testinhead/CD4-PBMC-1382_head.bedgraph_rolled_pathological2.bedgraph"

outfile=sys.argv[2] #infile+"_maxbased"
mincut=float(sys.argv[3]) #0.5  # < mincut
maxcut=float(sys.argv[4]) #0.5  # mhb > maxcut

mincpg=int(sys.argv[5]) #3


# In[3]:


##given group calculate the value
def assignMHBvalue(singleMHB,mincutoff,maxcutoff):
    underminval=singleMHB[singleMHB.CpGval<mincutoff]
    overmaxval=singleMHB[singleMHB.CpGval>maxcutoff]
    
    inthemiddle=singleMHB[(singleMHB.CpGval>=mincutoff) & (singleMHB.CpGval<=maxcutoff)]
    
    underminval_count=underminval.shape[0]
    overmaxval_count=overmaxval.shape[0]
    inthemiddle_count =inthemiddle.shape[0]
    
    
    if (underminval_count + overmaxval_count + inthemiddle_count) != singleMHB.shape[0]:
        print ("error in assignMHBvalue")
        sys.exit (1)
        
    
    if inthemiddle_count < underminval_count or inthemiddle_count < overmaxval_count:
        if underminval_count > overmaxval_count:
            return underminval["CpGval"].mean()
        elif underminval_count < overmaxval_count:
            return overmaxval["CpGval"].mean()
        else:
            return -1 ###### as both in different direction and the count is larger than inthemiddle
    
    else:
        return inthemiddle["CpGval"].mean()
        
    
    


# In[4]:


df=pd.read_csv(infile,sep="\t",header=None)

df.head()


# In[5]:


df = df.rename(columns={0: "CpGchr",1:"CpGstart",2:"CpGend",3:"CpGval",4:"MHBchr",5:"MHBstart",6:"MHBend" })
df.head()


# In[6]:


df=df.drop(["CpGchr","CpGstart","CpGend"],axis=1)
df.head()


# In[7]:


df=(df.groupby(["MHBchr","MHBstart","MHBend"]).filter(lambda x: len(x["CpGval"]) >= mincpg))
dfgrp=df.groupby(["MHBchr","MHBstart","MHBend"])


# In[8]:


alluniquemhb=dfgrp.groups.keys()


# In[9]:


allmhbrows=[]
for g in alluniquemhb:
    
   
    tempval=assignMHBvalue(dfgrp.get_group(g),mincut,maxcut)
    
    #print(tempval)
    
    if tempval!=-1:
        glist=list(g)
        glist.append(tempval)
        allmhbrows.append(glist)
    
outdf=pd.DataFrame(allmhbrows)
outdf.head()


# In[10]:


outdf.to_csv(outfile,sep="\t",index=False,header = False)

