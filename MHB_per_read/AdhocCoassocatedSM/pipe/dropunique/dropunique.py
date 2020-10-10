#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys


# In[2]:

import sys
fname=sys.argv[1] #"/Users/irffanalahi/Research/weekly/for_10_8_20/my/adhocsm_allpblsubset/450kpos/pblsubsetpoormanMHB_hypo.txt_assigned.txt_mhb_intwith_blleuko450kg50_hyporadius_150bpSortedMerged.txt"

atleastcpg=int(sys.argv[2])

outname=fname+"_atleast"+str(atleastcpg)+"cpg.txt"

df=pd.read_csv(fname,sep="\t")
df.head()


# In[3]:


outdf=df.copy()
uniqindex=[]
for index, row in df.iterrows():
    currentchr=row['blockchr']
    currentstart=row['blockstart']
    count=0
    for i2,r2 in df.iterrows():
        if (r2['blockchr']==currentchr) and (r2['blockstart']==currentstart):
            count=count+1
            if count==atleastcpg:
                break
    if count==0:
        print("error")
        sys.exit()
    elif count < atleastcpg:
        
        uniqindex.append(index)


#print(len(uniqindex))
#print(uniqindex)
        
outdf=outdf.drop(uniqindex)
    


# In[4]:


outdf.to_csv(outname,sep="\t",index=False)

